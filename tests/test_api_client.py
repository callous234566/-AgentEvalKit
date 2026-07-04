"""Tests for rag.api_client with mocked HTTP calls."""

import unittest
from unittest.mock import MagicMock, patch

from rag.api_client import RagApiClient, build_api_headers


class BuildApiHeadersTest(unittest.TestCase):
    def test_empty_token(self):
        self.assertEqual(build_api_headers(""), {})

    def test_with_token(self):
        result = build_api_headers("my-token")
        self.assertEqual(result, {"Authorization": "Bearer my-token"})


class RagApiClientInitTest(unittest.TestCase):
    def test_trailing_slash_stripped(self):
        client = RagApiClient("http://localhost:8000/")
        self.assertEqual(client.api_base_url, "http://localhost:8000")
        self.assertEqual(client.last_response_meta, {})

    def test_headers_property(self):
        client = RagApiClient("http://localhost:8000", api_token="abc")
        self.assertEqual(client.headers, {"Authorization": "Bearer abc"})


class RagApiClientResponseMetaTest(unittest.TestCase):
    @patch("rag.api_client.requests.get")
    def test_success_response_captures_request_diagnostics(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            headers={"X-Request-ID": "req-123", "X-Process-Time-Ms": "42"},
            json=lambda: ["col"],
        )
        client = RagApiClient("http://localhost:8000")

        result = client.list_collections()

        self.assertEqual(result, ["col"])
        self.assertEqual(
            client.last_response_meta,
            {"request_id": "req-123", "process_time_ms": "42", "status_code": 200},
        )

    @patch("rag.api_client.requests.post")
    def test_non_200_response_still_captures_request_diagnostics(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=503,
            headers={"X-Request-ID": "req-fail", "X-Process-Time-Ms": "7"},
        )
        client = RagApiClient("http://localhost:8000")

        result = client.ask("what", "default")

        self.assertFalse(result["success"])
        self.assertIn("503", result["error"])
        self.assertEqual(
            client.last_response_meta,
            {"request_id": "req-fail", "process_time_ms": "7", "status_code": 503},
        )

    @patch("rag.api_client.requests.get", side_effect=RuntimeError("connection refused"))
    def test_exception_response_meta_has_error_summary(self, mock_get):
        client = RagApiClient("http://localhost:8000")

        self.assertFalse(client.health())

        self.assertEqual(client.last_response_meta["status_code"], None)
        self.assertEqual(client.last_response_meta["request_id"], "")
        self.assertEqual(client.last_response_meta["process_time_ms"], "")
        self.assertIn("connection refused", client.last_response_meta["error"])


class RagApiClientHealthTest(unittest.TestCase):
    @patch("rag.api_client.requests.get")
    def test_health_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        client = RagApiClient("http://localhost:8000")
        self.assertTrue(client.health())

    @patch("rag.api_client.requests.get")
    def test_health_failure(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)
        client = RagApiClient("http://localhost:8000")
        self.assertFalse(client.health())

    @patch("rag.api_client.requests.get", side_effect=Exception("connection refused"))
    def test_health_exception(self, mock_get):
        client = RagApiClient("http://localhost:8000")
        self.assertFalse(client.health())


class RagApiClientListCollectionsTest(unittest.TestCase):
    @patch("rag.api_client.requests.get")
    def test_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: ["col1", "col2"])
        client = RagApiClient("http://localhost:8000")
        result = client.list_collections()
        self.assertEqual(result, ["col1", "col2"])

    @patch("rag.api_client.requests.get", side_effect=Exception("fail"))
    def test_exception_returns_empty(self, mock_get):
        client = RagApiClient("http://localhost:8000")
        self.assertEqual(client.list_collections(), [])


class RagApiClientAskTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "answer": "42", "sources": []},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.ask("what", "default")
        self.assertTrue(result["success"])
        self.assertEqual(result["answer"], "42")

    def test_connection_error_fallback(self):
        client = RagApiClient("http://127.0.0.1:1", api_token="abc")
        result = client.ask("hello", "default")
        self.assertFalse(result["success"])
        self.assertIn("请求异常", result["error"])

    @patch("rag.api_client.requests.post")
    def test_non_200_status(self, mock_post):
        mock_post.return_value = MagicMock(status_code=500)
        client = RagApiClient("http://localhost:8000")
        result = client.ask("what", "default")
        self.assertFalse(result["success"])
        self.assertIn("500", result["error"])


class RagApiClientRetrieveTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "success": True,
                "documents": [{"content": "doc1", "metadata": {}}],
                "sources": [],
            },
        )
        client = RagApiClient("http://localhost:8000")
        result = client.retrieve("query", "default")
        self.assertTrue(result["success"])

    @patch("rag.api_client.requests.post")
    def test_failure_fallback(self, mock_post):
        mock_post.return_value = MagicMock(status_code=404)
        client = RagApiClient("http://localhost:8000")
        result = client.retrieve("query", "default")
        self.assertFalse(result["success"])


class RagApiClientGenerateTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "answer": "generated", "sources": []},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.generate("q", "col", [{"content": "doc"}])
        self.assertTrue(result["success"])


class RagApiClientAgentTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_agent_preserves_debug_payload_and_request_shape(self, mock_post):
        payload = {
            "success": True,
            "answer": "agent answer",
            "agent_steps": [{"tool": "search_web", "input": "q", "output": "o"}],
            "debug_info": {
                "search_trace": {
                    "provider": "Tavily",
                    "fallback_used": False,
                    "attempts": [{"provider": "Tavily", "attempt": 1, "success": True, "error": ""}],
                    "result_count": 2,
                },
                "evidence_summary": {
                    "mode": "web_only",
                    "local_used": False,
                    "web_used": True,
                    "web_provider": "Tavily",
                    "web_fallback_used": False,
                    "web_attempt_count": 1,
                    "web_result_count": 2,
                    "policy_violations": [],
                },
            },
        }
        mock_post.return_value = MagicMock(
            status_code=200,
            headers={"X-Request-ID": "req-agent", "X-Process-Time-Ms": "99"},
            json=lambda: payload,
        )
        client = RagApiClient("http://localhost:8000", api_token="abc")

        result = client.agent(
            "what happened",
            "default",
            chat_history=[{"role": "user", "content": "hi"}],
            debug=True,
        )

        self.assertEqual(result["agent_steps"], payload["agent_steps"])
        self.assertEqual(result["debug_info"], payload["debug_info"])
        self.assertNotIn("request_id", result)
        self.assertEqual(
            client.last_response_meta,
            {"request_id": "req-agent", "process_time_ms": "99", "status_code": 200},
        )
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        self.assertEqual(mock_post.call_args.args[0], "http://localhost:8000/agent")
        self.assertEqual(kwargs["headers"], {"Authorization": "Bearer abc"})
        self.assertEqual(kwargs["timeout"], 180)
        self.assertEqual(kwargs["json"]["question"], "what happened")
        self.assertEqual(kwargs["json"]["collection_name"], "default")
        self.assertEqual(kwargs["json"]["chat_history"], [{"role": "user", "content": "hi"}])
        self.assertTrue(kwargs["json"]["debug"])

    @patch("rag.api_client.requests.post")
    def test_agent_failure_fallback_keeps_debug_shapes(self, mock_post):
        mock_post.return_value = MagicMock(status_code=500)
        client = RagApiClient("http://localhost:8000")

        result = client.agent("what", "default", debug=True)

        self.assertFalse(result["success"])
        self.assertEqual(result["agent_steps"], [])
        self.assertEqual(result["debug_info"], {})
        self.assertIn("500", result["error"])


class RagApiClientCreateDeleteCollectionTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_create_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "message": "created"},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.create_collection("new_col")
        self.assertTrue(result["success"])

    @patch("rag.api_client.requests.post", side_effect=Exception("fail"))
    def test_create_exception(self, mock_post):
        client = RagApiClient("http://localhost:8000")
        result = client.create_collection("col")
        self.assertFalse(result["success"])

    @patch("rag.api_client.requests.delete")
    def test_delete_success(self, mock_del):
        mock_del.return_value = MagicMock(status_code=200)
        client = RagApiClient("http://localhost:8000")
        self.assertTrue(client.delete_collection("col"))

    @patch("rag.api_client.requests.delete", side_effect=Exception("fail"))
    def test_delete_exception(self, mock_del):
        client = RagApiClient("http://localhost:8000")
        self.assertFalse(client.delete_collection("col"))


class RagApiClientRenameTest(unittest.TestCase):
    @patch("rag.api_client.requests.post")
    def test_rename_success(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "message": "renamed"},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.rename_collection("old", "new")
        self.assertTrue(result["success"])

    @patch("rag.api_client.requests.post", side_effect=Exception("fail"))
    def test_rename_exception(self, mock_post):
        client = RagApiClient("http://localhost:8000")
        result = client.rename_collection("old", "new")
        self.assertFalse(result["success"])
        self.assertIn("重命名异常", result["message"])


class RagApiClientDocumentsTest(unittest.TestCase):
    @patch("rag.api_client.requests.get")
    def test_list_documents_success(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "documents": [{"name": "doc1"}]},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.list_documents("col")
        self.assertTrue(result["success"])

    @patch("rag.api_client.requests.get", side_effect=Exception("fail"))
    def test_list_documents_exception(self, mock_get):
        client = RagApiClient("http://localhost:8000")
        result = client.list_documents("col")
        self.assertFalse(result["success"])

    @patch("rag.api_client.requests.delete")
    def test_delete_document_success(self, mock_del):
        mock_del.return_value = MagicMock(
            status_code=200,
            json=lambda: {"success": True, "message": "deleted"},
        )
        client = RagApiClient("http://localhost:8000")
        result = client.delete_document("col", "source.txt")
        self.assertTrue(result["success"])


if __name__ == "__main__":
    unittest.main()
