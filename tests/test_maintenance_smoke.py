import json
import tempfile
import unittest
from pathlib import Path

from langchain_core.documents import Document

from eval.rag_eval import build_headers, load_cases
from rag.api_client import RagApiClient, build_api_headers
from rag.upload_validation import validate_uploaded_file_content
from rag.vector_store import VectorStoreManager


class UploadValidationTest(unittest.TestCase):
    def test_accepts_valid_basic_files_and_rejects_spoofed_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)

            pdf = base / "ok.pdf"
            pdf.write_bytes(b"%PDF-1.7\n%test")
            validate_uploaded_file_content(str(pdf), ".pdf", "application/pdf")

            docx = base / "ok.docx"
            docx.write_bytes(b"PK\x03\x04fake-docx")
            validate_uploaded_file_content(
                str(docx),
                ".docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            text = base / "ok.txt"
            text.write_text("中文文本\nhello", encoding="utf-8")
            validate_uploaded_file_content(str(text), ".txt", "text/plain; charset=utf-8")

            fake_pdf = base / "fake.pdf"
            fake_pdf.write_text("not a pdf", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(str(fake_pdf), ".pdf", "application/pdf")

            binary_text = base / "binary.txt"
            binary_text.write_bytes(b"abc\x00def")
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(str(binary_text), ".txt", "text/plain")


class RagEvalTest(unittest.TestCase):
    def test_build_headers_and_case_validation(self):
        self.assertEqual(build_headers(""), {})
        self.assertEqual(build_headers("token"), {"Authorization": "Bearer token"})

        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)

            valid_cases = base / "valid.json"
            valid_cases.write_text(
                json.dumps([{"question": "test question", "expected_keywords": ["test"]}]),
                encoding="utf-8",
            )
            self.assertEqual(load_cases(valid_cases)[0]["question"], "test question")

            empty_cases = base / "empty.json"
            empty_cases.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_cases(empty_cases)

            bad_keywords = base / "bad_keywords.json"
            bad_keywords.write_text(
                json.dumps([{"question": "test", "expected_keywords": "oops"}]),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_cases(bad_keywords)


class ParentIndexCacheTest(unittest.TestCase):
    def test_parent_index_cache_expands_sibling_subchunks(self):
        manager = VectorStoreManager.__new__(VectorStoreManager)
        manager._collection_cache = {}

        class FakeCollection:
            name = "fake"

            def count(self):
                return 3

            def get(self, include=None):
                return {
                    "documents": ["part 0", "part 1", "other"],
                    "metadatas": [
                        {"source": "a.md", "parent_chunk_index": 7, "sub_chunk_index": 0},
                        {"source": "a.md", "parent_chunk_index": "7", "sub_chunk_index": 1},
                        {"source": "b.md"},
                    ],
                }

        class FakeStore:
            _collection = FakeCollection()

        cache = VectorStoreManager._get_cached_collection_snapshot(manager, FakeStore())
        self.assertEqual(cache["count"], 3)
        self.assertEqual(len(cache["parent_index"][("a.md", 7)]), 2)

        hit = Document(
            page_content="part 1",
            metadata={"source": "a.md", "parent_chunk_index": 7, "sub_chunk_index": 1},
        )
        expanded = VectorStoreManager._expand_related_subchunks(manager, FakeStore(), [hit], 4)
        self.assertEqual(len(expanded), 1)
        self.assertEqual(expanded[0].page_content, "part 0\npart 1")
        self.assertEqual(expanded[0].metadata["expanded_subchunks"], 2)


class ApiClientTest(unittest.TestCase):
    def test_headers_and_failed_request_fallback(self):
        self.assertEqual(build_api_headers(""), {})
        self.assertEqual(build_api_headers("abc"), {"Authorization": "Bearer abc"})

        client = RagApiClient("http://127.0.0.1:9", api_token="abc")
        result = client.ask("hello", "default")
        self.assertFalse(result["success"])
        self.assertIn("请求异常", result["error"])


if __name__ == "__main__":
    unittest.main()
