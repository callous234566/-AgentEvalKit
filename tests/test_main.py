"""Tests for main.py FastAPI endpoints and helper functions."""

import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient


class SanitizeUploadFilenameTest(unittest.TestCase):
    def _call(self, name):
        from main import sanitize_upload_filename
        return sanitize_upload_filename(name)

    def test_normal_filename(self):
        self.assertEqual(self._call("test.pdf"), "test.pdf")

    def test_chinese_filename(self):
        result = self._call("测试文档.pdf")
        self.assertIn(".pdf", result)

    def test_path_traversal_stripped(self):
        result = self._call("../../etc/passwd.pdf")
        self.assertNotIn("..", result)
        self.assertNotIn("/", result)

    def test_empty_raises(self):
        with self.assertRaises(HTTPException):
            self._call("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(HTTPException):
            self._call("   ")

    def test_no_extension_raises(self):
        with self.assertRaises(HTTPException):
            self._call("noext")

    def test_special_chars_replaced(self):
        result = self._call("file name@#.pdf")
        self.assertNotIn(" ", result)
        self.assertNotIn("@", result)
        self.assertIn(".pdf", result)

    def test_dot_prefix_stripped(self):
        result = self._call(".hidden.pdf")
        self.assertFalse(result.startswith("."))


class QaChainDocumentFromPayloadTest(unittest.TestCase):
    def test_conversion(self):
        from main import qa_chain_document_from_payload
        from main import RetrievedDocument

        payload = RetrievedDocument(content="test content", metadata={"source": "a.txt"})
        doc = qa_chain_document_from_payload(payload)
        self.assertEqual(doc.page_content, "test content")
        self.assertEqual(doc.metadata["source"], "a.txt")

    def test_empty_metadata(self):
        from main import qa_chain_document_from_payload, RetrievedDocument

        payload = RetrievedDocument(content="content", metadata={})
        doc = qa_chain_document_from_payload(payload)
        self.assertEqual(doc.metadata, {})


class GetQaChainCacheTest(unittest.TestCase):
    def setUp(self):
        import main
        main._qa_chain_cache.clear()

    @patch("main.QAChain")
    def test_creates_and_caches(self, MockQAChain):
        from main import get_qa_chain
        mock_instance = MagicMock()
        MockQAChain.return_value = mock_instance

        chain1 = get_qa_chain("test_collection")
        chain2 = get_qa_chain("test_collection")
        self.assertIs(chain1, chain2)
        MockQAChain.assert_called_once()

    @patch("main.QAChain")
    def test_different_params_different_cache(self, MockQAChain):
        from main import get_qa_chain
        MockQAChain.return_value = MagicMock()

        get_qa_chain("col1", top_k=3)
        get_qa_chain("col1", top_k=5)
        self.assertEqual(MockQAChain.call_count, 2)

    @patch("main.QAChain")
    def test_cache_eviction(self, MockQAChain):
        from main import get_qa_chain
        MockQAChain.return_value = MagicMock()

        for i in range(20):
            get_qa_chain(f"col_{i}")
        import main
        self.assertLessEqual(len(main._qa_chain_cache), main._QA_CHAIN_CACHE_MAX_SIZE)


class HealthEndpointTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_health_returns_200(self, mock_vs, mock_key):
        from main import app
        client = TestClient(app)
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_root_returns_200(self, mock_vs, mock_key):
        from main import app
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "running")


class CollectionsEndpointTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_list_collections(self, mock_vs, mock_key):
        mock_vs.list_collections.return_value = ["col1", "col2"]
        from main import app
        client = TestClient(app)
        response = client.get("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["col1", "col2"])

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_create_collection(self, mock_vs, mock_key):
        mock_vs._get_store.return_value = MagicMock()
        from main import app
        client = TestClient(app)
        response = client.post("/collections/new_col")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])


class AskEndpointTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_ask_empty_question_rejected(self, mock_chain, mock_key):
        from main import app
        client = TestClient(app)
        response = client.post("/ask", json={"question": "", "collection_name": "test"})
        self.assertEqual(response.status_code, 400)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_ask_no_api_key(self, mock_chain, mock_key):
        mock_key.return_value = False
        from main import app
        client = TestClient(app)
        response = client.post("/ask", json={"question": "test", "collection_name": "test"})
        self.assertEqual(response.status_code, 500)


class PydanticModelTest(unittest.TestCase):
    def test_question_request_defaults(self):
        from main import QuestionRequest
        req = QuestionRequest(question="test")
        self.assertEqual(req.collection_name, "default")
        self.assertEqual(req.chat_history, [])
        self.assertIsNone(req.top_k)

    def test_question_request_validation(self):
        from main import QuestionRequest
        req = QuestionRequest(question="test", top_k=5, temperature=0.5)
        self.assertEqual(req.top_k, 5)
        self.assertEqual(req.temperature, 0.5)

    def test_rename_request_requires_name(self):
        from main import RenameCollectionRequest
        with self.assertRaises(Exception):
            RenameCollectionRequest(new_name="")

    def test_chat_message(self):
        from main import ChatMessage
        msg = ChatMessage(role="user", content="hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "hello")


if __name__ == "__main__":
    unittest.main()
