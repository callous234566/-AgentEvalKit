"""Tests for rag.text_splitter.TextSplitter."""

import unittest

from langchain_core.documents import Document

from rag.text_splitter import TextSplitter


class TextSplitterInitTest(unittest.TestCase):
    def test_uses_config_defaults(self):
        import config
        splitter = TextSplitter()
        self.assertEqual(splitter.chunk_size, config.CHUNK_SIZE)
        self.assertEqual(splitter.chunk_overlap, config.CHUNK_OVERLAP)

    def test_custom_params(self):
        splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
        self.assertEqual(splitter.chunk_size, 100)
        self.assertEqual(splitter.chunk_overlap, 20)


class SplitDocumentsTest(unittest.TestCase):
    def setUp(self):
        self.splitter = TextSplitter(chunk_size=200, chunk_overlap=50)

    def test_empty_input(self):
        self.assertEqual(self.splitter.split_documents([]), [])

    def test_plain_text_produces_chunks(self):
        doc = Document(
            page_content="。".join([f"这是第{i}段测试文本" for i in range(30)]),
            metadata={"file_type": ".txt"},
        )
        chunks = self.splitter.split_documents([doc])
        self.assertGreaterEqual(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("chunk_index", chunk.metadata)

    def test_chunk_indices_are_sequential(self):
        doc = Document(
            page_content="。".join([f"段落{i}" for i in range(50)]),
            metadata={"file_type": ".txt"},
        )
        chunks = self.splitter.split_documents([doc])
        indices = [c.metadata["chunk_index"] for c in chunks]
        self.assertEqual(indices, list(range(len(chunks))))

    def test_markdown_with_headers_uses_header_splitting(self):
        md_content = "\n".join([
            "# 标题一",
            "这是第一部分的内容。" * 5,
            "",
            "## 标题二",
            "这是第二部分的内容。" * 5,
            "",
            "### 标题三",
            "这是第三部分的内容。" * 5,
        ])
        doc = Document(page_content=md_content, metadata={"file_type": ".md"})
        chunks = self.splitter.split_documents([doc])
        self.assertGreater(len(chunks), 1)

    def test_markdown_without_headers_falls_back_to_recursive(self):
        doc = Document(
            page_content="普通文本，没有标题。\n" * 30,
            metadata={"file_type": ".md"},
        )
        chunks = self.splitter.split_documents([doc])
        self.assertGreater(len(chunks), 0)

    def test_short_document_stays_single_chunk(self):
        doc = Document(
            page_content="短短的文档。",
            metadata={"file_type": ".txt"},
        )
        chunks = self.splitter.split_documents([doc])
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].page_content, "短短的文档。")

    def test_preserves_original_metadata(self):
        doc = Document(
            page_content="内容。" * 30,
            metadata={"file_type": ".txt", "source": "test.txt", "custom_key": "value"},
        )
        chunks = self.splitter.split_documents([doc])
        for chunk in chunks:
            self.assertEqual(chunk.metadata.get("source"), "test.txt")
            self.assertEqual(chunk.metadata.get("custom_key"), "value")


class HasMarkdownHeadersTest(unittest.TestCase):
    def setUp(self):
        self.splitter = TextSplitter()

    def test_detects_h1(self):
        self.assertTrue(self.splitter._has_markdown_headers("# 标题"))

    def test_detects_h2(self):
        self.assertTrue(self.splitter._has_markdown_headers("## 标题"))

    def test_detects_h3(self):
        self.assertTrue(self.splitter._has_markdown_headers("### 标题"))

    def test_no_headers(self):
        self.assertFalse(self.splitter._has_markdown_headers("普通文本"))

    def test_hash_in_middle_of_line(self):
        self.assertFalse(self.splitter._has_markdown_headers("文本中的#号"))


class ContainsCoreConceptTest(unittest.TestCase):
    def setUp(self):
        self.splitter = TextSplitter()

    def test_detects_qkv(self):
        self.assertTrue(self.splitter._contains_core_concept("Query, Key, Value 的计算"))

    def test_detects_attention_formula(self):
        self.assertTrue(self.splitter._contains_core_concept("Attention = Softmax(QK^T)"))

    def test_detects_code_block(self):
        self.assertTrue(self.splitter._contains_core_concept("代码示例：\n```python\nprint()\n```"))

    def test_detects_formula_marker(self):
        self.assertTrue(self.splitter._contains_core_concept("公式：E=mc^2"))

    def test_detects_algorithm_marker(self):
        self.assertTrue(self.splitter._contains_core_concept("算法：排序"))

    def test_detects_step_marker(self):
        self.assertTrue(self.splitter._contains_core_concept("步骤：第一步"))

    def test_plain_text_not_core(self):
        self.assertFalse(self.splitter._contains_core_concept("这是一段普通文本，没有特殊标记。"))


class SplitTextTest(unittest.TestCase):
    def test_empty_text(self):
        splitter = TextSplitter()
        self.assertEqual(splitter.split_text(""), [])

    def test_whitespace_only(self):
        splitter = TextSplitter()
        self.assertEqual(splitter.split_text("   \n\n  "), [])

    def test_basic_split(self):
        splitter = TextSplitter(chunk_size=50, chunk_overlap=10)
        text = "。".join([f"这是第{i}句话" for i in range(20)])
        chunks = splitter.split_text(text)
        self.assertGreater(len(chunks), 1)


class GetChunkInfoTest(unittest.TestCase):
    def test_empty_chunks(self):
        splitter = TextSplitter()
        info = splitter.get_chunk_info([])
        self.assertEqual(info["total_chunks"], 0)
        self.assertEqual(info["avg_chunk_size"], 0)

    def test_stats_computation(self):
        splitter = TextSplitter()
        chunks = [
            Document(page_content="短"),
            Document(page_content="中等长度文本"),
            Document(page_content="这是一段比较长的测试文本内容"),
        ]
        info = splitter.get_chunk_info(chunks)
        self.assertEqual(info["total_chunks"], 3)
        self.assertEqual(info["min_chunk_size"], 1)
        self.assertGreater(info["max_chunk_size"], info["min_chunk_size"])
        self.assertGreater(info["avg_chunk_size"], 0)


if __name__ == "__main__":
    unittest.main()
