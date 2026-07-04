"""
向量数据库操作模块。使用 Chroma 作为本地向量数据库，支持多知识库管理。Embedding 默认通过 SiliconFlow API 调用 BAAI/bge-large-zh-v1.5。"""

import hashlib
import logging
import os
import re
import uuid
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_chroma import Chroma

import config
from .reranker import create_bge_compressor

import threading

logger = logging.getLogger(__name__)
_embedding_model = None
_embedding_lock = threading.Lock()
EMBEDDING_SAFE_MAX_CHARS = 180
EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS = 300
EMBEDDING_SPLIT_OVERLAP = 60
EMBEDDING_MIN_RETRY_CHARS = 40


def get_embedding_model():
    """
    获取 Embedding 模型实例（单例模式）。    默认使用 SiliconFlow API 的 BAAI/bge-large-zh-v1.5 模型。    """
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model
    with _embedding_lock:
        if _embedding_model is not None:
            return _embedding_model
        from langchain_openai import OpenAIEmbeddings

        logger.info(f"正在初始化 Embedding 模型: {config.EMBEDDING_MODEL}")

        _embedding_model = OpenAIEmbeddings(
            api_key=config.LLM_API_KEY,
            model=config.EMBEDDING_MODEL,
            base_url=config.EMBEDDING_API_BASE,
            # SiliconFlow expects raw text inputs for multilingual embeddings.
            # This project already applies conservative chunking before upload,
            # so LangChain must not convert strings into OpenAI token-id arrays.
            check_embedding_ctx_length=False,
        )
        logger.info(f"Embedding 模型初始化完成 {config.EMBEDDING_MODEL}")
    return _embedding_model


def sanitize_collection_name(name: str) -> str:
    """
    将用户可见知识库名称转换为 Chroma 支持的 collection 名称。    Chroma 要求名称只包含 [a-zA-Z0-9._-]，长度 3-512，且首尾为字母或数字。
    Args:
        name: 用户输入的知识库名称，可能包含中文。
    Returns:
        str: 合法的 Chroma collection 名称。    """
    # Return unchanged when the name already satisfies Chroma's rules.
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{1,510}[a-zA-Z0-9]$', name):
        return name

    # 非 ASCII 名称使用稳定哈希映射，避免 Chroma 名称限制。    # Use an MD5 prefix to keep non-ASCII collection names Chroma-safe.
    name_hash = hashlib.md5(name.encode('utf-8')).hexdigest()[:16]
    safe_name = f"kb_{name_hash}"

    logger.info(f"知识库名称转换 '{name}' -> '{safe_name}'")
    return safe_name


class VectorStoreManager:
    """
    向量存储管理器。    负责多知识库 collection 的创建、查询、重命名、删除和名称映射持久化。    """
    def __init__(self, db_path: str = None):
        """
        初始化向量存储管理器。
        Args:
            db_path: Chroma 数据库持久化路径，默认从配置读取。        """
        self.db_path = db_path or config.CHROMA_DB_PATH
        self._ensure_db_dir()

        # Cache loaded vectorstore instances.
        self._stores: dict = {}
        self._last_search_trace: dict = {}
        self._collection_cache: dict = {}

        # User-visible name -> internal Chroma collection name.
        self._name_mapping: dict = {}

        # Persistent user-visible name -> Chroma collection name mapping.
        self._mapping_file = Path(self.db_path) / "collection_name_mapping.json"

        # Load persisted name mapping from disk.
        self._load_name_mapping()

        logger.info(f"向量存储管理器初始化完成，数据库路径: {self.db_path}")

    def _load_name_mapping(self):
        """Load persisted collection name mapping."""
        if self._mapping_file.exists():
            try:
                import json
                with open(self._mapping_file, "r", encoding="utf-8") as f:
                    self._name_mapping = json.load(f)
                logger.info(f"已从磁盘加载 {len(self._name_mapping)} 个知识库名称映射")
            except Exception as e:
                logger.warning(f"加载名称映射失败: {e}")
                self._name_mapping = {}
        else:
            self._name_mapping = {}

    def _save_name_mapping(self):
        """Save collection name mapping to disk."""
        try:
            import json
            with open(self._mapping_file, "w", encoding="utf-8") as f:
                json.dump(self._name_mapping, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存名称映射失败: {e}")

    def _ensure_db_dir(self):
        """Ensure the vector database directory exists."""
        Path(self.db_path).mkdir(parents=True, exist_ok=True)

    def _get_collection_name(self, name: str) -> str:
        """
        获取或创建名称映射。
        Args:
            name: 用户指定的知识库名称。
        Returns:
            str: 合法的 collection 名称。        """
        # Return directly when the input is already an internal Chroma name.
        chroma_to_user = {v: k for k, v in self._name_mapping.items()}
        if name in chroma_to_user:
            return name

        if name not in self._name_mapping:
            self._name_mapping[name] = sanitize_collection_name(name)
            self._save_name_mapping()
        return self._name_mapping[name]

    def _get_store(self, collection_name: str) -> Chroma:
        """
        获取或创建指定知识库的向量存储实例。
        Args:
            collection_name: 用户友好的知识库名称，可能包含中文。
        Returns:
            Chroma: 向量存储实例。        """
        # Convert the user-visible name to a Chroma-safe collection name.
        chroma_name = self._get_collection_name(collection_name)

        if collection_name not in self._stores:
            embeddings = get_embedding_model()

            self._stores[collection_name] = Chroma(
                collection_name=chroma_name,
                embedding_function=embeddings,
                persist_directory=self.db_path,
            )

        return self._stores[collection_name]

    def _collection_exists(self, collection_name: str) -> bool:
        """Return whether the underlying Chroma collection still exists."""
        chroma_name = self._name_mapping.get(collection_name)
        if not chroma_name:
            chroma_to_user = {v: k for k, v in self._name_mapping.items()}
            chroma_name = collection_name if collection_name in chroma_to_user else sanitize_collection_name(collection_name)
        try:
            from chromadb import PersistentClient

            client = PersistentClient(path=self.db_path)
            collection_names = [
                col if isinstance(col, str) else getattr(col, "name", "")
                for col in client.list_collections()
            ]
            return chroma_name in collection_names
        except Exception as e:
            logger.warning("检查知识库 '%s' 是否存在失败: %s", collection_name, e)
            return True

    def _is_collection_deleted_state_error(self, error: Exception) -> bool:
        """Detect Chroma wrapper errors raised after a collection was already deleted."""
        message = str(error).lower()
        return (
            "collection not initialized" in message
            or "reset_collection" in message
            or "does not exist" in message
            or "not found" in message
            or "already deleted" in message
        )

    def _discard_collection_state(self, collection_name: str, store: Optional[Chroma] = None) -> None:
        """Clear local caches and persisted name mapping after collection deletion."""
        if store is not None:
            try:
                self._invalidate_collection_cache(store)
            except Exception:
                self._invalidate_collection_cache(collection_name=collection_name)
        else:
            self._invalidate_collection_cache(collection_name=collection_name)

        self._stores.pop(collection_name, None)
        if collection_name in self._name_mapping:
            del self._name_mapping[collection_name]
            self._save_name_mapping()

    def add_documents(
        self,
        documents: List[Document],
        collection_name: str = "default",
    ) -> int:
        """
        向指定知识库添加文档。
        Args:
            documents: 要添加的文档列表。            collection_name: 目标知识库名称，默认为 default。
        Returns:
            int: 成功添加的文档块数量。
        Raises:
            ValueError: 文档列表为空。
            RuntimeError: 添加失败。        """
        if not documents:
            raise ValueError("文档列表不能为空")

        try:
            store = self._get_store(collection_name)

            documents = self._split_oversized_documents(documents)
            ingest_batch_id = uuid.uuid4().hex
            for doc in documents:
                doc.metadata = dict(doc.metadata or {})
                doc.metadata["ingest_batch_id"] = ingest_batch_id

            # SiliconFlow Embedding has strict token limits; keep batches modest.
            batch_size = 32
            for start in range(0, len(documents), batch_size):
                batch = documents[start:start + batch_size]
                self._add_documents_with_embedding_retry(store, batch)

            self._persist_store_if_supported(store)

            logger.info(f"成功添加 {len(documents)} 个文档块到知识库 '{collection_name}'")
            self._invalidate_collection_cache(store)
            return len(documents)

        except Exception as e:
            if "store" in locals() and "ingest_batch_id" in locals():
                self._rollback_ingest_batch(store, collection_name, ingest_batch_id)
            error_msg = f"添加文档到知识库失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def _add_documents_with_embedding_retry(self, store: Chroma, documents: List[Document]) -> None:
        """Add documents and split failed embedding inputs more aggressively on token-limit errors."""
        try:
            store.add_documents(documents)
            return
        except Exception as e:
            if not self._is_embedding_token_limit_error(e):
                raise

            if len(documents) > 1:
                midpoint = max(1, len(documents) // 2)
                logger.warning(
                    "Embedding batch hit token limit; retrying as smaller batches: batch_size=%s",
                    len(documents),
                )
                self._add_documents_with_embedding_retry(store, documents[:midpoint])
                self._add_documents_with_embedding_retry(store, documents[midpoint:])
                return

            doc = documents[0]
            parts = self._split_single_failed_embedding_document(doc)
            if len(parts) <= 1:
                raise

            logger.warning(
                "Embedding single chunk hit token limit; retrying with smaller chunks: source=%s, len=%s, parts=%s",
                doc.metadata.get("source"),
                len(doc.page_content or ""),
                len(parts),
            )
            self._add_documents_with_embedding_retry(store, parts)

    def _is_embedding_token_limit_error(self, error: Exception) -> bool:
        """Return True for SiliconFlow/OpenAI-compatible embedding token-limit failures."""
        message = str(error).lower()
        return (
            "less than 512 tokens" in message
            or "maximum context length" in message
            or "request entity too large" in message
            or "error code: 413" in message
        )

    def _split_single_failed_embedding_document(self, doc: Document) -> List[Document]:
        """Split one document more aggressively after the provider rejects it."""
        content = doc.page_content or ""
        if len(content) <= EMBEDDING_MIN_RETRY_CHARS:
            return [doc]

        retry_max_chars = max(EMBEDDING_MIN_RETRY_CHARS, min(len(content) // 2, EMBEDDING_SAFE_MAX_CHARS // 2))
        retry_overlap = min(10, max(0, retry_max_chars // 5))
        parts = self._split_text_by_chars(
            content,
            max_chars=retry_max_chars,
            overlap=retry_overlap,
        )

        split_docs = []
        for idx, part in enumerate(parts):
            metadata = dict(doc.metadata or {})
            metadata.setdefault("parent_chunk_index", metadata.get("chunk_index"))
            existing_sub_index = metadata.get("sub_chunk_index")
            metadata["sub_chunk_index"] = f"{existing_sub_index}.{idx}" if existing_sub_index is not None else idx
            metadata["embedding_retry_split"] = True
            split_docs.append(Document(page_content=part, metadata=metadata))

        return split_docs

    def _rollback_ingest_batch(self, store: Chroma, collection_name: str, ingest_batch_id: str) -> int:
        """Delete chunks written by the current failed ingest attempt."""
        try:
            raw = store._collection.get(include=["metadatas"])
            ids_to_delete = []

            for doc_id, metadata in zip(raw.get("ids") or [], raw.get("metadatas") or []):
                metadata = metadata or {}
                if metadata.get("ingest_batch_id") == ingest_batch_id:
                    ids_to_delete.append(doc_id)

            if not ids_to_delete:
                return 0

            store._collection.delete(ids=ids_to_delete)
            self._persist_store_if_supported(store)
            self._invalidate_collection_cache(store)
            logger.warning(
                "宸插洖婊氬け璐ヤ笂浼犵殑閮ㄥ垎鍏ュ簱鐗囨: collection=%s, chunks=%s",
                collection_name,
                len(ids_to_delete),
            )
            return len(ids_to_delete)
        except Exception as rollback_error:
            logger.error(f"回滚失败的上传批次失败 {rollback_error}")
            return 0

    def _persist_store_if_supported(self, store) -> bool:
        """Persist only legacy vector store wrappers that still require it."""
        persist = getattr(store, "persist", None)
        if not callable(persist):
            return False

        store_module = store.__class__.__module__
        if store_module.startswith(("langchain_chroma", "langchain_community.vectorstores")):
            return False

        persist()
        return True

    def _split_oversized_documents(self, documents: List[Document]) -> List[Document]:
        """
        Embedding API 单条输入有长度限制，入库前将超长块二次切分。        """
        max_chars = EMBEDDING_SAFE_MAX_CHARS
        max_estimated_tokens = EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS
        overlap = EMBEDDING_SPLIT_OVERLAP
        normalized = []

        for doc in documents:
            content = doc.page_content or ""
            if (
                len(content) <= max_chars
                and self._estimate_embedding_tokens(content) <= max_estimated_tokens
            ):
                normalized.append(doc)
                continue

            parts = self._split_text_for_embedding_limit(
                content,
                max_chars=max_chars,
                max_estimated_tokens=max_estimated_tokens,
                overlap=overlap,
            )
            for idx, part in enumerate(parts):
                metadata = dict(doc.metadata)
                metadata["parent_chunk_index"] = metadata.get("chunk_index")
                metadata["sub_chunk_index"] = idx
                normalized.append(Document(page_content=part, metadata=metadata))

        if len(normalized) != len(documents):
            logger.info(f"瓒呴暱鍒嗗潡浜屾鍒囧垎: {len(documents)} -> {len(normalized)}")
        return normalized

    def _split_text_for_embedding_limit(
        self,
        text: str,
        max_chars: int,
        max_estimated_tokens: int,
        overlap: int,
    ) -> List[str]:
        """Split text until every part is comfortably below the embedding API limit."""
        parts = self._split_text_by_chars(text, max_chars=max_chars, overlap=overlap)
        normalized = []

        for part in parts:
            if self._estimate_embedding_tokens(part) <= max_estimated_tokens:
                normalized.append(part)
                continue

            normalized.extend(
                self._split_text_for_embedding_limit(
                    part,
                    max_chars=max(60, max_chars // 2),
                    max_estimated_tokens=max(120, max_estimated_tokens // 2),
                    overlap=min(overlap, max(0, max_chars // 6)),
                )
            )

        return normalized

    def _estimate_embedding_tokens(self, text: str) -> int:
        """
        Conservative local token estimate used only as a preflight guard.

        SiliconFlow rejects embedding inputs over 512 tokens. We avoid adding a
        tokenizer dependency here and instead over-count punctuation/code-heavy
        text, which is where char-based splitting is most likely to fail.
        """
        if not text:
            return 0

        tokens = 0
        ascii_run = 0

        for char in text:
            codepoint = ord(char)
            if char.isascii() and char.isalnum():
                ascii_run += 1
                continue

            if ascii_run:
                tokens += max(1, (ascii_run + 3) // 4)
                ascii_run = 0

            if char.isspace():
                continue
            if 0x4E00 <= codepoint <= 0x9FFF:
                tokens += 1
            elif char.isascii():
                tokens += 1
            else:
                tokens += 2

        if ascii_run:
            tokens += max(1, (ascii_run + 3) // 4)

        return tokens

    def _split_text_by_chars(self, text: str, max_chars: int, overlap: int) -> List[str]:
        """Split text by preferred boundaries without exceeding embedding limits."""
        if len(text) <= max_chars:
            return [text]

        parts = []
        start = 0
        separators = ["\n\n", "\n", "。", "，", "；", "：", "、", " "]

        while start < len(text):
            end = min(start + max_chars, len(text))
            if end < len(text):
                split_at = -1
                window = text[start:end]
                for sep in separators:
                    pos = window.rfind(sep)
                    if pos >= int(max_chars * 0.55):
                        split_at = start + pos + len(sep)
                        break
                if split_at > start:
                    end = split_at

            part = text[start:end].strip()
            if part:
                parts.append(part)

            if end >= len(text):
                break
            start = max(end - overlap, start + 1)

        return parts

    def similarity_search(
        self,
        query: str,
        collection_name: str = "default",
        top_k: int = None,
        enable_contextual_compression: Optional[bool] = None,
    ) -> List[Document]:
        """
        鐩镐技搴︽绱細鍏堝彫鍥炶緝澶氬€欓€夛紝鍐嶇粨鍚?BM25銆佸叧閿瘝鍜岄噸鎺掔瓫閫夌粨鏋溿€?
        Args:
            query: 查询文本。            collection_name: 知识库名称。            top_k: 返回结果数量，默认从配置读取。
        Returns:
            List[Document]: 相关文档片段列表。
        Raises:
            RuntimeError: 检索失败。        """
        top_k = top_k or config.RETRIEVER_TOP_K
        use_compression = (
            config.ENABLE_CONTEXTUAL_COMPRESSION
            if enable_contextual_compression is None
            else enable_contextual_compression
        )

        try:
            store = self._get_store(collection_name)

            # Retrieve a wider candidate set before hybrid reranking.
            initial_k = self._initial_candidate_count(top_k)
            vector_docs_and_scores = store.similarity_search_with_score(
                query=query,
                k=initial_k,
            )
            vector_docs = self._documents_from_vector_scores(vector_docs_and_scores)
            vector_docs = [d for d in vector_docs if d.metadata.get("enabled", True)]
            ensemble_docs, bm25_count = self._ensemble_hybrid_search(
                store=store,
                query=query,
                vector_docs=vector_docs,
                top_k=initial_k,
            )
            keyword_docs = self._keyword_search(store, query, initial_k)

            if ensemble_docs:
                docs_and_scores = self._documents_to_pseudo_scores(ensemble_docs)
                docs_and_scores.extend(keyword_docs)
            else:
                # Fall back to vector results plus lightweight keyword search.
                docs_and_scores = list(vector_docs_and_scores)
                docs_and_scores.extend(keyword_docs)

            candidate_count = self._rerank_candidate_count(top_k)
            reranked_results = self._rerank_results(query, docs_and_scores, candidate_count)
            expanded_results = self._expand_related_subchunks(store, reranked_results, candidate_count)
            compression_trace = {"enabled": use_compression}
            if use_compression:
                final_results, compression_trace = self._compress_with_contextual_retriever(
                    query,
                    expanded_results,
                    top_k,
                )
            else:
                final_results = expanded_results[:top_k]
            self._last_search_trace = {
                "vector_candidate_count": len(vector_docs_and_scores),
                "bm25_candidate_count": bm25_count,
                "keyword_candidate_count": len(keyword_docs),
                "ensemble_candidate_count": len(ensemble_docs),
                "retrieved_count": len(docs_and_scores),
                "reranked_count": len(reranked_results),
                "selected_count": len(final_results),
                "top_k": top_k,
                "initial_k": initial_k,
                "rerank_candidate_count": candidate_count,
                "contextual_compression": use_compression,
                "compression": compression_trace,
                "weights": self._retrieval_weight_trace(),
                "final_documents": self._trace_documents(final_results),
            }

            logger.info(
                "知识库 %s 检索完成，查询 %s... 返回 %s 条结果",
                collection_name,
                query[:30],
                len(final_results),
            )
            return final_results

        except Exception as e:
            raw_error = str(e)
            if "expecting embedding with dimension" in raw_error.lower():
                error_msg = (
                    "向量检索失败：当前知识库的向量维度与现用 Embedding 模型不一致。"
                    "请使用当前 EMBEDDING_MODEL 重新上传或重建该知识库。"
                )
            else:
                error_msg = f"向量检索失败 {raw_error}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def get_last_search_trace(self) -> dict:
        """Return statistics from the latest retrieval pass."""
        return dict(self._last_search_trace)

    def _trace_documents(self, documents: List[Document]) -> list[dict]:
        """Build JSON-safe trace metadata for final retrieval results."""
        traced = []
        for index, doc in enumerate(documents, 1):
            metadata = dict(doc.metadata or {})
            section = (
                metadata.get("header_3")
                or metadata.get("header_2")
                or metadata.get("section_header")
                or metadata.get("header_1")
                or ""
            )
            traced.append({
                "index": index,
                "source": metadata.get("source", "未知文档"),
                "section": section,
                "score": metadata.get("score", 0),
                "vector_score": metadata.get("vector_score", 0),
                "keyword_score": metadata.get("keyword_score", 0),
                "phrase_score": metadata.get("phrase_score", 0),
                "rerank_score": metadata.get("rerank_score", 0),
                "distance": metadata.get("distance", 0),
                "candidate_source": metadata.get("candidate_source", ""),
                "keyword_candidate_score": metadata.get("keyword_candidate_score", 0),
                "ensemble_rank": metadata.get("ensemble_rank", 0),
                "expanded_subchunks": metadata.get("expanded_subchunks", 0),
                "contextual_compression_protected": metadata.get("contextual_compression_protected", False),
            })
        return traced

    def _initial_candidate_count(self, top_k: int) -> int:
        multiplier = max(int(config.RETRIEVER_INITIAL_K_MULTIPLIER), 1)
        minimum = max(int(config.RETRIEVER_INITIAL_K_MIN), top_k)
        return max(top_k * multiplier, minimum)

    def _rerank_candidate_count(self, top_k: int) -> int:
        multiplier = max(int(config.RETRIEVER_RERANK_K_MULTIPLIER), 1)
        return max(top_k * multiplier, top_k)

    def _retrieval_weight_trace(self) -> dict:
        return {
            "hybrid_vector": config.HYBRID_VECTOR_WEIGHT,
            "hybrid_bm25": config.HYBRID_BM25_WEIGHT,
            "rerank_vector": config.RERANK_VECTOR_WEIGHT,
            "rerank_keyword": config.RERANK_KEYWORD_WEIGHT,
            "rerank_phrase": config.RERANK_PHRASE_WEIGHT,
            "keyword_header": config.KEYWORD_HEADER_WEIGHT,
            "keyword_phrase": config.KEYWORD_PHRASE_WEIGHT,
        }

    def _documents_from_vector_scores(self, docs_and_scores: list) -> List[Document]:
        """Copy vector candidates and keep distance scores for ensemble merging."""
        documents = []
        for doc, distance in docs_and_scores:
            metadata = dict(doc.metadata or {})
            metadata["candidate_source"] = "vector"
            metadata["distance"] = float(distance)
            documents.append(Document(page_content=doc.page_content, metadata=metadata))
        return documents

    def _get_cached_collection_snapshot(self, store: Chroma) -> dict:
        """Read and cache collection documents used by lexical retrieval helpers."""
        cache_key = self._collection_cache_key(store)
        cached = self._collection_cache.get(cache_key)
        current_count = self._safe_collection_count(store)
        if cached and cached.get("count") == current_count:
            return cached

        try:
            raw = store._collection.get(include=["documents", "metadatas"])
        except Exception as e:
            logger.warning(f"读取 collection 文档失败: {e}")
            empty_cache = {
                "count": current_count,
                "documents": [],
                "raw_pairs": [],
                "parent_index": {},
                "bm25": None,
            }
            self._collection_cache[cache_key] = empty_cache
            return empty_cache

        documents = []
        raw_pairs = []
        parent_index = {}
        for content, metadata in zip(raw.get("documents") or [], raw.get("metadatas") or []):
            if content and content.strip():
                metadata = dict(metadata or {})
                if not metadata.get("enabled", True):
                    continue
                documents.append(Document(page_content=content, metadata=metadata))
                raw_pairs.append((content, metadata))
                parent_idx = metadata.get("parent_chunk_index")
                source = metadata.get("source")
                if parent_idx is not None and source:
                    try:
                        normalized_parent_idx = int(parent_idx)
                    except (TypeError, ValueError):
                        normalized_parent_idx = parent_idx
                    try:
                        sub_chunk_idx = int(metadata.get("sub_chunk_index", 0))
                    except (TypeError, ValueError):
                        sub_chunk_idx = 0
                    parent_index.setdefault((source, normalized_parent_idx), []).append(
                        (sub_chunk_idx, content, metadata)
                    )

        for siblings in parent_index.values():
            siblings.sort(key=lambda item: item[0])

        cache = {
            "count": current_count,
            "documents": documents,
            "raw_pairs": raw_pairs,
            "parent_index": parent_index,
            "bm25": None,
        }
        self._collection_cache[cache_key] = cache
        logger.info(
            "Collection 文档缓存已更新 count=%s, docs=%s, parent_groups=%s",
            current_count,
            len(documents),
            len(parent_index),
        )
        return cache

    def _get_bm25_retriever(self, store: Chroma, documents: List[Document]) -> BM25Retriever:
        """Return a cached BM25 retriever for the current collection snapshot."""
        cache = self._get_cached_collection_snapshot(store)
        if cache.get("bm25") is None:
            cache["bm25"] = BM25Retriever.from_documents(
                documents,
                preprocess_func=self._tokenize_for_bm25,
                k=min(config.RETRIEVER_TOP_K, len(documents)),
            )
            logger.info(f"BM25 缂撳瓨宸叉瀯寤? docs={len(documents)}")
        return cache["bm25"]

    def _collection_cache_key(self, store: Chroma) -> str:
        collection = getattr(store, "_collection", None)
        return str(getattr(collection, "name", None) or id(store))

    def _safe_collection_count(self, store: Chroma) -> int:
        try:
            return int(store._collection.count())
        except Exception:
            return -1

    def _invalidate_collection_cache(self, store: Optional[Chroma] = None, collection_name: Optional[str] = None):
        """Invalidate cached collection documents and BM25 retrievers."""
        if store is not None:
            try:
                self._collection_cache.pop(self._collection_cache_key(store), None)
            except Exception:
                self._collection_cache.clear()
        elif collection_name is not None and collection_name in self._stores:
            try:
                self._collection_cache.pop(self._collection_cache_key(self._stores[collection_name]), None)
            except Exception:
                self._collection_cache.clear()
        else:
            self._collection_cache.clear()

    def _ensemble_hybrid_search(
        self,
        store: Chroma,
        query: str,
        vector_docs: List[Document],
        top_k: int,
    ) -> tuple[List[Document], int]:
        """Merge vector search and BM25 results with LangChain EnsembleRetriever."""
        all_docs = self._get_collection_documents(store)
        if not all_docs:
            return vector_docs, 0

        try:
            vector_retriever = RunnableLambda(lambda _: vector_docs)
            bm25_retriever = self._get_bm25_retriever(store, all_docs)
            bm25_retriever.k = min(top_k, len(all_docs))
            ensemble = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[config.HYBRID_VECTOR_WEIGHT, config.HYBRID_BM25_WEIGHT],
            )
            merged_docs = ensemble.invoke(query)

            results = []
            seen = set()
            for rank, doc in enumerate(merged_docs):
                fingerprint = hashlib.md5(doc.page_content.strip().encode("utf-8")).hexdigest()
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                metadata = dict(doc.metadata or {})
                metadata["ensemble_rank"] = rank + 1
                metadata["candidate_source"] = metadata.get("candidate_source", "bm25")
                results.append(Document(page_content=doc.page_content, metadata=metadata))

            return results[:top_k], min(top_k, len(all_docs))
        except Exception as e:
            logger.warning(f"BM25 + EnsembleRetriever 妫€绱㈠け璐ワ紝鍥為€€鍒板師鍏抽敭璇嶆绱? {e}")
            return [], 0

    def _get_collection_documents(self, store: Chroma) -> List[Document]:
        cache = self._get_cached_collection_snapshot(store)
        return list(cache["documents"])

    def _documents_to_pseudo_scores(self, documents: List[Document]) -> list:
        """
        将 EnsembleRetriever 输出转换为统一重排输入。        BM25 候选没有 Chroma 距离，这里按 Ensemble 排名生成温和的伪距离。        """
        docs_and_scores = []
        total = max(len(documents), 1)
        for idx, doc in enumerate(documents):
            metadata = dict(doc.metadata or {})
            distance = metadata.get("distance")
            if distance is None:
                distance = 0.25 + (idx / total)
            metadata["ensemble_rank"] = metadata.get("ensemble_rank", idx + 1)
            metadata["ensemble_score"] = round(1.0 / (idx + 1), 4)
            docs_and_scores.append((
                Document(page_content=doc.page_content, metadata=metadata),
                float(distance),
            ))
        return docs_and_scores

    def _compress_with_contextual_retriever(
        self,
        query: str,
        documents: List[Document],
        top_k: int,
    ) -> tuple[List[Document], dict]:
        """Compress context with ContextualCompressionRetriever and BGE reranker."""
        trace = {
            "enabled": True,
            "input_count": len(documents),
            "compressed_count": 0,
            "protected_count": 0,
            "fallback_reason": "",
        }
        if not documents:
            return [], trace

        try:
            base_retriever = RunnableLambda(lambda _: documents)
            compression_retriever = ContextualCompressionRetriever(
                base_retriever=base_retriever,
                base_compressor=create_bge_compressor(top_k),
            )
            compressed_docs = list(compression_retriever.invoke(query))
            trace["compressed_count"] = len(compressed_docs)
            if not compressed_docs:
                trace["fallback_reason"] = "empty_compressed_results"
                return documents[:top_k], trace
            final_docs, protected_count = self._protect_compressed_results(
                baseline_docs=documents,
                compressed_docs=compressed_docs,
                top_k=top_k,
            )
            trace["protected_count"] = protected_count
            return final_docs, trace
        except Exception as e:
            logger.warning(f"涓婁笅鏂囧帇缂╁け璐ワ紝浣跨敤鏈帇缂╃墖娈? {e}")
            trace["fallback_reason"] = "compression_error"
            trace["error"] = str(e)
            return documents[:top_k], trace

    def _protect_compressed_results(
        self,
        baseline_docs: List[Document],
        compressed_docs: List[Document],
        top_k: int,
    ) -> tuple[List[Document], int]:
        """Keep high-confidence baseline hits if compression drops them."""
        compressed_limited = compressed_docs[:top_k]
        if not config.ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION:
            return compressed_limited, 0

        protect_limit = max(int(config.CONTEXTUAL_COMPRESSION_PROTECT_TOP_N), 0)
        if protect_limit <= 0:
            return compressed_limited, 0

        compressed_seen = {
            self._document_fingerprint(doc)
            for doc in compressed_limited
        }
        protected_docs = []
        for doc in baseline_docs:
            score = float((doc.metadata or {}).get("score") or 0.0)
            if score < config.CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE:
                continue
            fingerprint = self._document_fingerprint(doc)
            if fingerprint in compressed_seen:
                continue
            metadata = dict(doc.metadata or {})
            metadata["contextual_compression_protected"] = True
            protected_docs.append(Document(page_content=doc.page_content, metadata=metadata))
            if len(protected_docs) >= protect_limit:
                break

        if not protected_docs:
            return compressed_limited, 0

        merged = []
        seen = set()
        for doc in protected_docs + compressed_limited:
            fingerprint = self._document_fingerprint(doc)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            merged.append(doc)
            if len(merged) >= top_k:
                break

        return merged, len(protected_docs)

    def _document_fingerprint(self, doc: Document) -> str:
        content = (doc.page_content or "").strip()
        metadata = doc.metadata or {}
        source = str(metadata.get("source", ""))
        parent = str(metadata.get("parent_chunk_index", ""))
        chunk = str(metadata.get("chunk_index", ""))
        return hashlib.md5(f"{source}|{parent}|{chunk}|{content}".encode("utf-8")).hexdigest()

    def _tokenize_for_bm25(self, text: str) -> List[str]:
        """Tokenize mixed Chinese and English documents for BM25."""
        stopwords = {"什么", "哪些", "怎么", "如何", "以及", "一个", "这个", "那个", "主要"}
        tokens = []

        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_+#.-]*|[\u4e00-\u9fff]{2,}", text.lower()):
            token = token.strip()
            if not token or token in stopwords:
                continue
            tokens.append(token)
            if re.fullmatch(r"[\u4e00-\u9fff]{3,}", token):
                tokens.extend(
                    token[idx:idx + 2]
                    for idx in range(len(token) - 1)
                    if token[idx:idx + 2] not in stopwords
                )

        return tokens or [text.lower().strip()]

    def _expand_related_subchunks(
        self,
        store: Chroma,
        documents: List[Document],
        top_k: int,
    ) -> List[Document]:
        """
        命中超长代码或章节子块时，合并同一父块的相邻子块，恢复完整上下文。        """
        if not documents:
            return []

        expanded = []
        seen = set()
        parent_index = self._get_cached_collection_snapshot(store).get("parent_index", {})

        for doc in documents:
            metadata = doc.metadata or {}
            parent_idx = metadata.get("parent_chunk_index")
            source = metadata.get("source")

            if parent_idx is None or not source:
                fingerprint = hashlib.md5(doc.page_content.strip().encode("utf-8")).hexdigest()
                if fingerprint not in seen:
                    expanded.append(doc)
                    seen.add(fingerprint)
                continue

            try:
                normalized_parent_idx = int(parent_idx)
            except (TypeError, ValueError):
                normalized_parent_idx = parent_idx
            siblings = parent_index.get((source, normalized_parent_idx), [])

            if len(siblings) <= 1:
                fingerprint = hashlib.md5(doc.page_content.strip().encode("utf-8")).hexdigest()
                if fingerprint not in seen:
                    expanded.append(doc)
                    seen.add(fingerprint)
                continue

            sibling_parts = []
            sibling_seen = set()
            for _, content, _ in siblings:
                content = content.strip()
                if not content:
                    continue
                part_fingerprint = hashlib.md5(content.encode("utf-8")).hexdigest()
                if part_fingerprint in sibling_seen:
                    continue
                sibling_seen.add(part_fingerprint)
                sibling_parts.append(content)
            combined = "\n".join(sibling_parts)
            combined = combined[:5000]

            new_metadata = dict(metadata)
            new_metadata["expanded_subchunks"] = len(siblings)
            new_doc = Document(page_content=combined, metadata=new_metadata)
            fingerprint = hashlib.md5(combined.strip().encode("utf-8")).hexdigest()
            if fingerprint not in seen:
                expanded.append(new_doc)
                seen.add(fingerprint)

        return expanded[:top_k]

    def _keyword_search(self, store: Chroma, query: str, top_k: int) -> list:
        """Run lightweight keyword search over titles and content."""
        raw_pairs = self._get_cached_collection_snapshot(store).get("raw_pairs", [])
        query_lower = query.lower().strip()
        query_phrases = self._extract_query_phrases(query_lower)
        query_terms = self._extract_query_terms(query_lower)
        scored = []

        for content, metadata in raw_pairs:
            if not content:
                continue

            metadata = metadata or {}
            metadata_text = " ".join(
                str(metadata.get(key, ""))
                for key in ("source", "header_1", "header_2", "header_3", "section_header")
            ).lower()
            content_lower = content.lower()
            searchable_text = f"{metadata_text}\n{content_lower}"

            keyword_matches = sum(1 for term in query_terms if term in searchable_text)
            if keyword_matches == 0 and query_lower not in searchable_text:
                continue

            header_hits = sum(1 for term in query_terms if term in metadata_text)
            phrase_score = max(
                1.0 if self._has_specific_phrase_match(searchable_text, query_phrases) else 0.0,
                self._metadata_match_score(metadata_text, query_terms, query_phrases),
            )
            special_boost = self._special_keyword_boost(query_terms, searchable_text)
            lexical_score = (
                keyword_matches / max(len(query_terms), 1)
                + header_hits * config.KEYWORD_HEADER_WEIGHT
                + phrase_score * config.KEYWORD_PHRASE_WEIGHT
                + special_boost
            )

            doc = Document(page_content=content, metadata=dict(metadata))
            doc.metadata["keyword_candidate_score"] = round(lexical_score, 4)
            # Keyword hits get a moderate pseudo-distance; reranking still decides.
            pseudo_distance = max(
                config.KEYWORD_PSEUDO_DISTANCE_FLOOR,
                1.0 - min(lexical_score, config.KEYWORD_PSEUDO_DISTANCE_MAX_SCORE),
            )
            scored.append((lexical_score, doc, pseudo_distance))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [(doc, distance) for _, doc, distance in scored[:top_k]]

    def _rerank_results(self, query: str, docs_and_scores: list, top_k: int) -> List[Document]:
        """
        对搜索结果进行重排序。        结合向量相似度和关键词匹配度提升相关性，重排只做辅助优化。
        Args:
            query: 查询文本。            docs_and_scores: 初始搜索结果及 Chroma 距离分数。            top_k: 返回结果数量。
        Returns:
            List[Document]: 重排序后的文档列表。        """
        if not docs_and_scores:
            return []

        query_lower = query.lower().strip()
        query_phrases = self._extract_query_phrases(query_lower)
        query_terms = self._extract_query_terms(query_lower)

        scored_docs = []
        for idx, (doc, distance) in enumerate(docs_and_scores):
            content_lower = doc.page_content.lower()
            metadata_text = " ".join(
                str(doc.metadata.get(key, ""))
                for key in ("source", "header_1", "header_2", "header_3", "section_header")
            ).lower()
            searchable_text = f"{metadata_text}\n{content_lower}"

            keyword_matches = sum(1 for term in query_terms if term in searchable_text)
            keyword_score = keyword_matches / max(len(query_terms), 1)
            keyword_candidate_score = float(doc.metadata.get("keyword_candidate_score") or 0.0)
            if keyword_candidate_score:
                keyword_score = max(
                    keyword_score,
                    min(keyword_candidate_score, config.KEYWORD_MAX_CANDIDATE_SCORE),
                )
            phrase_score = max(
                1.0 if self._has_specific_phrase_match(searchable_text, query_phrases) else 0.0,
                self._metadata_match_score(metadata_text, query_terms, query_phrases),
            )

            # Chroma returns distance, so smaller is better.
            vector_score = 1.0 / (1.0 + max(float(distance), 0.0))

            combined_score = (
                vector_score * config.RERANK_VECTOR_WEIGHT
                + keyword_score * config.RERANK_KEYWORD_WEIGHT
                + phrase_score * config.RERANK_PHRASE_WEIGHT
            )

            doc.metadata["distance"] = float(distance)
            doc.metadata["vector_score"] = round(vector_score, 4)
            doc.metadata["keyword_score"] = round(keyword_score, 4)
            doc.metadata["phrase_score"] = round(phrase_score, 4)
            doc.metadata["score"] = round(combined_score, 4)
            scored_docs.append((combined_score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        min_score = config.RETRIEVER_MIN_SCORE
        filtered = []
        seen = set()
        for score, doc in scored_docs:
            if score < min_score:
                continue
            fingerprint = self._result_dedup_key(doc)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            filtered.append(doc)

        return filtered[:top_k]

    def _metadata_match_score(
        self,
        metadata_text: str,
        query_terms: set,
        query_phrases: List[str],
    ) -> float:
        """Score title/source matches separately from body matches."""
        if not metadata_text:
            return 0.0
        if self._has_specific_phrase_match(metadata_text, query_phrases):
            return 1.0

        normalized_metadata = self._normalize_phrase_text(metadata_text)
        for phrase in query_phrases:
            normalized_phrase = self._normalize_phrase_text(phrase)
            if not self._is_specific_phrase(normalized_phrase):
                continue
            if normalized_phrase in normalized_metadata:
                return 1.0
        return 0.0

    def _has_specific_phrase_match(self, searchable_text: str, query_phrases: List[str]) -> bool:
        """Return true only when an exact phrase is specific enough to boost."""
        for phrase in query_phrases:
            normalized_phrase = self._normalize_phrase_text(phrase)
            if self._is_specific_phrase(normalized_phrase) and phrase in searchable_text:
                return True
        return False

    def _normalize_phrase_text(self, text: str) -> str:
        """Normalize titles and questions for exact phrase matching."""
        normalized = str(text or "").lower()
        for stopword in ("什么", "哪些", "怎么", "如何", "以及", "一个", "这个", "那个", "主要", "的", "有"):
            normalized = normalized.replace(stopword, "")
        return re.sub(r"[^a-z0-9_+#.\-\u4e00-\u9fff]+", "", normalized)

    def _is_specific_phrase(self, phrase: str) -> bool:
        """Avoid boosting broad single-term phrases such as only 'langchain'."""
        if len(phrase) < 4:
            return False
        has_cjk = bool(re.search(r"[\u4e00-\u9fff]", phrase))
        if has_cjk:
            return True
        return len(phrase) >= 12

    def _result_dedup_key(self, doc: Document) -> str:
        """Prefer diverse final results by collapsing same parent or same section."""
        metadata = doc.metadata or {}
        source = str(metadata.get("source") or "")
        parent = metadata.get("parent_chunk_index")
        if source and parent not in (None, ""):
            return f"parent::{source}::{parent}"

        section = " / ".join(
            str(metadata.get(key, "")).strip()
            for key in ("header_1", "header_2", "header_3", "section_header")
            if metadata.get(key)
        )
        if source and section:
            return f"section::{source}::{section}"

        content = (doc.page_content or "").strip()
        return "content::" + hashlib.md5(content.encode("utf-8")).hexdigest()

    def _special_keyword_boost(self, query_terms: set, searchable_text: str) -> float:
        """Boost high-signal implementation terms for specific coding questions."""
        large_file_triggers = {"大文件", "分块", "内存", "内存溢出", "oom"}
        streaming_markers = {
            "stream_read_text",
            "流式读取",
            "逐块读取",
            "逐行读取",
            "chunk_size",
            "oom",
        }
        if not (query_terms & large_file_triggers):
            return 0.0

        hits = sum(1 for marker in streaming_markers if marker.lower() in searchable_text)
        return min(hits * 0.45, 1.8)

    def _extract_query_phrases(self, query: str) -> List[str]:
        """Extract line-level phrases for exact-title matching after query rewrite."""
        lines = [line.strip().lower() for line in re.split(r"[\r\n]+", query or "") if line.strip()]
        if len(lines) > 1:
            lines = lines[:1]

        phrases = []
        for phrase in lines:
            if len(phrase) >= 6:
                phrases.append(phrase)
        return phrases or [query.lower().strip()]

    def _extract_query_terms(self, query: str) -> set:
        """Extract Chinese and English query terms for lexical matching."""
        stopwords = {"什么", "哪些", "怎么", "如何", "以及", "一个", "这个", "那个", "主要"}
        terms = set()

        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_+#.-]*|[\u4e00-\u9fff]{2,}", query):
            token = token.strip().lower()
            if token and token not in stopwords:
                terms.add(token)

        for token in list(terms):
            if re.fullmatch(r"[\u4e00-\u9fff]{4,}", token):
                for i in range(len(token) - 1):
                    gram = token[i:i + 2]
                    if gram not in stopwords:
                        terms.add(gram)

        query_lower = query.lower()
        for rule in config.TERM_EXPANSION_RULES:
            if any(t in query_lower or t in query for t in rule["triggers"]):
                terms.update(rule["expand"])

        return terms or {query}

    def delete_collection(self, collection_name: str) -> bool:
        """
        删除整个知识库。
        Args:
            collection_name: 知识库名称。
        Returns:
            bool: 是否删除成功。        """
        store = None
        try:
            store = self._get_store(collection_name)
            store.delete_collection()
            self._discard_collection_state(collection_name, store)
            logger.info("知识库 '%s' 已删除", collection_name)
            return True

        except Exception as e:
            if self._is_collection_deleted_state_error(e) and not self._collection_exists(collection_name):
                self._discard_collection_state(collection_name, store)
                logger.info("知识库 '%s' 已删除（Chroma 已确认 collection 不存在）", collection_name)
                return True

            error_msg = f"删除知识库失败: {str(e)}"
            logger.error(error_msg)
            return False

    def rename_collection(self, old_name: str, new_name: str) -> bool:
        """
        重命名用户可见知识库名称。        Chroma 内部 collection 名称保持不变，只更新持久化名称映射。        """
        new_name = (new_name or "").strip()
        if not old_name or not new_name:
            return False
        if old_name == new_name:
            return True
        if new_name in self.list_collections():
            raise ValueError(f"知识库 '{new_name}' 已存在")

        try:
            chroma_name = self._get_collection_name(old_name)
            self._name_mapping.pop(old_name, None)
            self._name_mapping[new_name] = chroma_name

            if old_name in self._stores:
                self._invalidate_collection_cache(self._stores[old_name])
                self._stores[new_name] = self._stores.pop(old_name)

            self._save_name_mapping()
            logger.info(f"知识库重命名: '{old_name}' -> '{new_name}'")
            return True
        except Exception as e:
            logger.error(f"知识库重命名失败: {e}")
            raise

    def list_collections(self) -> List[str]:
        """
        列出所有知识库名称。
        Returns:
            List[str]: 知识库名称列表，返回用户友好名称。        """
        try:
            from chromadb import PersistentClient

            client = PersistentClient(path=self.db_path)
            collections = client.list_collections()

            # Chroma collection name -> user-visible name.
            chroma_to_user = {v: k for k, v in self._name_mapping.items()}

            result = []
            for col in collections:
                # Prefer user-visible names when a mapping exists.
                name = chroma_to_user.get(col.name, col.name)
                # Hide the empty default collection.
                if name == "default":
                    try:
                        if col.count() == 0:
                            continue
                    except Exception:
                        pass
                result.append(name)

            # Keep placeholder sync logic for unmapped hashed collections.
            for col in collections:
                if col.name not in chroma_to_user.values() and col.name.startswith("kb_"):
                    # This is an unmapped hashed collection; keep placeholder logic.
                    pass
            return result

        except Exception as e:
            logger.error(f"获取知识库列表失? {str(e)}")
            return []

    def get_collection_info(self, collection_name: str) -> dict:
        """
        获取知识库的基本信息。
        Args:
            collection_name: 知识库名称。
        Returns:
            dict: 包含文档数量等信息的字典。        """
        try:
            store = self._get_store(collection_name)
            count = store._collection.count()
            return {
                "collection_name": collection_name,
                "document_count": count,
                "db_path": self.db_path,
            }

        except Exception as e:
            logger.error(f"获取知识库信息失败 {str(e)}")
            return {
                "collection_name": collection_name,
                "document_count": 0,
                "error": str(e),
            }

    def list_documents(self, collection_name: str) -> List[dict]:
        """Group current collection chunks by source document.

        Reads directly from Chroma (not the retrieval cache) so that
        disabled documents are still visible in the management UI.
        """
        try:
            store = self._get_store(collection_name)
            raw = store._collection.get(include=["documents", "metadatas"])
            grouped = {}

            for content, metadata in zip(raw.get("documents") or [], raw.get("metadatas") or []):
                metadata = metadata or {}
                source = str(metadata.get("source") or metadata.get("file_name") or "未知文档")
                info = grouped.setdefault(source, {
                    "name": Path(source).name,
                    "source": source,
                    "size": int(metadata.get("file_size") or 0),
                    "upload_time": metadata.get("upload_time") or "",
                    "chunk_count": 0,
                    "content_chars": 0,
                    "file_type": metadata.get("file_type") or "",
                    "enabled": bool(metadata.get("enabled", True)),
                })

                info["chunk_count"] += 1
                info["content_chars"] += len(content or "")
                if not info["size"] and metadata.get("file_size"):
                    info["size"] = int(metadata.get("file_size") or 0)
                if not info["upload_time"] and metadata.get("upload_time"):
                    info["upload_time"] = metadata.get("upload_time")
                if not info["file_type"] and metadata.get("file_type"):
                    info["file_type"] = metadata.get("file_type")

            documents = list(grouped.values())
            documents.sort(key=lambda item: item.get("upload_time") or "", reverse=True)
            return documents
        except Exception as e:
            logger.error(f"列出知识库文档失败 {e}")
            raise RuntimeError(f"列出知识库文档失败 {e}") from e

    def delete_document(self, collection_name: str, source: str) -> bool:
        """Delete all chunks for one source document in the collection."""
        if not source:
            return False

        try:
            store = self._get_store(collection_name)
            raw = store._collection.get(include=["metadatas"])
            ids_to_delete = []

            for doc_id, metadata in zip(raw.get("ids") or [], raw.get("metadatas") or []):
                metadata = metadata or {}
                if metadata.get("source") == source:
                    ids_to_delete.append(doc_id)

            if not ids_to_delete:
                return False

            store._collection.delete(ids=ids_to_delete)
            self._persist_store_if_supported(store)
            self._invalidate_collection_cache(store)
            logger.info(f"已从知识库'{collection_name}' 删除文档 '{source}', 分块数 {len(ids_to_delete)}")
            return True
        except Exception as e:
            logger.error(f"删除文档失败: {e}")
            raise RuntimeError(f"删除文档失败: {e}") from e

    def set_document_enabled(self, collection_name: str, source: str, enabled: bool) -> bool:
        """Enable or disable a document (all its chunks) by toggling the enabled metadata field."""
        if not source:
            return False

        try:
            store = self._get_store(collection_name)
            raw = store._collection.get(include=["metadatas"])
            ids_to_update = []

            for doc_id, metadata in zip(raw.get("ids") or [], raw.get("metadatas") or []):
                metadata = metadata or {}
                if metadata.get("source") == source:
                    ids_to_update.append(doc_id)

            if not ids_to_update:
                return False

            store._collection.update(
                ids=ids_to_update,
                metadatas=[{"enabled": enabled}] * len(ids_to_update),
            )
            self._persist_store_if_supported(store)
            self._invalidate_collection_cache(store)
            action = "启用" if enabled else "禁用"
            logger.info(f"已{action}知识库'{collection_name}' 中文档 '{source}', 分块数 {len(ids_to_update)}")
            return True
        except Exception as e:
            logger.error(f"设置文档启用状态失败: {e}")
            raise RuntimeError(f"设置文档启用状态失败: {e}") from e

    def delete_documents(self, collection_name: str, sources: list) -> dict:
        """Batch delete multiple source documents in a single pass."""
        if not sources:
            return {"deleted_count": 0, "chunks_deleted": 0}

        try:
            store = self._get_store(collection_name)
            raw = store._collection.get(include=["metadatas"])
            sources_set = set(sources)
            ids_to_delete = []
            found_sources = set()

            for doc_id, metadata in zip(raw.get("ids") or [], raw.get("metadatas") or []):
                metadata = metadata or {}
                source = metadata.get("source")
                if source in sources_set:
                    ids_to_delete.append(doc_id)
                    found_sources.add(source)

            if not ids_to_delete:
                return {"deleted_count": 0, "chunks_deleted": 0}

            store._collection.delete(ids=ids_to_delete)
            self._persist_store_if_supported(store)
            self._invalidate_collection_cache(store)
            logger.info(
                f"已从知识库'{collection_name}' 批量删除 {len(found_sources)} 个文档, "
                f"分块数 {len(ids_to_delete)}"
            )
            return {"deleted_count": len(found_sources), "chunks_deleted": len(ids_to_delete)}
        except Exception as e:
            logger.error(f"批量删除文档失败: {e}")
            raise RuntimeError(f"批量删除文档失败: {e}") from e
