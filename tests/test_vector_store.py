"""Tests for rag.vector_store pure functions and helpers."""

import unittest
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

import rag.vector_store as vector_store_module
from rag.vector_store import (
    EMBEDDING_SAFE_MAX_CHARS,
    EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS,
    sanitize_collection_name,
    VectorStoreManager,
)


class EmbeddingModelCompatibilityTest(unittest.TestCase):
    def tearDown(self):
        vector_store_module._embedding_model = None

    def test_siliconflow_embedding_keeps_raw_text_inputs(self):
        vector_store_module._embedding_model = None
        with patch("langchain_openai.OpenAIEmbeddings") as embedding_cls:
            model = vector_store_module.get_embedding_model()

        self.assertIs(model, embedding_cls.return_value)
        self.assertFalse(embedding_cls.call_args.kwargs["check_embedding_ctx_length"])


class SanitizeCollectionNameTest(unittest.TestCase):
    def test_english_name_unchanged(self):
        self.assertEqual(sanitize_collection_name("my-collection"), "my-collection")

    def test_dotted_name_unchanged(self):
        self.assertEqual(sanitize_collection_name("my.collection.name"), "my.collection.name")

    def test_chinese_name_hashes(self):
        result = sanitize_collection_name("我的知识库")
        self.assertTrue(result.startswith("kb_"))
        self.assertEqual(len(result), 19)  # "kb_" + 16 hex chars

    def test_hash_is_deterministic(self):
        a = sanitize_collection_name("测试")
        b = sanitize_collection_name("测试")
        self.assertEqual(a, b)

    def test_different_names_different_hashes(self):
        a = sanitize_collection_name("知识库A")
        b = sanitize_collection_name("知识库B")
        self.assertNotEqual(a, b)

    def test_single_char_name_hashes(self):
        result = sanitize_collection_name("a")
        # Single char fails the regex check (needs 3+ chars), so it hashes
        self.assertTrue(result.startswith("kb_") or result == "a")

    def test_alphanumeric_three_plus_unchanged(self):
        self.assertEqual(sanitize_collection_name("abc123"), "abc123")


class SplitTextByCharsTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_short_text_unchanged(self):
        result = self.manager._split_text_by_chars("短文本", max_chars=100, overlap=10)
        self.assertEqual(result, ["短文本"])

    def test_long_text_splits(self):
        text = "。".join([f"句子{i}" for i in range(20)])
        result = self.manager._split_text_by_chars(text, max_chars=30, overlap=5)
        self.assertGreater(len(result), 1)
        for part in result:
            self.assertLessEqual(len(part), 30 + 20)  # allow some margin for separator

    def test_empty_text(self):
        result = self.manager._split_text_by_chars("", max_chars=100, overlap=10)
        # Empty text produces an empty-string part (the strip() yields "")
        self.assertEqual(result, [""])


class SplitOversizedDocumentsTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_short_docs_unchanged(self):
        docs = [Document(page_content="短", metadata={"chunk_index": 0})]
        result = self.manager._split_oversized_documents(docs)
        self.assertEqual(len(result), 1)

    def test_long_doc_splits(self):
        long_text = "测试内容。" * 100
        doc = Document(page_content=long_text, metadata={"chunk_index": 0})
        result = self.manager._split_oversized_documents([doc])
        self.assertGreater(len(result), 1)
        for d in result:
            self.assertIn("parent_chunk_index", d.metadata)
            self.assertIn("sub_chunk_index", d.metadata)

    def test_preserves_original_metadata(self):
        long_text = "x" * 500
        doc = Document(page_content=long_text, metadata={"chunk_index": 5, "source": "test.txt"})
        result = self.manager._split_oversized_documents([doc])
        for d in result:
            self.assertEqual(d.metadata.get("source"), "test.txt")
            self.assertEqual(d.metadata.get("parent_chunk_index"), 5)

    def test_dense_code_like_text_is_split_conservatively(self):
        dense_text = "(".join(["lambda x: x['value'] + 1;" for _ in range(80)])
        doc = Document(page_content=dense_text, metadata={"chunk_index": 2, "source": "code.md"})
        result = self.manager._split_oversized_documents([doc])

        self.assertGreater(len(result), 1)
        for d in result:
            self.assertLessEqual(len(d.page_content), EMBEDDING_SAFE_MAX_CHARS)
            self.assertLessEqual(
                self.manager._estimate_embedding_tokens(d.page_content),
                EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS,
            )

    def test_dense_non_ascii_text_is_recursively_split(self):
        dense_text = "🚀" * 1000
        doc = Document(page_content=dense_text, metadata={"chunk_index": 3, "source": "emoji.md"})
        result = self.manager._split_oversized_documents([doc])

        self.assertGreater(len(result), 1)
        for d in result:
            self.assertLessEqual(len(d.page_content), EMBEDDING_SAFE_MAX_CHARS)
            self.assertLessEqual(
                self.manager._estimate_embedding_tokens(d.page_content),
                EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS,
            )

    def test_embedding_token_estimate_overcounts_punctuation(self):
        plain = self.manager._estimate_embedding_tokens("simple english sentence")
        dense = self.manager._estimate_embedding_tokens("[]{}()::==!!,,..")

        self.assertGreater(dense, plain)


class FakeCollection:
    def __init__(self):
        self.deleted_ids = []

    def get(self, include=None):
        return {
            "ids": ["old-1", "new-1", "new-2"],
            "metadatas": [
                {"ingest_batch_id": "old"},
                {"ingest_batch_id": "batch-1"},
                {"ingest_batch_id": "batch-1"},
            ],
        }

    def delete(self, ids):
        self.deleted_ids.extend(ids)


class FakeStore:
    def __init__(self):
        self._collection = FakeCollection()
        self.persisted = False

    def persist(self):
        self.persisted = True


class ModernChromaLikeStore(FakeStore):
    __module__ = "langchain_chroma.vectorstores"


class TokenLimitRetryStore:
    def __init__(self, fail_when):
        self.fail_when = fail_when
        self.calls = []
        self.successful = []

    def add_documents(self, documents):
        self.calls.append(list(documents))
        if self.fail_when(documents):
            raise RuntimeError("Error code: 413 - input must have less than 512 tokens")
        self.successful.extend(documents)


class RollbackIngestBatchTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)
        self.manager._collection_cache = {}

    def test_rollback_deletes_only_current_batch(self):
        store = FakeStore()

        deleted = self.manager._rollback_ingest_batch(store, "test", "batch-1")

        self.assertEqual(deleted, 2)
        self.assertEqual(store._collection.deleted_ids, ["new-1", "new-2"])
        self.assertTrue(store.persisted)

    def test_persist_helper_keeps_legacy_store_compatibility(self):
        store = FakeStore()

        persisted = self.manager._persist_store_if_supported(store)

        self.assertTrue(persisted)
        self.assertTrue(store.persisted)

    def test_persist_helper_skips_modern_chroma_store(self):
        store = ModernChromaLikeStore()

        persisted = self.manager._persist_store_if_supported(store)

        self.assertFalse(persisted)
        self.assertFalse(store.persisted)


class EmbeddingRetryTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_token_limit_batch_is_retried_as_smaller_batches(self):
        store = TokenLimitRetryStore(fail_when=lambda docs: len(docs) > 1)
        docs = [
            Document(page_content="short one", metadata={"source": "a.md"}),
            Document(page_content="short two", metadata={"source": "a.md"}),
        ]

        self.manager._add_documents_with_embedding_retry(store, docs)

        self.assertEqual([len(call) for call in store.calls], [2, 1, 1])

    def test_token_limit_single_chunk_is_split_and_retried(self):
        def fail_when(docs):
            return any(len(doc.page_content) > 60 for doc in docs)

        store = TokenLimitRetryStore(fail_when=fail_when)
        doc = Document(page_content="A" * 140, metadata={"source": "long.md", "chunk_index": 7})

        self.manager._add_documents_with_embedding_retry(store, [doc])

        self.assertGreater(len(store.successful), 1)
        for split_doc in store.successful:
            self.assertTrue(split_doc.metadata.get("embedding_retry_split"))
            self.assertEqual(split_doc.metadata.get("parent_chunk_index"), 7)
            self.assertLessEqual(len(split_doc.page_content), 60)

    def test_non_token_limit_error_is_not_retried(self):
        class BrokenStore:
            def __init__(self):
                self.calls = 0

            def add_documents(self, documents):
                self.calls += 1
                raise RuntimeError("network unavailable")

        store = BrokenStore()

        with self.assertRaises(RuntimeError):
            self.manager._add_documents_with_embedding_retry(
                store,
                [Document(page_content="short", metadata={})],
            )

        self.assertEqual(store.calls, 1)


class DocumentsFromVectorScoresTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_basic_conversion(self):
        docs_and_scores = [
            (Document(page_content="doc1", metadata={"source": "a.txt"}), 0.5),
            (Document(page_content="doc2", metadata={}), 0.3),
        ]
        result = self.manager._documents_from_vector_scores(docs_and_scores)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].metadata["candidate_source"], "vector")
        self.assertAlmostEqual(result[0].metadata["distance"], 0.5)
        self.assertAlmostEqual(result[1].metadata["distance"], 0.3)


class DocumentsToPseudoScoresTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_generates_pseudo_distances(self):
        docs = [
            Document(page_content="a", metadata={}),
            Document(page_content="b", metadata={}),
        ]
        result = self.manager._documents_to_pseudo_scores(docs)
        self.assertEqual(len(result), 2)
        for doc, distance in result:
            self.assertIsInstance(distance, float)
            self.assertGreaterEqual(distance, 0)
        # First doc should have lower (better) pseudo distance
        self.assertLessEqual(result[0][1], result[1][1])

    def test_preserves_existing_distance(self):
        docs = [Document(page_content="a", metadata={"distance": 0.1})]
        result = self.manager._documents_to_pseudo_scores(docs)
        self.assertAlmostEqual(result[0][1], 0.1)


class ExtractQueryTermsTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_chinese_terms(self):
        terms = self.manager._extract_query_terms("机器学习算法")
        self.assertIn("机器", terms)
        self.assertIn("学习", terms)

    def test_english_terms(self):
        terms = self.manager._extract_query_terms("python code")
        self.assertIn("python", terms)
        self.assertIn("code", terms)

    def test_stopwords_excluded(self):
        terms = self.manager._extract_query_terms("什么是主要的")
        self.assertNotIn("什么", terms)
        self.assertNotIn("主要", terms)

    def test_chain_keyword_expansion(self):
        terms = self.manager._extract_query_terms("chain 使用方法")
        self.assertIn("chain", terms)
        self.assertIn("chains", terms)

    def test_agent_keyword_expansion(self):
        terms = self.manager._extract_query_terms("agent 智能体")
        self.assertIn("agent", terms)
        self.assertIn("智能体", terms)

    def test_rag_keyword_expansion(self):
        terms = self.manager._extract_query_terms("rag 检索生成")
        self.assertIn("rag", terms)
        self.assertIn("检索", terms)

    def test_empty_query_returns_query(self):
        terms = self.manager._extract_query_terms("")
        self.assertIn("", terms)


class DeleteCollectionTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)
        self.manager.db_path = "unused"
        self.manager._stores = {}
        self.manager._name_mapping = {"项目知识库": "kb_deleted"}
        self.manager._collection_cache = {}
        self.manager._save_name_mapping = MagicMock()

    def test_delete_collection_treats_chroma_deleted_state_as_success(self):
        store = MagicMock()
        store.delete_collection.side_effect = RuntimeError(
            "Chroma collection not initialized. Use `reset_collection` to re-create and initialize the collection."
        )
        self.manager._stores["项目知识库"] = store
        self.manager._get_store = MagicMock(return_value=store)
        self.manager._collection_exists = MagicMock(return_value=False)

        result = self.manager.delete_collection("项目知识库")

        self.assertTrue(result)
        self.assertNotIn("项目知识库", self.manager._stores)
        self.assertNotIn("项目知识库", self.manager._name_mapping)
        self.manager._save_name_mapping.assert_called_once()

    def test_delete_collection_keeps_real_failures_as_failure(self):
        store = MagicMock()
        store.delete_collection.side_effect = RuntimeError("permission denied")
        self.manager._stores["项目知识库"] = store
        self.manager._get_store = MagicMock(return_value=store)

        result = self.manager.delete_collection("项目知识库")

        self.assertFalse(result)
        self.assertIn("项目知识库", self.manager._stores)
        self.assertIn("项目知识库", self.manager._name_mapping)


    def test_collection_exists_supports_chroma_name_strings(self):
        collection_name = next(iter(self.manager._name_mapping))
        client = MagicMock()
        client.list_collections.return_value = ["other_collection", "kb_deleted"]

        with patch("chromadb.PersistentClient", return_value=client):
            self.assertTrue(self.manager._collection_exists(collection_name))

        client.list_collections.return_value = ["other_collection"]
        with patch("chromadb.PersistentClient", return_value=client):
            self.assertFalse(self.manager._collection_exists(collection_name))

    def test_delete_collection_treats_missing_collection_error_as_success(self):
        collection_name = next(iter(self.manager._name_mapping))
        store = MagicMock()
        store.delete_collection.side_effect = RuntimeError("Collection kb_deleted does not exist")
        self.manager._stores[collection_name] = store
        self.manager._get_store = MagicMock(return_value=store)

        client = MagicMock()
        client.list_collections.return_value = ["other_collection"]
        with patch("chromadb.PersistentClient", return_value=client):
            result = self.manager.delete_collection(collection_name)

        self.assertTrue(result)
        self.assertNotIn(collection_name, self.manager._stores)
        self.assertNotIn(collection_name, self.manager._name_mapping)

    def test_delete_collection_ignores_deleted_store_cache_key_failure(self):
        collection_name = next(iter(self.manager._name_mapping))
        store = MagicMock()
        self.manager._stores[collection_name] = store
        self.manager._get_store = MagicMock(return_value=store)
        self.manager._collection_cache = {"kb_deleted": ["cached"]}
        self.manager._collection_cache_key = MagicMock(
            side_effect=ValueError(
                "Chroma collection not initialized. Use `reset_collection` to re-create and initialize the collection."
            )
        )

        result = self.manager.delete_collection(collection_name)

        self.assertTrue(result)
        self.assertEqual(self.manager._collection_cache, {})
        self.assertNotIn(collection_name, self.manager._stores)
        self.assertNotIn(collection_name, self.manager._name_mapping)


class TokenizeForBm25Test(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_chinese_tokenization(self):
        tokens = self.manager._tokenize_for_bm25("机器学习算法简介")
        self.assertIn("机器", tokens)
        self.assertIn("学习", tokens)

    def test_english_tokenization(self):
        tokens = self.manager._tokenize_for_bm25("python_function test-var")
        self.assertIn("python_function", tokens)
        self.assertIn("test-var", tokens)

    def test_stopwords_filtered(self):
        tokens = self.manager._tokenize_for_bm25("什么是主要的")
        self.assertNotIn("什么", tokens)
        self.assertNotIn("主要", tokens)

    def test_fallback_on_pure_stopwords(self):
        tokens = self.manager._tokenize_for_bm25("什么")
        self.assertTrue(len(tokens) > 0)


class RerankResultsTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_empty_input(self):
        result = self.manager._rerank_results("query", [], 5)
        self.assertEqual(result, [])

    def test_deduplication(self):
        docs_and_scores = [
            (Document(page_content="相同内容", metadata={}), 0.5),
            (Document(page_content="相同内容", metadata={}), 0.3),
        ]
        result = self.manager._rerank_results("query", docs_and_scores, 5)
        self.assertEqual(len(result), 1)

    def test_deduplicates_same_source_section(self):
        docs_and_scores = [
            (
                Document(
                    page_content="第一段 LangChain RAG 自定义链路",
                    metadata={
                        "source": "03_LangChain学习资料.md",
                        "header_1": "LangChain 学习资料",
                        "header_2": "8.2 自定义 RAG 链路实现",
                    },
                ),
                0.1,
            ),
            (
                Document(
                    page_content="第二段 LangChain RAG 自定义链路",
                    metadata={
                        "source": "03_LangChain学习资料.md",
                        "header_1": "LangChain 学习资料",
                        "header_2": "8.2 自定义 RAG 链路实现",
                    },
                ),
                0.2,
            ),
            (
                Document(
                    page_content="LangChain LCEL 表达式语言",
                    metadata={
                        "source": "03_LangChain学习资料.md",
                        "header_1": "LangChain 学习资料",
                        "header_2": "8.2 自定义 RAG 链路实现",
                        "header_3": "8.2.2 LCEL",
                    },
                ),
                0.3,
            ),
        ]

        result = self.manager._rerank_results("LangChain RAG 链路", docs_and_scores, 5)

        sections = [
            " / ".join(
                str(doc.metadata.get(key, ""))
                for key in ("header_1", "header_2", "header_3")
                if doc.metadata.get(key)
            )
            for doc in result
        ]
        self.assertEqual(len(result), 2)
        self.assertIn("LangChain 学习资料 / 8.2 自定义 RAG 链路实现", sections)
        self.assertIn("LangChain 学习资料 / 8.2 自定义 RAG 链路实现 / 8.2.2 LCEL", sections)

    def test_score_metadata_added(self):
        docs_and_scores = [
            (Document(page_content="文档内容", metadata={"source": "a.txt"}), 0.5),
        ]
        result = self.manager._rerank_results("文档", docs_and_scores, 5)
        self.assertEqual(len(result), 1)
        self.assertIn("score", result[0].metadata)
        self.assertIn("vector_score", result[0].metadata)
        self.assertIn("keyword_score", result[0].metadata)
        self.assertIn("phrase_score", result[0].metadata)

    def test_metadata_match_contributes_phrase_score(self):
        docs_and_scores = [
            (
                Document(
                    page_content="正文只提到一些实现细节。",
                    metadata={"source": "guide.md", "header_2": "LangChain 核心模块"},
                ),
                0.9,
            )
        ]

        result = self.manager._rerank_results("LangChain 的核心模块有哪些？", docs_and_scores, 5)

        self.assertEqual(len(result), 1)
        self.assertGreater(result[0].metadata["phrase_score"], 0)

    def test_metadata_match_does_not_boost_loose_term_overlap(self):
        docs_and_scores = [
            (
                Document(
                    page_content="上下文压缩可以过滤长上下文。",
                    metadata={"source": "03_LangChain学习资料.md", "header_2": "上下文压缩"},
                ),
                0.9,
            )
        ]

        result = self.manager._rerank_results("LangChain 的核心模块有哪些？", docs_and_scores, 5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].metadata["phrase_score"], 0.0)

    def test_single_english_term_does_not_boost_metadata_phrase(self):
        docs_and_scores = [
            (
                Document(
                    page_content="介绍 LangChain 的普通章节。",
                    metadata={"source": "03_LangChain学习资料.md", "header_2": "应用实例"},
                ),
                0.9,
            )
        ]

        result = self.manager._rerank_results("LangChain", docs_and_scores, 5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].metadata["phrase_score"], 0.0)

    def test_rewrite_extra_line_does_not_drive_phrase_score(self):
        query = "LangChain 的核心模块有哪些？\nLangChain 相关信息和应用实例"
        docs_and_scores = [
            (
                Document(
                    page_content="这里是 LangChain 相关信息和应用实例。",
                    metadata={"source": "examples.md", "header_2": "应用实例"},
                ),
                0.9,
            )
        ]

        result = self.manager._rerank_results(query, docs_and_scores, 5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].metadata["phrase_score"], 0.0)

    def test_keyword_candidate_score_keeps_exact_title_match(self):
        docs_and_scores = [
            (
                Document(
                    page_content=(
                        "#### 问题一：如何在 Python 中处理大文件分块而不占用过多内存？\n"
                        "正确做法是使用流式读取，逐块读取文件内容。"
                    ),
                    metadata={
                        "source": "02_Python学习笔记.md",
                        "keyword_candidate_score": 1.85,
                    },
                ),
                2.5,
            ),
        ]

        result = self.manager._rerank_results(
            "如何在 Python 中处理大文件分块而不占用过多内存？",
            docs_and_scores,
            5,
        )

        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(result[0].metadata["keyword_score"], 1.0)
        self.assertGreater(result[0].metadata["score"], 0.35)

    def test_multiline_rewrite_phrase_boosts_original_question_match(self):
        query = (
            "如何在 Python 中处理大文件分块而不占用过多内存？\n"
            "Python 大文件处理 文件处理 分块读取"
        )
        docs_and_scores = [
            (
                Document(
                    page_content="文件读取、文件写入、JSON 文件处理、CSV 文件处理。",
                    metadata={"source": "general.md", "keyword_candidate_score": 1.2},
                ),
                0.15,
            ),
            (
                Document(
                    page_content=(
                        "#### 问题一：如何在 Python 中处理大文件分块而不占用过多内存？\n"
                        "正确做法是使用流式读取。"
                    ),
                    metadata={"source": "target.md", "keyword_candidate_score": 1.2},
                ),
                0.15,
            ),
        ]

        result = self.manager._rerank_results(query, docs_and_scores, 5)

        self.assertEqual(result[0].metadata["source"], "target.md")

    def test_large_file_streaming_markers_outrank_generic_file_parser(self):
        query = "如何在 Python 中处理大文件分块而不占用过多内存？"
        docs_and_scores = [
            (
                Document(
                    page_content="RAG 场景：将 PDF 文档解析为纯文本后分块入库。file_path Path read",
                    metadata={"source": "parser.md", "keyword_candidate_score": 1.8},
                ),
                0.15,
            ),
            (
                Document(
                    page_content=(
                        "正确做法是使用流式读取和逐块读取，避免 OOM。\n"
                        "def stream_read_text(file_path, chunk_size=8192): ..."
                    ),
                    metadata={"source": "stream.md", "keyword_candidate_score": 2.4},
                ),
                0.4,
            ),
        ]

        result = self.manager._rerank_results(query, docs_and_scores, 5)

        self.assertEqual(result[0].metadata["source"], "stream.md")


class ConfigurableRetrievalTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    @patch("rag.vector_store.config.RETRIEVER_INITIAL_K_MULTIPLIER", 8)
    @patch("rag.vector_store.config.RETRIEVER_INITIAL_K_MIN", 30)
    @patch("rag.vector_store.config.RETRIEVER_RERANK_K_MULTIPLIER", 5)
    def test_candidate_counts_use_configured_multipliers(self):
        self.assertEqual(self.manager._initial_candidate_count(3), 30)
        self.assertEqual(self.manager._initial_candidate_count(5), 40)
        self.assertEqual(self.manager._rerank_candidate_count(3), 15)

    @patch("rag.vector_store.config.RETRIEVER_MIN_SCORE", 0.0)
    @patch("rag.vector_store.config.RERANK_VECTOR_WEIGHT", 0.1)
    @patch("rag.vector_store.config.RERANK_KEYWORD_WEIGHT", 0.8)
    @patch("rag.vector_store.config.RERANK_PHRASE_WEIGHT", 0.1)
    def test_rerank_score_uses_configured_weights(self):
        docs_and_scores = [
            (Document(page_content="alpha beta gamma", metadata={"source": "a.md"}), 1.0),
        ]

        result = self.manager._rerank_results("alpha beta gamma", docs_and_scores, 1)

        self.assertEqual(result[0].metadata["score"], 0.95)
        self.assertEqual(result[0].metadata["vector_score"], 0.5)
        self.assertEqual(result[0].metadata["keyword_score"], 1.0)

    @patch("rag.vector_store.config.KEYWORD_HEADER_WEIGHT", 2.0)
    @patch("rag.vector_store.config.KEYWORD_PHRASE_WEIGHT", 3.0)
    @patch("rag.vector_store.config.KEYWORD_PSEUDO_DISTANCE_FLOOR", 0.2)
    @patch("rag.vector_store.config.KEYWORD_PSEUDO_DISTANCE_MAX_SCORE", 0.9)
    def test_keyword_search_uses_configured_weights(self):
        self.manager._get_cached_collection_snapshot = MagicMock(return_value={
            "raw_pairs": [
                ("alpha beta gamma", {"source": "a.md", "header_2": "alpha"}),
            ]
        })

        result = self.manager._keyword_search(MagicMock(), "alpha beta gamma", 1)

        doc, distance = result[0]
        self.assertEqual(doc.metadata["keyword_candidate_score"], 6.0)
        self.assertEqual(distance, 0.2)


class ContextualCompressionProtectionTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    @patch("rag.vector_store.config.ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION", True)
    @patch("rag.vector_store.config.CONTEXTUAL_COMPRESSION_PROTECT_TOP_N", 1)
    @patch("rag.vector_store.config.CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE", 0.7)
    def test_protect_compressed_results_keeps_high_confidence_baseline_doc(self):
        baseline = [
            Document(page_content="高置信内容", metadata={"source": "a.md", "score": 0.9}),
            Document(page_content="普通内容", metadata={"source": "b.md", "score": 0.4}),
        ]
        compressed = [
            Document(page_content="压缩内容", metadata={"source": "c.md", "score": 0.8}),
        ]

        result, protected_count = self.manager._protect_compressed_results(
            baseline_docs=baseline,
            compressed_docs=compressed,
            top_k=2,
        )

        self.assertEqual(protected_count, 1)
        self.assertEqual(result[0].metadata["source"], "a.md")
        self.assertTrue(result[0].metadata["contextual_compression_protected"])
        self.assertEqual(result[1].metadata["source"], "c.md")

    @patch("rag.vector_store.ContextualCompressionRetriever")
    @patch("rag.vector_store.create_bge_compressor")
    def test_compression_empty_results_fallback_to_baseline(self, mock_compressor, mock_retriever):
        mock_retriever.return_value.invoke.return_value = []
        baseline = [
            Document(page_content="基础内容", metadata={"source": "a.md", "score": 0.8}),
        ]

        result, trace = self.manager._compress_with_contextual_retriever("问题", baseline, 1)

        self.assertEqual(result[0].metadata["source"], "a.md")
        self.assertEqual(trace["fallback_reason"], "empty_compressed_results")
        self.assertEqual(trace["compressed_count"], 0)


class TraceDocumentsTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)

    def test_trace_documents_exports_scores_and_source_metadata(self):
        docs = [
            Document(
                page_content="内容",
                metadata={
                    "source": "a.md",
                    "header_2": "章节",
                    "score": 0.91,
                    "vector_score": 0.8,
                    "keyword_score": 0.7,
                    "rerank_score": 0.6,
                    "distance": 0.2,
                    "candidate_source": "bm25",
                    "keyword_candidate_score": 1.2,
                    "ensemble_rank": 3,
                    "expanded_subchunks": 2,
                    "contextual_compression_protected": True,
                },
            )
        ]

        result = self.manager._trace_documents(docs)

        self.assertEqual(result[0]["source"], "a.md")
        self.assertEqual(result[0]["section"], "章节")
        self.assertEqual(result[0]["score"], 0.91)
        self.assertEqual(result[0]["vector_score"], 0.8)
        self.assertEqual(result[0]["keyword_score"], 0.7)
        self.assertEqual(result[0]["rerank_score"], 0.6)
        self.assertEqual(result[0]["candidate_source"], "bm25")
        self.assertEqual(result[0]["expanded_subchunks"], 2)
        self.assertTrue(result[0]["contextual_compression_protected"])


if __name__ == "__main__":
    unittest.main()
