"""
BGE reranker based contextual compression utilities.

The primary path calls an OpenAI-compatible rerank endpoint, such as
SiliconFlow's BGE reranker service. If the remote reranker is unavailable,
the compressor falls back to a deterministic lexical scorer so retrieval
continues to work.
"""

import logging
import re
from typing import Iterable, List, Sequence, Tuple

import requests
from langchain_core.documents import Document
from langchain_core.documents.compressor import BaseDocumentCompressor

import config

logger = logging.getLogger(__name__)


class BGERerankSentenceCompressor(BaseDocumentCompressor):
    """Compress documents by BGE reranking and sentence extraction."""

    top_n: int = 3
    max_sentences_per_doc: int = 3
    min_score: float = 0.0
    api_key: str = ""
    api_base: str = ""
    model: str = ""
    timeout: int = 45

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks=None,
    ) -> Sequence[Document]:
        docs = [doc for doc in documents if (doc.page_content or "").strip()]
        if not docs:
            return []

        ranked_docs, method = self._rank_documents(query, docs, self.top_n)
        compressed_docs = []

        for doc, doc_score in ranked_docs:
            content = doc.page_content.strip()
            compressed_content = self._compress_content(query, content)
            if not compressed_content:
                continue

            metadata = dict(doc.metadata or {})
            metadata["rerank_score"] = round(float(doc_score), 4)
            metadata["compression_method"] = method
            metadata["original_content_chars"] = len(content)
            metadata["compressed_content_chars"] = len(compressed_content)
            metadata["score"] = round(
                max(float(metadata.get("score") or 0), float(doc_score)),
                4,
            )
            compressed_docs.append(
                Document(page_content=compressed_content, metadata=metadata)
            )

        return compressed_docs[: self.top_n]

    def _rank_documents(
        self,
        query: str,
        documents: Sequence[Document],
        top_n: int,
    ) -> Tuple[List[Tuple[Document, float]], str]:
        texts = [doc.page_content for doc in documents]
        api_scores = self._call_rerank_api(query, texts, min(top_n, len(texts)))
        if api_scores:
            ranked = [
                (documents[index], score)
                for index, score in api_scores
                if 0 <= index < len(documents) and score >= self.min_score
            ]
            return ranked[:top_n], "bge-reranker"

        fallback = [
            (doc, self._lexical_score(query, doc.page_content))
            for doc in documents
        ]
        fallback.sort(key=lambda item: item[1], reverse=True)
        return fallback[:top_n], "lexical-fallback"

    def _compress_content(self, query: str, content: str) -> str:
        if self._looks_like_code(content):
            return content[: config.CONTEXTUAL_COMPRESSION_MAX_CHARS]

        sentences = self._split_sentences(content)
        if len(sentences) <= self.max_sentences_per_doc:
            return content[: config.CONTEXTUAL_COMPRESSION_MAX_CHARS]

        sentence_scores = self._call_rerank_api(
            query,
            sentences,
            min(self.max_sentences_per_doc, len(sentences)),
        )
        method = "api"
        if not sentence_scores:
            method = "fallback"
            sentence_scores = [
                (idx, self._lexical_score(query, sentence))
                for idx, sentence in enumerate(sentences)
            ]
            sentence_scores.sort(key=lambda item: item[1], reverse=True)

        selected_indexes = {
            index
            for index, score in sentence_scores[: self.max_sentences_per_doc]
            if score >= self.min_score or method == "fallback"
        }
        selected = [
            sentence
            for index, sentence in enumerate(sentences)
            if index in selected_indexes
        ]
        compressed = "\n".join(selected).strip()
        return compressed[: config.CONTEXTUAL_COMPRESSION_MAX_CHARS]

    def _call_rerank_api(
        self,
        query: str,
        texts: Sequence[str],
        top_n: int,
    ) -> List[Tuple[int, float]]:
        if not self.api_key or not self.api_base or not self.model or not texts:
            return []

        documents = [text[:4000] for text in texts if text and text.strip()]
        if not documents:
            return []

        url = f"{self.api_base.rstrip('/')}/rerank"
        payload = {
            "model": self.model,
            "query": query[:2000],
            "documents": documents,
            "top_n": max(1, min(top_n, len(documents))),
            "return_documents": False,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.warning(f"BGE reranker 调用失败，使用本地降级压缩: {e}")
            return []

        results = data.get("results") or data.get("data") or []
        parsed = []
        for item in results:
            if not isinstance(item, dict):
                continue
            index = item.get("index")
            score = (
                item.get("relevance_score")
                if item.get("relevance_score") is not None
                else item.get("score")
            )
            try:
                parsed.append((int(index), float(score)))
            except (TypeError, ValueError):
                continue

        parsed.sort(key=lambda item: item[1], reverse=True)
        return parsed

    def _split_sentences(self, text: str) -> List[str]:
        parts = re.split(r"(?<=[。！？!?；;])\s*|\n+", text)
        sentences = []
        for part in parts:
            part = part.strip()
            if part:
                sentences.append(part)
        return sentences or [text.strip()]

    def _looks_like_code(self, text: str) -> bool:
        code_markers = ("```", "def ", "class ", "import ", "return ", "{", "};")
        marker_hits = sum(1 for marker in code_markers if marker in text)
        return marker_hits >= 2

    def _lexical_score(self, query: str, text: str) -> float:
        terms = self._terms(query)
        if not terms:
            return 0.0

        text_lower = text.lower()
        matches = sum(1 for term in terms if term in text_lower)
        phrase_bonus = 0.35 if query.lower().strip() in text_lower else 0.0
        return min(1.0, matches / max(len(terms), 1) + phrase_bonus)

    def _terms(self, text: str) -> List[str]:
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_+#.-]*|[\u4e00-\u9fff]{2,}", text.lower())
        terms = []
        seen = set()
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            terms.append(token)
            if re.fullmatch(r"[\u4e00-\u9fff]{4,}", token):
                for idx in range(len(token) - 1):
                    gram = token[idx:idx + 2]
                    if gram not in seen:
                        seen.add(gram)
                        terms.append(gram)
        return terms


def create_bge_compressor(top_n: int) -> BGERerankSentenceCompressor:
    """Build the configured contextual compressor."""
    return BGERerankSentenceCompressor(
        top_n=top_n,
        max_sentences_per_doc=config.CONTEXTUAL_COMPRESSION_SENTENCES_PER_DOC,
        min_score=config.RERANKER_MIN_SCORE,
        api_key=config.LLM_API_KEY,
        api_base=config.RERANKER_API_BASE,
        model=config.RERANKER_MODEL,
        timeout=config.RERANKER_TIMEOUT,
    )
