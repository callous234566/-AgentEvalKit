"""Additional FastAPI endpoint tests using TestClient."""

import logging
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class RequestContextMiddlewareTest(unittest.TestCase):
    def test_health_response_includes_request_headers(self):
        from main import app

        client = TestClient(app)
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers.get("X-Request-ID"))
        self.assertTrue(response.headers.get("X-Process-Time-Ms", "").isdigit())

    def test_preserves_incoming_request_id(self):
        from main import app

        client = TestClient(app)
        response = client.get("/health", headers={"X-Request-ID": "req-test-1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Request-ID"], "req-test-1")

    @patch("main.config.API_TOKEN", "secret")
    def test_unauthorized_response_includes_request_id(self):
        from main import app

        client = TestClient(app)
        response = client.post(
            "/retrieve",
            json={"question": "test", "collection_name": "test"},
            headers={"X-Request-ID": "req-unauthorized"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["X-Request-ID"], "req-unauthorized")

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_request_id_context_reaches_submodule_logs(self, mock_vs, mock_key):
        def log_and_return(collection_name):
            logging.getLogger("rag.vector_store").info("submodule_context_log")
            return []

        mock_vs.list_documents.side_effect = log_and_return
        from main import app

        client = TestClient(app)
        with self.assertLogs("rag.vector_store", level="INFO") as logs:
            response = client.get(
                "/collections/test/documents",
                headers={"X-Request-ID": "req-context-test"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Request-ID"], "req-context-test")
        self.assertIn("submodule_context_log", "\n".join(logs.output))
        self.assertEqual(logs.records[0].request_id, "req-context-test")


class CollectionsEndpointsTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_get_collection_info(self, mock_vs, mock_key):
        mock_vs.get_collection_info.return_value = {
            "collection_name": "test",
            "document_count": 5,
        }
        from main import app
        client = TestClient(app)
        response = client.get("/collections/test/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["document_count"], 5)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_list_collection_documents(self, mock_vs, mock_key):
        mock_vs.list_documents.return_value = [
            {"name": "doc1.pdf", "chunk_count": 3},
        ]
        from main import app
        client = TestClient(app)
        response = client.get("/collections/test/documents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["documents"]), 1)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_endpoint_business_failure_log_includes_request_id(self, mock_vs, mock_key):
        mock_vs.list_documents.side_effect = RuntimeError("boom")
        from main import app

        client = TestClient(app)
        with self.assertLogs("main", level="ERROR") as logs:
            response = client.get(
                "/collections/test/documents",
                headers={"X-Request-ID": "req-log-test"},
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.headers["X-Request-ID"], "req-log-test")
        log_output = "\n".join(logs.output)
        self.assertIn("request_id=req-log-test", log_output)
        self.assertIn("operation=list_collection_documents", log_output)
        self.assertIn("collection_name='test'", log_output)
        self.assertIn("boom", log_output)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_delete_collection_document(self, mock_vs, mock_key):
        mock_vs.delete_document.return_value = True
        from main import app
        client = TestClient(app)
        response = client.delete("/collections/test/documents?source=doc.pdf")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_delete_nonexistent_document(self, mock_vs, mock_key):
        mock_vs.delete_document.return_value = False
        from main import app
        client = TestClient(app)
        response = client.delete("/collections/test/documents?source=missing.pdf")
        self.assertEqual(response.status_code, 404)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_delete_collection(self, mock_vs, mock_key):
        mock_vs.delete_collection.return_value = True
        from main import app
        client = TestClient(app)
        response = client.delete("/collections/test")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_delete_collection_failure_log_includes_request_id(self, mock_vs, mock_key):
        mock_vs.delete_collection.side_effect = RuntimeError("delete boom")
        from main import app

        client = TestClient(app)
        with self.assertLogs("main", level="ERROR") as logs:
            response = client.delete(
                "/collections/test",
                headers={"X-Request-ID": "req-delete-log"},
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.headers["X-Request-ID"], "req-delete-log")
        log_output = "\n".join(logs.output)
        self.assertIn("request_id=req-delete-log", log_output)
        self.assertIn("operation=delete_collection", log_output)
        self.assertIn("collection_name='test'", log_output)
        self.assertIn("delete boom", log_output)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_rename_collection(self, mock_vs, mock_key):
        mock_vs.rename_collection.return_value = True
        from main import app
        client = TestClient(app)
        response = client.post(
            "/collections/old_name/rename",
            json={"new_name": "new_name"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["new_name"], "new_name")

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.vector_store")
    def test_rename_empty_name_rejected(self, mock_vs, mock_key):
        from main import app
        client = TestClient(app)
        response = client.post(
            "/collections/old/rename",
            json={"new_name": ""},
        )
        self.assertEqual(response.status_code, 422)


class RetrieveEndpointTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_retrieve_empty_question(self, mock_chain, mock_key):
        from main import app
        client = TestClient(app)
        response = client.post("/retrieve", json={"question": "", "collection_name": "test"})
        self.assertEqual(response.status_code, 400)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_retrieve_no_api_key(self, mock_chain, mock_key):
        mock_key.return_value = False
        from main import app
        client = TestClient(app)
        response = client.post("/retrieve", json={"question": "test", "collection_name": "test"})
        self.assertEqual(response.status_code, 500)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_retrieve_returns_trace_and_source_scores(self, mock_chain, mock_key):
        fake_chain = MagicMock()
        fake_chain.retrieve.return_value = {
            "question": "test",
            "retrieval_query": "test query",
            "resolved_question": "test",
            "documents": [
                {
                    "content": "content",
                    "metadata": {
                        "source": "a.md",
                        "score": 0.9,
                        "vector_score": 0.8,
                        "keyword_score": 0.7,
                        "rerank_score": 0.6,
                        "candidate_source": "bm25",
                    },
                }
            ],
            "sources": [
                {
                    "index": 1,
                    "source": "a.md",
                    "section": "章节",
                    "content": "content",
                    "score": 0.9,
                    "vector_score": 0.8,
                    "keyword_score": 0.7,
                    "rerank_score": 0.6,
                    "candidate_source": "bm25",
                }
            ],
            "retrieved_count": 10,
            "selected_count": 1,
            "trace": {
                "retrieved_count": 10,
                "selected_count": 1,
                "final_documents": [
                    {
                        "source": "a.md",
                        "score": 0.9,
                        "candidate_source": "bm25",
                    }
                ],
            },
            "success": True,
            "error": None,
        }
        mock_chain.return_value = fake_chain
        from main import app

        client = TestClient(app)
        response = client.post("/retrieve", json={"question": "test", "collection_name": "test"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["trace"]["final_documents"][0]["source"], "a.md")
        self.assertEqual(data["sources"][0]["vector_score"], 0.8)
        self.assertEqual(data["sources"][0]["candidate_source"], "bm25")


class GenerateEndpointTest(unittest.TestCase):
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_generate_empty_question(self, mock_chain, mock_key):
        from main import app
        client = TestClient(app)
        response = client.post("/generate", json={"question": "", "collection_name": "test"})
        self.assertEqual(response.status_code, 400)

    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    def test_generate_no_api_key(self, mock_chain, mock_key):
        mock_key.return_value = False
        from main import app
        client = TestClient(app)
        response = client.post("/generate", json={"question": "test", "collection_name": "test"})
        self.assertEqual(response.status_code, 500)


class AgentEndpointTest(unittest.TestCase):
    @patch("main.config.AGENT_ENABLED", True)
    @patch("main.config.check_api_key", return_value=True)
    @patch("main._get_llm")
    @patch("rag.agent.run_agent")
    @patch("rag.agent.create_agent")
    @patch("rag.tools.create_tools")
    def test_agent_returns_debug_info(
        self,
        mock_tools,
        mock_create_agent,
        mock_run_agent,
        mock_llm,
        mock_key,
    ):
        mock_tools.return_value = []
        mock_create_agent.return_value = object()
        mock_run_agent.return_value = {
            "success": True,
            "answer": "ok",
            "agent_steps": [{"tool": "search_web", "input": "q", "output": "o"}],
            "debug_info": {"enabled": True, "tool_sequence": ["search_web"]},
            "error": None,
        }
        from main import app

        client = TestClient(app)
        response = client.post(
            "/agent",
            json={"question": "test", "collection_name": "test", "debug": True},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["debug_info"]["tool_sequence"], ["search_web"])
        self.assertTrue(mock_run_agent.called)

    @patch("main.config.AGENT_ENABLED", True)
    @patch("main.config.check_api_key", return_value=True)
    @patch("main._get_llm")
    @patch("rag.agent.run_agent")
    @patch("rag.agent.create_agent")
    @patch("rag.tools.create_tools")
    def test_agent_preserves_policy_budget_and_source_layers(
        self,
        mock_tools,
        mock_create_agent,
        mock_run_agent,
        mock_llm,
        mock_key,
    ):
        mock_tools.return_value = []
        mock_create_agent.return_value = object()
        mock_run_agent.return_value = {
            "success": True,
            "answer": "ok",
            "agent_steps": [{"tool": "search_knowledge_base", "input": "q", "output": "o"}],
            "debug_info": {
                "enabled": True,
                "tool_sequence": ["search_knowledge_base"],
                "tool_policy": {"category": "local_knowledge", "recommended_first_tool": "search_knowledge_base"},
                "tool_budget": {"counts": {"total": 1}, "limits": {"max_tool_calls": 4}, "violations": []},
                "source_layers": {"mode": "local_only", "local_priority": True},
                "evidence_summary": {
                    "mode": "local_plus_web",
                    "local_used": True,
                    "web_used": True,
                    "local_fallback_used": True,
                    "web_provider": "Tavily",
                    "web_fallback_used": True,
                    "web_attempt_count": 1,
                    "web_result_count": 2,
                    "policy_violations": ["web_used_for_non_realtime_question"],
                },
            },
            "error": None,
        }
        from main import app

        client = TestClient(app)
        response = client.post(
            "/agent",
            json={"question": "LangChain 的核心模块有哪些？", "collection_name": "test", "debug": True},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["debug_info"]["tool_policy"]["category"], "local_knowledge")
        self.assertEqual(data["debug_info"]["tool_budget"]["counts"]["total"], 1)
        self.assertEqual(data["debug_info"]["source_layers"]["mode"], "local_only")
        evidence_summary = data["debug_info"]["evidence_summary"]
        self.assertEqual(evidence_summary["mode"], "local_plus_web")
        self.assertTrue(evidence_summary["local_used"])
        self.assertTrue(evidence_summary["web_used"])
        self.assertTrue(evidence_summary["local_fallback_used"])
        self.assertEqual(evidence_summary["web_provider"], "Tavily")
        self.assertTrue(evidence_summary["web_fallback_used"])
        self.assertEqual(evidence_summary["web_attempt_count"], 1)
        self.assertEqual(evidence_summary["web_result_count"], 2)
        self.assertEqual(
            evidence_summary["policy_violations"],
            ["web_used_for_non_realtime_question"],
        )

    @patch("main.config.AGENT_ENABLED", True)
    @patch("main.config.check_api_key", return_value=True)
    @patch("main._get_llm")
    @patch("rag.agent.run_agent")
    @patch("rag.agent.create_agent")
    @patch("rag.tools.create_tools")
    def test_agent_failure_log_includes_request_id(
        self,
        mock_tools,
        mock_create_agent,
        mock_run_agent,
        mock_llm,
        mock_key,
    ):
        mock_tools.return_value = []
        mock_create_agent.return_value = object()
        mock_run_agent.side_effect = RuntimeError("agent boom")
        from main import app

        client = TestClient(app)
        with self.assertLogs("main", level="ERROR") as logs:
            response = client.post(
                "/agent",
                json={"question": "test", "collection_name": "test", "debug": True},
                headers={"X-Request-ID": "req-agent-log"},
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.headers["X-Request-ID"], "req-agent-log")
        log_output = "\n".join(logs.output)
        self.assertIn("request_id=req-agent-log", log_output)
        self.assertIn("operation=agent_query", log_output)
        self.assertIn("collection_name='test'", log_output)
        self.assertIn("agent boom", log_output)

    @patch("main.config.AGENT_ENABLED", True)
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    @patch("main._get_llm")
    @patch("rag.agent.run_agent")
    @patch("rag.agent.create_agent")
    @patch("rag.tools.create_tools")
    def test_agent_local_failure_falls_back_to_regular_rag(
        self,
        mock_tools,
        mock_create_agent,
        mock_run_agent,
        mock_llm,
        mock_get_qa_chain,
        mock_key,
    ):
        fake_chain = MagicMock()
        fake_chain.ask.return_value = {
            "question": "test",
            "answer": "fallback answer",
            "sources": [{"source": "doc.md"}],
            "success": True,
            "error": None,
        }
        mock_get_qa_chain.return_value = fake_chain
        mock_tools.return_value = []
        mock_create_agent.return_value = object()
        mock_run_agent.return_value = {
            "success": False,
            "answer": "",
            "agent_steps": [],
            "debug_info": {
                "tool_policy": {"category": "local_knowledge"},
                "fallback_reason": "agent_execution_error",
            },
            "error": "agent failed",
        }
        from main import app

        client = TestClient(app)
        response = client.post(
            "/agent",
            json={"question": "test", "collection_name": "test", "debug": True},
            headers={"X-Request-ID": "req-agent-fallback"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["answer"], "fallback answer")
        self.assertEqual(data["agent_steps"][0]["tool"], "fallback_rag")
        self.assertEqual(data["debug_info"]["fallback_used"], "rag_qa")
        self.assertEqual(data["debug_info"]["fallback_sources"], [{"source": "doc.md"}])
        fake_chain.ask.assert_called_once()

    @patch("main.config.AGENT_ENABLED", True)
    @patch("main.config.check_api_key", return_value=True)
    @patch("main.get_qa_chain")
    @patch("main._get_llm")
    @patch("rag.agent.run_agent")
    @patch("rag.agent.create_agent")
    @patch("rag.tools.create_tools")
    def test_agent_realtime_failure_does_not_fallback_to_rag(
        self,
        mock_tools,
        mock_create_agent,
        mock_run_agent,
        mock_llm,
        mock_get_qa_chain,
        mock_key,
    ):
        mock_tools.return_value = []
        mock_create_agent.return_value = object()
        mock_run_agent.return_value = {
            "success": False,
            "answer": "",
            "agent_steps": [],
            "debug_info": {
                "tool_policy": {"category": "external_realtime"},
                "fallback_reason": "agent_execution_error",
            },
            "error": "web failed",
        }
        from main import app

        client = TestClient(app)
        response = client.post(
            "/agent",
            json={"question": "2026 年 Python 最新版本是什么？", "collection_name": "test", "debug": True},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "web failed")
        mock_get_qa_chain.assert_not_called()


if __name__ == "__main__":
    unittest.main()
