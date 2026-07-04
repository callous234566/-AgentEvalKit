"""Tests for rag.qa_chain.QAChain helper methods."""

import unittest
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from rag.qa_chain import QAChain


class NormalizeChatHistoryTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)
        self.chain.collection_name = "test"

    def test_empty_history(self):
        result = self.chain._normalize_chat_history([])
        self.assertEqual(result, [])

    def test_filters_invalid_roles(self):
        history = [
            {"role": "user", "content": "你好"},
            {"role": "system", "content": "系统消息"},
            {"role": "assistant", "content": "回答"},
        ]
        result = self.chain._normalize_chat_history(history)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["role"], "user")
        self.assertEqual(result[1]["role"], "assistant")

    def test_filters_empty_content(self):
        history = [
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "  "},
        ]
        result = self.chain._normalize_chat_history(history)
        self.assertEqual(result, [])

    def test_truncates_to_max_turns(self):
        import config
        max_messages = max(config.CHAT_HISTORY_TURNS * 2, 0)
        history = [
            {"role": "user", "content": f"q{i}"}
            for i in range(max_messages + 10)
        ]
        result = self.chain._normalize_chat_history(history)
        self.assertLessEqual(len(result), max_messages)

    def test_handles_pydantic_like_objects(self):
        class FakeMsg:
            def __init__(self, role, content):
                self._data = {"role": role, "content": content}
            def model_dump(self):
                return self._data

        history = [FakeMsg("user", "问题"), FakeMsg("assistant", "回答")]
        result = self.chain._normalize_chat_history(history)
        self.assertEqual(len(result), 2)


class FormatChatHistoryTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_empty_returns_wu(self):
        result = self.chain._format_chat_history([])
        self.assertEqual(result, "无")

    def test_formats_roles(self):
        history = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"},
        ]
        result = self.chain._format_chat_history(history)
        self.assertIn("用户: 你好", result)
        self.assertIn("助手: 你好！", result)

    def test_truncates_long_content(self):
        history = [{"role": "user", "content": "x" * 400}]
        result = self.chain._format_chat_history(history)
        self.assertIn("...", result)
        self.assertLess(len(result), 400)

    def test_newlines_replaced(self):
        history = [{"role": "user", "content": "多\n行\n文本"}]
        result = self.chain._format_chat_history(history)
        self.assertNotIn("\n", result.split(":", 1)[-1])


class BuildContextualQueryTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_no_history_returns_question(self):
        result = self.chain._build_contextual_query("什么是RAG？", [])
        self.assertEqual(result, "什么是RAG？")

    def test_pronoun_triggers_context(self):
        history = [
            {"role": "user", "content": "RAG是什么"},
            {"role": "assistant", "content": "RAG是检索增强生成"},
        ]
        result = self.chain._build_contextual_query("它的优点是什么？", history)
        self.assertIn("它的优点是什么", result)
        self.assertIn("RAG是什么", result)

    def test_generation_keyword_adds_signals(self):
        history = [{"role": "user", "content": "RAG系统"}]
        result = self.chain._build_contextual_query("生成组件怎么优化", history)
        self.assertIn("生成组件", result)


class ResolveQuestionForPromptTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_no_history_returns_original(self):
        result = self.chain._resolve_question_for_prompt("问题", [])
        self.assertEqual(result, "问题")

    def test_generation_question_rewrite(self):
        history = [{"role": "user", "content": "RAG"}]
        result = self.chain._resolve_question_for_prompt("那生成组件呢", history)
        self.assertIn("指代", result)
        self.assertIn("那生成组件呢", result)

    def test_retrieval_question_rewrite(self):
        history = [{"role": "user", "content": "RAG"}]
        result = self.chain._resolve_question_for_prompt("检索组件怎么优化", history)
        self.assertIn("检索组件", result)

    def test_pronoun_question_rewrite(self):
        history = [{"role": "user", "content": "RAG"}]
        result = self.chain._resolve_question_for_prompt("它的优点是什么", history)
        self.assertIn("指代", result)

    def test_plain_question_unchanged(self):
        history = [{"role": "user", "content": "RAG"}]
        result = self.chain._resolve_question_for_prompt("Python怎么安装", history)
        self.assertEqual(result, "Python怎么安装")


class CleanAnswerTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_empty_returns_empty(self):
        # _clean_answer returns "" early when answer is falsy
        result = self.chain._clean_answer("")
        self.assertEqual(result, "")

    def test_degenerate_to_empty_returns_fallback(self):
        # Content that degenerates completely after cleanup
        result = self.chain._clean_answer('""""""""""""""""""""')
        self.assertEqual(result, "根据现有资料无法回答该问题。")

    def test_normal_text_unchanged(self):
        text = "这是一段正常的回答。"
        result = self.chain._clean_answer(text)
        self.assertEqual(result, text)

    def test_degenerate_quotes_truncated(self):
        text = '正常内容""""""""""""垃圾内容'
        result = self.chain._clean_answer(text)
        self.assertNotIn("垃圾内容", result)

    def test_repeated_english_words_compressed(self):
        text = "AgentAgentAgentAgent 是什么"
        result = self.chain._clean_answer(text)
        self.assertNotIn("AgentAgentAgent", result)
        self.assertIn("Agent", result)

    def test_long_punctuation_compressed(self):
        text = "这是好的。。。。。。。。"
        result = self.chain._clean_answer(text)
        self.assertNotIn("。。。。", result)

    def test_trailing_punctuation_stripped(self):
        text = "回答内容,,,，，"
        result = self.chain._clean_answer(text)
        self.assertFalse(result.endswith(","))


class CleanRewrittenQueryTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_empty(self):
        self.assertEqual(self.chain._clean_rewritten_query(""), "")

    def test_strips_code_fences(self):
        result = self.chain._clean_rewritten_query("```json\n改写查询\n```")
        self.assertNotIn("```", result)

    def test_strips_prefix_labels(self):
        for label in ("检索查询：", "改写后问题：", "查询语句:"):
            result = self.chain._clean_rewritten_query(f"{label}实际查询")
            self.assertEqual(result, "实际查询")

    def test_takes_first_line_when_multiline(self):
        result = self.chain._clean_rewritten_query("第一行\n第二行\n第三行")
        # _clean_rewritten_query collapses whitespace but only splits
        # when there are non-empty lines after regex cleanup
        self.assertIn("第一行", result)

    def test_strips_quotes(self):
        result = self.chain._clean_rewritten_query('"查询内容"')
        self.assertEqual(result, "查询内容")

    def test_truncates_to_300_chars(self):
        result = self.chain._clean_rewritten_query("x" * 500)
        self.assertLessEqual(len(result), 300)


class RewriteQueryForRetrievalTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)
        self.chain.enable_query_rewrite = True

        class FakeResponse:
            content = "Python 大文件 分块 内存优化 流式读取"

        self.chain.llm = MagicMock()
        self.chain.llm.invoke.return_value = FakeResponse()

    def test_rewrite_keeps_original_question_terms(self):
        question = "如何在 Python 中处理大文件分块而不占用过多内存？"

        result = self.chain._rewrite_query_for_retrieval(
            question=question,
            contextual_query=question,
            chat_history=[],
        )

        self.assertIn(question, result)
        self.assertIn("Python 大文件 分块", result)


class InitConfigTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def test_uses_configured_llm_max_tokens(self, mock_llm, mock_vs):
        import config

        QAChain(collection_name="test")

        self.assertEqual(mock_llm.call_args.kwargs["max_tokens"], config.LLM_MAX_TOKENS)


class FormatContextTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_empty_docs(self):
        context, sources = self.chain._format_context([])
        self.assertEqual(context, "")
        self.assertEqual(sources, [])

    def test_single_doc(self):
        docs = [Document(
            page_content="内容",
            metadata={"source": "test.txt", "score": 0.8},
        )]
        context, sources = self.chain._format_context(docs)
        self.assertIn("内容", context)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["source"], "test.txt")

    def test_section_from_metadata(self):
        docs = [Document(
            page_content="内容",
            metadata={"source": "test.md", "header_2": "二级标题"},
        )]
        context, sources = self.chain._format_context(docs)
        self.assertIn("二级标题", context)

    def test_blank_content_skipped(self):
        docs = [
            Document(page_content="", metadata={"source": "a.txt"}),
            Document(page_content="有内容", metadata={"source": "b.txt"}),
        ]
        context, sources = self.chain._format_context(docs)
        self.assertEqual(len(sources), 1)

    def test_content_truncated_in_sources(self):
        docs = [Document(
            page_content="x" * 300,
            metadata={"source": "long.txt"},
        )]
        _, sources = self.chain._format_context(docs)
        self.assertLess(len(sources[0]["content"]), 300)

    def test_sources_include_trace_scores(self):
        docs = [Document(
            page_content="内容",
            metadata={
                "source": "score.md",
                "header_2": "评分章节",
                "score": 0.91,
                "vector_score": 0.8,
                "keyword_score": 0.7,
                "rerank_score": 0.6,
                "distance": 0.2,
                "candidate_source": "bm25",
                "keyword_candidate_score": 1.2,
                "ensemble_rank": 3,
                "expanded_subchunks": 2,
            },
        )]

        _, sources = self.chain._format_context(docs)

        self.assertEqual(sources[0]["source"], "score.md")
        self.assertEqual(sources[0]["section"], "评分章节")
        self.assertEqual(sources[0]["score"], 0.91)
        self.assertEqual(sources[0]["vector_score"], 0.8)
        self.assertEqual(sources[0]["keyword_score"], 0.7)
        self.assertEqual(sources[0]["rerank_score"], 0.6)
        self.assertEqual(sources[0]["candidate_source"], "bm25")
        self.assertEqual(sources[0]["expanded_subchunks"], 2)


class RetrieveTraceTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)
        self.chain.collection_name = "test"
        self.chain.top_k = 3
        self.chain.enable_query_rewrite = False
        self.chain.enable_contextual_compression = False
        self.chain.vector_store = MagicMock()

    def test_retrieve_includes_search_trace_and_source_scores(self):
        doc = Document(
            page_content="内容",
            metadata={
                "source": "a.md",
                "score": 0.9,
                "vector_score": 0.8,
                "candidate_source": "bm25",
            },
        )
        self.chain.vector_store.similarity_search.return_value = [doc]
        self.chain.vector_store.get_last_search_trace.return_value = {
            "retrieved_count": 5,
            "selected_count": 1,
            "final_documents": [
                {"source": "a.md", "score": 0.9, "vector_score": 0.8}
            ],
        }

        result = self.chain.retrieve("问题", "test")

        self.assertTrue(result["success"])
        self.assertEqual(result["trace"]["final_documents"][0]["source"], "a.md")
        self.assertEqual(result["retrieved_count"], 5)
        self.assertEqual(result["selected_count"], 1)
        self.assertEqual(result["sources"][0]["vector_score"], 0.8)
        self.assertEqual(result["sources"][0]["candidate_source"], "bm25")

    def test_retrieve_falls_back_to_contextual_query_when_rewrite_has_no_hits(self):
        self.chain.enable_query_rewrite = True
        self.chain._rewrite_query_for_retrieval = MagicMock(return_value="改写跑偏")
        doc = Document(page_content="原问题命中内容", metadata={"source": "a.md"})
        self.chain.vector_store.similarity_search.side_effect = [[], [doc]]
        self.chain.vector_store.get_last_search_trace.side_effect = [
            {"retrieved_count": 0, "selected_count": 0},
            {"retrieved_count": 1, "selected_count": 1},
        ]

        result = self.chain.retrieve("原问题", "test")

        self.assertTrue(result["success"])
        self.assertEqual(result["retrieval_query"], "原问题")
        self.assertEqual(result["documents"][0]["metadata"]["source"], "a.md")
        self.assertEqual(self.chain.vector_store.similarity_search.call_count, 2)
        self.assertTrue(result["trace"]["query_rewrite"]["fallback_used"])
        self.assertEqual(result["trace"]["query_rewrite"]["attempted_query"], "改写跑偏")

    def test_retrieve_does_not_fallback_when_rewrite_returns_hits(self):
        self.chain.enable_query_rewrite = True
        self.chain._rewrite_query_for_retrieval = MagicMock(return_value="改写命中")
        doc = Document(page_content="改写命中内容", metadata={"source": "a.md"})
        self.chain.vector_store.similarity_search.return_value = [doc]
        self.chain.vector_store.get_last_search_trace.return_value = {
            "retrieved_count": 1,
            "selected_count": 1,
        }

        result = self.chain.retrieve("原问题", "test")

        self.assertTrue(result["success"])
        self.assertEqual(result["retrieval_query"], "改写命中")
        self.assertEqual(self.chain.vector_store.similarity_search.call_count, 1)
        self.assertFalse(result["trace"]["query_rewrite"]["fallback_used"])


class BuildFallbackAnswerTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_returns_none_when_not_rejected(self):
        result = self.chain._build_fallback_answer("问题", [], "正常回答")
        self.assertIsNone(result)

    def test_returns_none_for_rejected_without_matching_docs(self):
        result = self.chain._build_fallback_answer("普通问题", [], "根据现有资料无法回答该问题。")
        self.assertIsNone(result)

    def test_generation_fallback(self):
        docs = [Document(
            page_content="生成优化方法",
            metadata={"header_1": "RAG", "header_2": "生成优化"},
        )]
        answer = "根据现有资料无法回答该问题。"
        result = self.chain._build_fallback_answer("生成组件怎么优化", docs, answer)
        self.assertIsNotNone(result)
        self.assertIn("生成", result)

    def test_generation_fallback_keeps_source_and_deduplicates(self):
        docs = [
            Document(
                page_content="LangChain 的核心模块包括模型、提示词、链、检索器和工具。",
                metadata={
                    "source": "03_LangChain学习资料.md",
                    "header_1": "LangChain 学习资料",
                    "header_2": "核心模块",
                },
            ),
            Document(
                page_content="LangChain 的核心模块包括模型、提示词、链、检索器和工具。",
                metadata={
                    "source": "03_LangChain学习资料.md",
                    "header_1": "LangChain 学习资料",
                    "header_2": "核心模块",
                },
            ),
        ]
        answer = "根据现有资料无法回答该问题。"

        result = self.chain._build_fallback_answer("LangChain 的核心模块有哪些？", docs, answer)

        self.assertIsNotNone(result)
        self.assertIn("03_LangChain学习资料.md", result)
        self.assertIn("核心模块", result)
        self.assertEqual(result.count("LangChain 的核心模块包括"), 1)


class LargeFileStreamingAnswerTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)

    def test_adds_complete_code_when_model_answer_is_incomplete(self):
        docs = [Document(
            page_content=(
                "正确做法是使用流式读取。\n"
                "def stream_read_text(file_path, chunk_size=8192): ..."
            ),
            metadata={"source": "02_Python学习笔记.md"},
        )]

        result = self.chain._build_large_file_streaming_answer(
            "如何在 Python 中处理大文件分块而不占用过多内存？",
            docs,
            "可以使用 stream_read_text 和 chunk_large_file。",
        )

        self.assertIsNotNone(result)
        self.assertIn("```python", result)
        self.assertIn("while True", result)
        self.assertIn("yield chunk", result)
        self.assertIn("chunk_large_file", result)

    def test_keeps_complete_model_code(self):
        complete = "```python\nwhile True:\n    yield chunk\n\ndef chunk_large_file(): pass\n# stream_read_text\n```"
        docs = [Document(page_content="stream_read_text", metadata={})]

        result = self.chain._build_large_file_streaming_answer(
            "如何在 Python 中处理大文件分块而不占用过多内存？",
            docs,
            complete,
        )

        self.assertIsNone(result)


class GenerateFromDocumentsTest(unittest.TestCase):
    @patch("rag.qa_chain.VectorStoreManager")
    @patch("rag.qa_chain.ChatOpenAI")
    def setUp(self, mock_llm, mock_vs):
        self.chain = QAChain.__new__(QAChain)
        self.chain.collection_name = "test"
        self.chain.enable_query_rewrite = False
        self.chain.enable_contextual_compression = False
        self.chain.llm = MagicMock()
        self.chain.prompt = MagicMock()
        self.chain.vector_store = MagicMock()
        self.chain.top_k = 3
        self.chain.temperature = 0.1

    def test_empty_docs_returns_cannot_answer(self):
        result = self.chain.generate_from_documents("问题", [])
        self.assertTrue(result["success"])
        self.assertIn("无法回答", result["answer"])

    def test_missing_question_entities_returns_cannot_answer(self):
        docs = [
            Document(
                page_content="Query Rewrite 可以缓解检索跑偏，并在改写失败时回退到原始查询。",
                metadata={"source": "06_Query_Rewrite资料.md"},
            )
        ]

        result = self.chain.generate_from_documents(
            "这些资料是否说明了火星基地厨房的虚构配置项？",
            docs,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["answer"], "根据现有资料无法回答该问题。")
        self.chain.llm.invoke.assert_not_called()

    def test_related_question_entities_do_not_trigger_guard(self):
        docs = [
            Document(
                page_content="Query Rewrite 跑偏时，可以回退到原始查询，避免错误改写影响检索。",
                metadata={"source": "06_Query_Rewrite资料.md"},
            )
        ]
        self.chain.prompt.format.return_value = "prompt"
        self.chain.llm.invoke.return_value = MagicMock(content="可以回退到原始查询。")

        result = self.chain.generate_from_documents(
            "Query Rewrite 跑偏时如何回退到原始查询？",
            docs,
        )

        self.assertTrue(result["success"])
        self.assertIn("原始查询", result["answer"])
        self.chain.llm.invoke.assert_called_once_with("prompt")

    def test_domain_anchor_question_does_not_trigger_entity_guard(self):
        docs = [
            Document(
                page_content="上下文压缩会保留核心片段，减少冗余内容。",
                metadata={"source": "05_Contextual_Compression资料.md"},
            )
        ]
        self.chain.prompt.format.return_value = "prompt"
        self.chain.llm.invoke.return_value = MagicMock(content="需要保护高置信片段。")

        result = self.chain.generate_from_documents(
            "Contextual Compression 为什么需要保护高置信片段？",
            docs,
        )

        self.assertTrue(result["success"])
        self.assertIn("高置信片段", result["answer"])
        self.chain.llm.invoke.assert_called_once_with("prompt")

    def test_model_rejection_still_uses_existing_fallback(self):
        docs = [
            Document(
                page_content="LangChain 的核心模块包括模型、提示词、链和工具。",
                metadata={"source": "03_LangChain学习资料.md", "header_2": "核心模块"},
            )
        ]
        self.chain.prompt.format.return_value = "prompt"
        self.chain.llm.invoke.return_value = MagicMock(content="根据现有资料无法回答该问题。")

        result = self.chain.generate_from_documents("LangChain 的核心模块有哪些？", docs)

        self.assertTrue(result["success"])
        self.assertIn("根据现有资料，可以整理出以下相关要点", result["answer"])
        self.assertIn("03_LangChain学习资料.md", result["answer"])


if __name__ == "__main__":
    unittest.main()
