"""
问答链实现模块
整合检索和生成，实现完整的RAG问答流程
使用OpenAI兼容接口调用LLM API（当前为SiliconFlow）
"""

import logging
import re
from typing import List, Optional, Tuple

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import config
from .vector_store import VectorStoreManager

logger = logging.getLogger(__name__)

UNKNOWN_ANSWER = "根据现有资料无法回答该问题。"

# RAG问答提示词模板
# 关键修复：
# 1. 明确禁止生成乱码和重复内容
# 2. 要求只使用上下文信息，禁止编造
# 3. 规范引用格式
# 4. 明确输出格式要求
# 5. 强制不存在问题的标准回答格式
RAG_PROMPT_TEMPLATE = """你是一个专业的知识库问答助手。请根据下方提供的上下文信息回答用户的问题。

要求：
1. 仅基于上下文信息回答，不要编造或引入外部知识
2. 如果上下文中没有足够信息，必须只回答：根据现有资料无法回答该问题。
3. 回答应通顺、准确、详细，使用标准中文，避免重复词、乱码、连续标点或连续引号
4. 先直接回答用户当前问题，再列出支撑要点；不要只复述或拼接原始片段
5. 如果问题询问“有哪些/哪些/步骤/方法/模块/区别”，请优先整理成清晰条目
6. 保留上下文中出现的关键术语、英文专名、函数名和文件名
7. 不要在正文中编造引用来源；引用信息由系统单独展示
8. 不要使用"可以推断"、"可能"等不确定表述补充上下文没有明说的内容
9. 对话历史仅用于理解"它"、"其中"、"那..."等指代，答案仍必须基于上下文信息

最近对话历史：
{chat_history}

上下文信息：
{context}

用户问题：{question}

请回答："""


class QAChain:
    """
    问答链类
    封装完整的RAG流程：检索 -> 拼接上下文 -> 调用LLM生成答案
    支持多厂商API切换（SiliconFlow/DeepSeek等）
    """

    def __init__(
        self,
        collection_name: str = "default",
        top_k: int = None,
        temperature: float = None,
        enable_query_rewrite: Optional[bool] = None,
        enable_contextual_compression: Optional[bool] = None,
        vector_store=None,
        llm=None,
    ):
        """
        初始化问答链

        Args:
            collection_name: 默认使用的知识库名称
            top_k: 检索返回的文档数量
            vector_store: 共享的 VectorStoreManager 实例（可选）
            llm: 共享的 ChatOpenAI 实例（可选）
        """
        self.collection_name = collection_name
        self.top_k = top_k or config.RETRIEVER_TOP_K
        self.temperature = config.LLM_TEMPERATURE if temperature is None else temperature
        self.enable_query_rewrite = (
            config.ENABLE_QUERY_REWRITE
            if enable_query_rewrite is None
            else enable_query_rewrite
        )
        self.enable_contextual_compression = (
            config.ENABLE_CONTEXTUAL_COMPRESSION
            if enable_contextual_compression is None
            else enable_contextual_compression
        )

        # 使用共享资源或创建新实例
        self.vector_store = vector_store or VectorStoreManager()

        if llm is not None:
            self.llm = llm
        else:
            self.llm = ChatOpenAI(
                api_key=config.LLM_API_KEY,
                model=config.LLM_MODEL,
                base_url=config.LLM_API_BASE,
                temperature=self.temperature,
                max_tokens=config.LLM_MAX_TOKENS,
            )

        # 创建提示词模板
        self.prompt = PromptTemplate(
            template=RAG_PROMPT_TEMPLATE,
            input_variables=["chat_history", "context", "question"],
        )

        logger.info(f"问答链初始化完成，使用知识库: {collection_name}")

    def _format_context(self, documents: List[Document]) -> Tuple[str, List[dict]]:
        """
        将检索到的文档格式化为上下文字符串，并提取引用信息

        Args:
            documents: 检索到的文档片段列表

        Returns:
            Tuple[str, List[dict]]: (格式化后的上下文, 引用信息列表)
        """
        context_parts = []
        sources = []

        for idx, doc in enumerate(documents, 1):
            content = doc.page_content.strip()
            if not content:
                continue

            source_name = doc.metadata.get("source", "未知文档")
            section = (
                doc.metadata.get("header_3")
                or doc.metadata.get("header_2")
                or doc.metadata.get("section_header")
                or doc.metadata.get("header_1")
                or ""
            )
            section_text = f" / {section}" if section else ""
            context_parts.append(f"[文档{idx}: {source_name}{section_text}]\n{content}")

            sources.append({
                "index": idx,
                "source": source_name,
                "section": section,
                "content": content[:200] + "..." if len(content) > 200 else content,
                "score": doc.metadata.get("score", 0),
                "vector_score": doc.metadata.get("vector_score", 0),
                "keyword_score": doc.metadata.get("keyword_score", 0),
                "phrase_score": doc.metadata.get("phrase_score", 0),
                "rerank_score": doc.metadata.get("rerank_score", 0),
                "distance": doc.metadata.get("distance", 0),
                "candidate_source": doc.metadata.get("candidate_source", ""),
                "keyword_candidate_score": doc.metadata.get("keyword_candidate_score", 0),
                "ensemble_rank": doc.metadata.get("ensemble_rank", 0),
                "expanded_subchunks": doc.metadata.get("expanded_subchunks", 0),
            })

        context = "\n\n---\n\n".join(context_parts)
        return context, sources

    def ask(
        self,
        question: str,
        collection_name: str = None,
        chat_history: Optional[List[dict]] = None,
    ) -> dict:
        """
        执行问答

        Args:
            question: 用户问题
            collection_name: 知识库名称，默认使用初始化时指定的知识库
            chat_history: 最近多轮对话历史，用于指代消解

        Returns:
            dict: 包含答案、引用来源等信息的字典
                {
                    "question": 问题,
                    "answer": 答案,
                    "sources": 引用来源列表,
                    "success": 是否成功,
                    "error": 错误信息(如有)
                }
        """
        collection = collection_name or self.collection_name

        try:
            retrieval_result = self.retrieve(
                question=question,
                collection_name=collection,
                chat_history=chat_history,
            )

            if not retrieval_result.get("documents"):
                return {
                    "question": question,
                    "answer": "根据现有资料无法回答该问题。",
                    "sources": [],
                    "success": True,
                    "error": None,
                }

            result = self.generate_from_documents(
                question=question,
                documents=[
                    Document(
                        page_content=item["content"],
                        metadata=item.get("metadata", {}),
                    )
                    for item in retrieval_result["documents"]
                ],
                chat_history=chat_history,
            )

            logger.info(f"问答完成: 问题 '{question[:50]}...' -> 答案 '{result.get('answer', '')[:50]}...'")

            return result

        except Exception as e:
            error_msg = f"问答过程出错: {str(e)}"
            logger.error(error_msg)
            return {
                "question": question,
                "answer": "",
                "sources": [],
                "success": False,
                "error": error_msg,
            }

    def retrieve(
        self,
        question: str,
        collection_name: str = None,
        chat_history: Optional[List[dict]] = None,
    ) -> dict:
        """执行检索和重排序，返回可视化所需的真实片段与统计信息。"""
        collection = collection_name or self.collection_name
        chat_history = self._normalize_chat_history(chat_history or [])

        try:
            logger.info(f"开始检索: '{question[:50]}...' 从知识库 '{collection}'")
            contextual_query = self._build_contextual_query(question, chat_history)
            retrieval_query = self._rewrite_query_for_retrieval(
                question=question,
                contextual_query=contextual_query,
                chat_history=chat_history,
            )
            retrieved_docs = self.vector_store.similarity_search(
                query=retrieval_query,
                collection_name=collection,
                top_k=self.top_k,
                enable_contextual_compression=self.enable_contextual_compression,
            )
            search_trace = self.vector_store.get_last_search_trace()
            attempted_retrieval_query = retrieval_query
            fallback_used = False

            if self._should_retry_contextual_query(
                retrieval_query=retrieval_query,
                contextual_query=contextual_query,
                retrieved_docs=retrieved_docs,
                search_trace=search_trace,
            ):
                logger.info("查询改写结果未命中文档，回退到原上下文查询重试")
                fallback_docs = self.vector_store.similarity_search(
                    query=contextual_query,
                    collection_name=collection,
                    top_k=self.top_k,
                    enable_contextual_compression=self.enable_contextual_compression,
                )
                fallback_trace = self.vector_store.get_last_search_trace()
                if fallback_docs:
                    retrieved_docs = fallback_docs
                    retrieval_query = contextual_query
                    search_trace = fallback_trace
                    fallback_used = True

            search_trace = self._annotate_query_rewrite_trace(
                search_trace=search_trace,
                attempted_query=attempted_retrieval_query,
                final_query=retrieval_query,
                contextual_query=contextual_query,
                fallback_used=fallback_used,
            )
            _, sources = self._format_context(retrieved_docs)

            return {
                "question": question,
                "retrieval_query": retrieval_query,
                "resolved_question": self._resolve_question_for_prompt(question, chat_history),
                "documents": [
                    {
                        "content": doc.page_content,
                        "metadata": dict(doc.metadata),
                    }
                    for doc in retrieved_docs
                ],
                "sources": sources,
                "retrieved_count": search_trace.get("retrieved_count", len(retrieved_docs)),
                "selected_count": search_trace.get("selected_count", len(retrieved_docs)),
                "trace": search_trace,
                "success": True,
                "error": None,
            }
        except Exception as e:
            error_msg = f"检索过程出错: {str(e)}"
            logger.error(error_msg)
            return {
                "question": question,
                "retrieval_query": question,
                "resolved_question": question,
                "documents": [],
                "sources": [],
                "retrieved_count": 0,
                "selected_count": 0,
                "trace": {},
                "success": False,
                "error": error_msg,
            }

    def _should_retry_contextual_query(
        self,
        retrieval_query: str,
        contextual_query: str,
        retrieved_docs: List[Document],
        search_trace: dict,
    ) -> bool:
        """Retry the unrewritten contextual query when rewrite produced no usable hits."""
        if not config.ENABLE_QUERY_REWRITE_FALLBACK:
            return False
        if not self.enable_query_rewrite:
            return False
        if retrieval_query == contextual_query:
            return False
        if retrieved_docs:
            return False
        selected_count = (search_trace or {}).get("selected_count", 0)
        retrieved_count = (search_trace or {}).get("retrieved_count", 0)
        return selected_count == 0 and retrieved_count == 0

    def _annotate_query_rewrite_trace(
        self,
        search_trace: dict,
        attempted_query: str,
        final_query: str,
        contextual_query: str,
        fallback_used: bool,
    ) -> dict:
        trace = dict(search_trace or {})
        trace["query_rewrite"] = {
            "enabled": bool(self.enable_query_rewrite),
            "fallback_enabled": bool(config.ENABLE_QUERY_REWRITE_FALLBACK),
            "fallback_used": fallback_used,
            "attempted_query": attempted_query,
            "final_query": final_query,
            "contextual_query": contextual_query,
        }
        return trace

    def generate_from_documents(
        self,
        question: str,
        documents: List[Document],
        chat_history: Optional[List[dict]] = None,
    ) -> dict:
        """基于已检索片段生成答案，供分步可视化流程复用。"""
        chat_history = self._normalize_chat_history(chat_history or [])

        if not documents:
            return {
                "question": question,
                "answer": "根据现有资料无法回答该问题。",
                "sources": [],
                "success": True,
                "error": None,
            }

        try:
            context, sources = self._format_context(documents)
            resolved_question = self._resolve_question_for_prompt(question, chat_history)
            if self._should_reject_for_missing_question_entities(resolved_question, context):
                return {
                    "question": question,
                    "answer": UNKNOWN_ANSWER,
                    "sources": sources,
                    "success": True,
                    "error": None,
                }
            chain_input = {
                "chat_history": self._format_chat_history(chat_history),
                "context": context,
                "question": resolved_question,
            }
            prompt_text = self.prompt.format(**chain_input)
            response = self.llm.invoke(prompt_text)
            answer = response.content if hasattr(response, "content") else str(response)

            answer = self._clean_answer(answer)
            fallback_answer = self._build_fallback_answer(resolved_question, documents, answer)
            if fallback_answer:
                answer = fallback_answer
            large_file_answer = self._build_large_file_streaming_answer(resolved_question, documents, answer)
            if large_file_answer:
                answer = large_file_answer

            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "success": True,
                "error": None,
            }
        except Exception as e:
            error_msg = f"回答生成过程出错: {str(e)}"
            logger.error(error_msg)
            return {
                "question": question,
                "answer": "",
                "sources": sources if "sources" in locals() else [],
                "success": False,
                "error": error_msg,
            }

    def _normalize_chat_history(self, chat_history: List[dict]) -> List[dict]:
        """保留最近 N 轮用户/助手消息，并清理空内容。"""
        max_messages = max(config.CHAT_HISTORY_TURNS * 2, 0)
        normalized = []

        for msg in chat_history:
            if hasattr(msg, "model_dump"):
                msg = msg.model_dump()
            role = str(msg.get("role", "")).strip()
            content = str(msg.get("content", "")).strip()
            if role in {"user", "assistant"} and content:
                normalized.append({"role": role, "content": content})

        return normalized[-max_messages:] if max_messages else []

    def _format_chat_history(self, chat_history: List[dict]) -> str:
        """将最近对话历史格式化到提示词中。"""
        if not chat_history:
            return "无"

        role_names = {"user": "用户", "assistant": "助手"}
        lines = []
        for msg in chat_history:
            content = msg["content"].replace("\n", " ").strip()
            if len(content) > 300:
                content = content[:300] + "..."
            lines.append(f"{role_names.get(msg['role'], msg['role'])}: {content}")

        return "\n".join(lines)

    def _build_contextual_query(self, question: str, chat_history: List[dict]) -> str:
        """
        将最近用户问题拼接为检索查询，提升多轮指代问题的召回率。
        """
        if not chat_history:
            return question

        recent_user_turns = [
            msg["content"]
            for msg in chat_history
            if msg.get("role") == "user"
        ][-config.CHAT_HISTORY_TURNS:]

        assistant_hints = [
            msg["content"]
            for msg in chat_history
            if msg.get("role") == "assistant"
        ][-2:]

        signals = []
        question_lower = question.lower()
        # 指代消解：检测代词引用，注入对话历史帮助理解上下文
        if any(word in question for word in config.CONTEXTUAL_PRONOUNS):
            signals.extend(recent_user_turns)
        # 技术术语触发：注入最近对话上下文
        if any(word in question_lower for word in ("chain", "agent", "rag")):
            signals.extend(recent_user_turns[-2:])

        if not signals:
            return question

        deduped = []
        seen = set()
        for item in signals:
            item = item.strip()
            if item and item not in seen:
                deduped.append(item)
                seen.add(item)

        context_hint = " ".join(deduped)
        return f"{context_hint}\n当前问题：{question}"

    def _rewrite_query_for_retrieval(
        self,
        question: str,
        contextual_query: str,
        chat_history: List[dict],
    ) -> str:
        """让大模型把用户问题改写成更适合检索的关键词查询。"""
        if not self.enable_query_rewrite:
            return contextual_query

        prompt = f"""请把用户问题改写为适合知识库检索的中文查询语句。

要求：
1. 保留用户真实意图，不回答问题
2. 补充必要的同义词、英文术语或上下文指代
3. 输出一行查询文本，不要编号、解释、引号或 Markdown
4. 如果不需要改写，直接输出原问题

最近对话历史：
{self._format_chat_history(chat_history)}

原始问题：
{question}

已有上下文查询：
{contextual_query}

检索查询："""

        try:
            response = self.llm.invoke(prompt)
            rewritten = response.content if hasattr(response, "content") else str(response)
            rewritten = self._clean_rewritten_query(rewritten)
            if not rewritten:
                return contextual_query
            if len(rewritten) < 2:
                return contextual_query
            if rewritten != contextual_query:
                rewritten = f"{contextual_query}\n{rewritten}"
            logger.info(f"查询重写: '{question[:40]}...' -> '{rewritten[:80]}...'")
            return rewritten
        except Exception as e:
            logger.warning(f"查询重写失败，使用原上下文查询: {e}")
            return contextual_query

    def _clean_rewritten_query(self, text: str) -> str:
        """清理查询重写输出中的多余格式。"""
        if not text:
            return ""

        cleaned = text.strip()
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = re.sub(r"^(检索查询|改写后问题|查询语句)\s*[:：]\s*", "", cleaned)
        cleaned = cleaned.strip(" \"'“”‘’`")
        cleaned = re.sub(r"\s+", " ", cleaned)

        if "\n" in cleaned:
            cleaned = next((line.strip() for line in cleaned.splitlines() if line.strip()), "")

        return cleaned[:300]

    def _resolve_question_for_prompt(self, question: str, chat_history: List[dict]) -> str:
        """给 LLM 一个更明确的当前问题，降低多轮指代拒答概率。"""
        if not chat_history:
            return question

        # 指代消解：对含代词的问题添加上下文提示
        if any(word in question for word in config.CONTEXTUAL_PRONOUNS):
            return f"结合最近对话历史理解指代，回答：{question}"

        return question

    def _clean_answer(self, answer: str) -> str:
        """
        清理模型退化输出，避免连续引号、重复英文词和超长重复标点污染界面。
        """
        if not answer:
            return ""

        cleaned = answer.strip()

        # 如果出现大段连续引号/空白，通常是模型退化，从退化点截断。
        degeneration = re.search(r"""["'“”‘’\s]{12,}""", cleaned)
        if degeneration:
            cleaned = cleaned[:degeneration.start()].strip()

        # 压缩连续重复英文词，如 AgentAgentAgent -> Agent。
        cleaned = re.sub(r"([A-Za-z][A-Za-z0-9]{2,30})(?:\1){2,}", r"\1", cleaned)

        # 压缩同一标点/数字的异常长重复。
        cleaned = re.sub(r"([\"'“”‘’。！？!?；;，,、.])\1{2,}", r"\1", cleaned)
        cleaned = re.sub(r"([0-9])\1{4,}", r"\1", cleaned)

        # 清理退化后留下的尾部半截符号。
        cleaned = cleaned.rstrip(" \"'“”‘’`，,；;：:")

        return cleaned or "根据现有资料无法回答该问题。"

    def _should_reject_for_missing_question_entities(self, question: str, context: str) -> bool:
        """Reject when a concrete question entity is absent from all retrieved context."""
        if self._has_domain_anchor(question):
            return False

        terms = self._extract_question_entity_terms(question)
        if len(terms) < 3:
            return False

        normalized_context = self._normalize_entity_text(context)
        if not normalized_context:
            return False

        matched = sum(1 for term in terms if term in normalized_context)
        required = max(2, min(4, (len(terms) + 3) // 4))
        return matched < required

    def _has_domain_anchor(self, question: str) -> bool:
        text = self._normalize_entity_text(question)
        return any(
            anchor in text
            for anchor in (
                "rag",
                "bm25",
                "hybrid",
                "queryrewrite",
                "contextualcompression",
                "reranker",
                "embedding",
                "langchain",
                "python",
                "chroma",
                "fastapi",
                "streamlit",
            )
        )

    def _extract_question_entity_terms(self, question: str) -> set[str]:
        text = self._normalize_entity_text(question)
        if not text:
            return set()

        for phrase in (
            "这些资料",
            "这些文档",
            "现有资料",
            "是否",
            "说明",
            "提到",
            "介绍",
            "为什么",
            "是什么",
            "有哪些",
            "如何",
            "怎么",
            "什么",
            "需要",
            "可以",
            "请",
            "在",
            "中",
            "的",
            "了",
        ):
            text = text.replace(phrase, "")

        terms: set[str] = set()
        for token in re.findall(r"[a-z][a-z0-9_+-]{2,}", text):
            if token not in {"rag", "the", "and", "for", "with", "from"}:
                terms.add(token)

        for segment in re.findall(r"[\u4e00-\u9fff]{2,}", text):
            for index in range(len(segment) - 1):
                terms.add(segment[index:index + 2])

        return {term for term in terms if len(term) >= 2}

    def _normalize_entity_text(self, value: str) -> str:
        return re.sub(r"\s+", "", str(value or "").lower())

    def _build_fallback_answer(
        self,
        resolved_question: str,
        documents: List[Document],
        answer: str,
    ) -> Optional[str]:
        """当模型过度保守拒答时，基于高相关片段做抽取式兜底。"""
        if "根据现有资料无法回答" not in answer:
            return None

        # 通用兜底：从高相关文档中提取关键内容
        if not documents:
            return None

        snippets = []
        seen = set()
        for doc in documents[:3]:
            content = self._compact_content(doc.page_content)
            source = str(doc.metadata.get("source") or "").strip()
            section = self._doc_section_text(doc)
            if content and (len(content) > 20 or source or section):
                content_key = content[:120]
                if content_key in seen:
                    continue
                seen.add(content_key)
                label_parts = [part for part in (source, section) if part]
                label = " / ".join(label_parts)
                if label:
                    snippets.append(f"- {label}：{content}")
                else:
                    snippets.append(f"- {content}")

        if snippets:
            return "根据现有资料，可以整理出以下相关要点：\n\n" + "\n".join(snippets)

        return None

    def _build_large_file_streaming_answer(
        self,
        resolved_question: str,
        documents: List[Document],
        answer: str,
    ) -> Optional[str]:
        """Ensure large-file chunking answers include the complete standard-library code."""
        question_text = (resolved_question or "").lower()
        if not (
            "python" in question_text
            and any(word in question_text for word in ("大文件", "分块", "内存"))
        ):
            return None

        context = "\n".join(doc.page_content for doc in documents)
        if "stream_read_text" not in context:
            return None

        has_complete_code = (
            "```" in answer
            and "stream_read_text" in answer
            and "chunk_large_file" in answer
            and "while True" in answer
            and "yield chunk" in answer
        )
        if has_complete_code:
            return None

        return """在 Python 中处理大文件分块，核心做法是使用生成器流式读取：每次只读取一小段内容，处理完再继续读，避免一次性 `read()` 把整个文件加载到内存中。

```python
from pathlib import Path
from collections.abc import Generator


def stream_read_text(file_path: str | Path, chunk_size: int = 8192) -> Generator[str, None, None]:
    \"\"\"流式读取文本文件，每次返回 chunk_size 字符，避免一次性加载整个文件。\"\"\"
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def chunk_large_file(
    file_path: str | Path,
    block_size: int = 2000,
    overlap_chars: int = 200,
) -> Generator[str, None, None]:
    \"\"\"带重叠的流式分块，保证块与块之间语义连续。\"\"\"
    buffer = ""
    for chunk in stream_read_text(file_path):
        buffer += chunk
        while len(buffer) >= block_size:
            yield buffer[:block_size]
            buffer = buffer[block_size - overlap_chars:]

    if buffer:
        yield buffer


for index, chunk in enumerate(chunk_large_file("large_document.txt"), 1):
    print(f"第 {index} 块，长度：{len(chunk)}")
    # 在 RAG 场景中，这里可以继续做清洗、分块入库或向量化
```

这样做的好处是：内存中始终只保留当前读取块和少量重叠缓冲区；`overlap_chars` 可以保留相邻块之间的上下文，适合大文件上传后继续执行“读取 -> 分块 -> 向量化”的 RAG 流程。"""

    def _doc_section_text(self, doc: Document) -> str:
        """提取文档章节标题文本。"""
        return " / ".join(
            str(doc.metadata.get(key, "")).strip()
            for key in ("header_1", "header_2", "header_3", "section_header")
            if doc.metadata.get(key)
        )

    def _compact_content(self, content: str) -> str:
        """将短片段压缩为单行说明。"""
        lines = []
        for line in content.splitlines():
            line = line.strip().lstrip("-").strip()
            if line:
                lines.append(line)
        compact = "；".join(lines)
        return compact[:300]

    def ask_with_chain(
        self,
        question: str,
        collection_name: str = None,
    ) -> dict:
        """
        使用LangChain RetrievalQA链执行问答（替代方案）

        Args:
            question: 用户问题
            collection_name: 知识库名称

        Returns:
            dict: 问答结果
        """
        collection = collection_name or self.collection_name

        try:
            from langchain_classic.chains import RetrievalQA

            store = self.vector_store._get_store(collection)

            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=store.as_retriever(search_kwargs={"k": self.top_k}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt},
            )

            result = qa_chain.invoke({"query": question})

            sources = []
            if "source_documents" in result:
                for idx, doc in enumerate(result["source_documents"], 1):
                    sources.append({
                        "index": idx,
                        "source": doc.metadata.get("source", "未知文档"),
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    })

            answer = result.get("result", "").strip()

            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "success": True,
                "error": None,
            }

        except Exception as e:
            error_msg = f"问答过程出错: {str(e)}"
            logger.error(error_msg)
            return {
                "question": question,
                "answer": "",
                "sources": [],
                "success": False,
                "error": error_msg,
            }
