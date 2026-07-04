"""Tests for rag.reranker.BGERerankSentenceCompressor pure functions."""

import unittest
from unittest.mock import patch

from langchain_core.documents import Document

from rag.reranker import BGERerankSentenceCompressor


class SplitSentencesTest(unittest.TestCase):
    def setUp(self):
        self.compressor = BGERerankSentenceCompressor()

    def test_chinese_period_split(self):
        result = self.compressor._split_sentences("第一句。第二句。第三句。")
        self.assertEqual(len(result), 3)

    def test_chinese_question_mark(self):
        result = self.compressor._split_sentences("这是什么？不知道！")
        self.assertEqual(len(result), 2)

    def test_newline_split(self):
        result = self.compressor._split_sentences("第一行\n第二行\n第三行")
        self.assertEqual(len(result), 3)

    def test_empty_text_returns_original(self):
        result = self.compressor._split_sentences("   ")
        self.assertEqual(result, [""])

    def test_single_sentence(self):
        result = self.compressor._split_sentences("只有一个句子")
        self.assertEqual(result, ["只有一个句子"])

    def test_mixed_punctuation(self):
        result = self.compressor._split_sentences("问题？回答。结束！")
        self.assertEqual(len(result), 3)

    def test_semicolon_split(self):
        result = self.compressor._split_sentences("部分一；部分二；部分三")
        self.assertEqual(len(result), 3)


class LooksLikeCodeTest(unittest.TestCase):
    def setUp(self):
        self.compressor = BGERerankSentenceCompressor()

    def test_python_code(self):
        text = "```python\ndef hello():\n    return 'world'\n```"
        self.assertTrue(self.compressor._looks_like_code(text))

    def test_class_definition(self):
        text = "class MyClass:\n    def method(self):\n        return True"
        self.assertTrue(self.compressor._looks_like_code(text))

    def test_import_and_return(self):
        text = "import os\nreturn os.getcwd()"
        self.assertTrue(self.compressor._looks_like_code(text))

    def test_plain_text_not_code(self):
        text = "这是一段普通的中文文本，没有任何代码标记。"
        self.assertFalse(self.compressor._looks_like_code(text))

    def test_single_marker_not_enough(self):
        text = "只有 return 关键字，但没有其他标记"
        self.assertFalse(self.compressor._looks_like_code(text))

    def test_json_like_structure(self):
        text = 'import json\ndata = {"key": "value"}\nreturn data'
        self.assertTrue(self.compressor._looks_like_code(text))


class LexicalScoreTest(unittest.TestCase):
    def setUp(self):
        self.compressor = BGERerankSentenceCompressor()

    def test_perfect_match(self):
        score = self.compressor._lexical_score("机器学习", "机器学习是人工智能的分支")
        self.assertGreater(score, 0)

    def test_no_match(self):
        score = self.compressor._lexical_score("量子物理", "机器学习是人工智能的分支")
        self.assertGreaterEqual(score, 0.0)

    def test_phrase_bonus(self):
        query = "机器学习"
        text = "我们讨论机器学习的应用场景"
        score = self.compressor._lexical_score(query, text)
        self.assertGreater(score, 0.3)

    def test_empty_query(self):
        score = self.compressor._lexical_score("", "一些文本")
        self.assertEqual(score, 0.0)

    def test_english_terms(self):
        score = self.compressor._lexical_score("python function", "this python function returns data")
        self.assertGreater(score, 0)

    def test_score_capped_at_one(self):
        score = self.compressor._lexical_score("a", "a a a a a a a a")
        self.assertLessEqual(score, 1.0)


class TermsExtractionTest(unittest.TestCase):
    def setUp(self):
        self.compressor = BGERerankSentenceCompressor()

    def test_chinese_terms(self):
        terms = self.compressor._terms("机器学习算法")
        self.assertIn("机器", terms)
        self.assertIn("学习", terms)
        self.assertIn("算法", terms)

    def test_english_terms(self):
        terms = self.compressor._terms("python function test")
        self.assertIn("python", terms)
        self.assertIn("function", terms)

    def test_deduplication(self):
        terms = self.compressor._terms("test test test")
        test_count = sum(1 for t in terms if t == "test")
        self.assertEqual(test_count, 1)

    def test_chinese_bigrams_from_long_token(self):
        terms = self.compressor._terms("自然语言处理技术")
        self.assertIn("自然", terms)
        self.assertIn("语言", terms)

    def test_mixed_language(self):
        terms = self.compressor._terms("使用Python进行机器学习")
        self.assertIn("python", terms)
        self.assertIn("机器", terms)


class CompressContentTest(unittest.TestCase):
    def setUp(self):
        self.compressor = BGERerankSentenceCompressor(
            max_sentences_per_doc=3,
            api_key="",
            api_base="",
            model="",
        )

    def test_short_content_returns_unchanged(self):
        content = "第一句。第二句。"
        result = self.compressor._compress_content("测试", content)
        self.assertEqual(result, content)

    def test_code_returns_unchanged(self):
        content = "```python\ndef hello():\n    return 'world'\n```\nimport os"
        result = self.compressor._compress_content("测试", content)
        self.assertTrue(result.startswith("```"))

    def test_long_text_gets_compressed(self):
        sentences = [f"这是第{i}个句子的内容。" for i in range(10)]
        content = " ".join(sentences)
        result = self.compressor._compress_content("第", content)
        self.assertLess(len(result), len(content))


class CompressDocumentsTest(unittest.TestCase):
    def test_empty_docs(self):
        compressor = BGERerankSentenceCompressor(top_n=3, api_key="", api_base="", model="")
        result = compressor.compress_documents([], "query")
        self.assertEqual(result, [])

    def test_blank_docs_filtered(self):
        compressor = BGERerankSentenceCompressor(top_n=3, api_key="", api_base="", model="")
        docs = [Document(page_content="   "), Document(page_content="")]
        result = compressor.compress_documents(docs, "query")
        self.assertEqual(result, [])

    def test_preserves_rerank_metadata(self):
        compressor = BGERerankSentenceCompressor(
            top_n=3, max_sentences_per_doc=2, api_key="", api_base="", model=""
        )
        docs = [Document(
            page_content="短内容。",
            metadata={"source": "test.txt", "score": 0.5},
        )]
        result = compressor.compress_documents(docs, "测试")
        self.assertEqual(len(result), 1)
        self.assertIn("rerank_score", result[0].metadata)
        self.assertIn("compression_method", result[0].metadata)


class CallRerankApiTest(unittest.TestCase):
    def test_returns_empty_without_config(self):
        compressor = BGERerankSentenceCompressor(api_key="", api_base="", model="")
        result = compressor._call_rerank_api("query", ["text1"], 1)
        self.assertEqual(result, [])

    def test_returns_empty_without_texts(self):
        compressor = BGERerankSentenceCompressor(api_key="k", api_base="http://x", model="m")
        result = compressor._call_rerank_api("query", [], 1)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
