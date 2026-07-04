"""Tests for rag.document_loader.DocumentLoader."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rag.document_loader import DocumentLoader


class DocumentLoaderInitTest(unittest.TestCase):
    def test_errors_list_starts_empty(self):
        loader = DocumentLoader()
        self.assertEqual(loader.errors, [])


class IsSupportedTest(unittest.TestCase):
    def test_supported_extensions(self):
        for ext in (".pdf", ".txt", ".docx", ".md"):
            self.assertTrue(DocumentLoader.is_supported(f"file{ext}"), f"{ext} should be supported")

    def test_unsupported_extensions(self):
        for ext in (".jpg", ".py", ".exe", ".xlsx", ".csv"):
            self.assertFalse(DocumentLoader.is_supported(f"file{ext}"), f"{ext} should not be supported")

    def test_case_insensitive(self):
        self.assertTrue(DocumentLoader.is_supported("FILE.PDF"))
        self.assertTrue(DocumentLoader.is_supported("file.TXT"))


class LoadRawTextTest(unittest.TestCase):
    def setUp(self):
        self.loader = DocumentLoader()

    def test_utf8_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("你好世界\nHello World")
            path = f.name
        try:
            docs = self.loader._load_raw_text(path)
            self.assertEqual(len(docs), 1)
            self.assertIn("你好世界", docs[0].page_content)
            self.assertIn("Hello World", docs[0].page_content)
        finally:
            Path(path).unlink()

    def test_gbk_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write("中文内容GBK编码".encode("gbk"))
            path = f.name
        try:
            docs = self.loader._load_raw_text(path)
            self.assertEqual(len(docs), 1)
            self.assertIn("中文内容", docs[0].page_content)
        finally:
            Path(path).unlink()

    def test_bom_stripped(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(b"\xef\xbb\xbfHello BOM")
            path = f.name
        try:
            docs = self.loader._load_raw_text(path)
            self.assertFalse(docs[0].page_content.startswith("﻿"))
            self.assertTrue(docs[0].page_content.startswith("Hello BOM"))
        finally:
            Path(path).unlink()

    def test_metadata_contains_encoding(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("test")
            path = f.name
        try:
            docs = self.loader._load_raw_text(path)
            self.assertIn("encoding", docs[0].metadata)
        finally:
            Path(path).unlink()

    def test_excessive_blank_lines_collapsed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("line1\n\n\n\n\nline2")
            path = f.name
        try:
            docs = self.loader._load_raw_text(path)
            content = docs[0].page_content
            self.assertNotIn("\n\n\n", content)
        finally:
            Path(path).unlink()


class LoadDocumentTest(unittest.TestCase):
    def setUp(self):
        self.loader = DocumentLoader()

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.loader.load_document("/nonexistent/path/file.txt")

    def test_unsupported_format(self):
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            f.write(b"content")
            path = f.name
        try:
            with self.assertRaises(ValueError):
                self.loader.load_document(path)
        finally:
            Path(path).unlink()

    def test_txt_file_loads_with_metadata(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("测试文档内容")
            path = f.name
        try:
            with patch.object(self.loader, "_load_raw_text", wraps=self.loader._load_raw_text) as mock:
                docs = self.loader.load_document(path, enable_multimodal=False)
            self.assertGreater(len(docs), 0)
            self.assertIn("source", docs[0].metadata)
            self.assertIn("file_type", docs[0].metadata)
            self.assertEqual(docs[0].metadata["file_type"], ".txt")
        finally:
            Path(path).unlink()

    def test_md_file_loads(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# 标题\n\nMarkdown内容")
            path = f.name
        try:
            docs = self.loader.load_document(path, enable_multimodal=False)
            self.assertGreater(len(docs), 0)
            self.assertEqual(docs[0].metadata["file_type"], ".md")
        finally:
            Path(path).unlink()


class LoadDocumentsBatchTest(unittest.TestCase):
    def setUp(self):
        self.loader = DocumentLoader()

    def test_batch_with_one_failing_file(self):
        good = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        good.write("好文件")
        good.close()

        docs = self.loader.load_documents(
            [good.name, "/nonexistent/file.txt"],
            enable_multimodal=False,
        )
        self.assertGreater(len(docs), 0)
        # load_documents catches exceptions per-file and logs warnings;
        # errors list is only populated via load_document's inner handler.
        Path(good.name).unlink()

    def test_empty_batch(self):
        docs = self.loader.load_documents([], enable_multimodal=False)
        self.assertEqual(docs, [])


if __name__ == "__main__":
    unittest.main()
