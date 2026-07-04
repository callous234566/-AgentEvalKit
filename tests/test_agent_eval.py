"""Tests for eval.agent_eval helper functions."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from eval.agent_eval import (
    ApiResult,
    build_headers,
    build_report,
    evaluate_case,
    load_cases,
    write_report,
)


class AgentEvalLoadCasesTest(unittest.TestCase):
    def test_load_cases_accepts_valid_cases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.json"
            path.write_text(
                json.dumps([
                    {"id": "case_1", "question": "问题", "tags": ["agent"]}
                ], ensure_ascii=False),
                encoding="utf-8",
            )

            cases = load_cases(path)

        self.assertEqual(cases[0]["id"], "case_1")

    def test_load_cases_rejects_missing_question(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.json"
            path.write_text(json.dumps([{"id": "case_1"}]), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_cases(path)

    def test_load_cases_rejects_non_list_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.json"
            path.write_text(
                json.dumps([
                    {
                        "id": "case_1",
                        "question": "问题",
                        "expected_debug_fields": "search_trace.provider",
                    }
                ], ensure_ascii=False),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_cases(path)


class AgentEvalHelpersTest(unittest.TestCase):
    def test_build_headers(self):
        self.assertEqual(build_headers(""), {})
        self.assertEqual(build_headers("tok"), {"Authorization": "Bearer tok"})

    def test_write_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.json"
            write_report({"summary": {"passed": 1}}, path)

            data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(data["summary"]["passed"], 1)


class AgentEvalCaseTest(unittest.TestCase):
    def test_evaluate_case_passes_routing_and_debug_assertions(self):
        case = {
            "id": "local",
            "question": "Agent 为什么优先检索本地？",
            "expected_category": "local_knowledge",
            "expected_first_tool": "search_knowledge_base",
            "forbidden_first_tools": ["search_web"],
            "required_allowed_tools": ["search_knowledge_base"],
            "expected_answer_keywords": ["本地"],
            "expected_debug_fields": ["routing_decision.category", "evidence_summary.mode"],
        }
        payload = {
            "success": True,
            "answer": "本地资料应该优先检索。",
            "agent_steps": [{"tool": "search_knowledge_base"}],
            "debug_info": {
                "routing_decision": {
                    "category": "local_knowledge",
                    "allowed_tools": ["search_knowledge_base"],
                },
                "tool_sequence": ["search_knowledge_base"],
                "evidence_summary": {"mode": "local_only"},
            },
        }

        with patch(
            "eval.agent_eval.post_agent_with_meta",
            return_value=ApiResult(payload, request_id="req-agent", process_time_ms="12"),
        ):
            result = evaluate_case(case, "http://api", "default", 5)

        self.assertTrue(result["passed"])
        self.assertEqual(result["details"]["request_id"], "req-agent")
        self.assertEqual(result["details"]["first_tool"], "search_knowledge_base")

    def test_evaluate_case_reports_failures(self):
        case = {
            "id": "bad",
            "question": "实时问题",
            "expected_category": "external_realtime",
            "expected_first_tool": "search_web",
            "forbidden_first_tools": ["execute_python_code"],
            "required_allowed_tools": ["search_web"],
            "expected_answer_sections": ["外部搜索补充"],
            "expected_answer_keywords": ["Python"],
            "forbidden_answer_keywords": ["pip install"],
            "expected_debug_fields": ["search_trace.provider"],
        }
        payload = {
            "success": False,
            "error": "boom",
            "answer": "pip install something",
            "agent_steps": [{"tool": "execute_python_code"}],
            "debug_info": {
                "routing_decision": {
                    "category": "local_knowledge",
                    "allowed_tools": ["search_knowledge_base"],
                },
                "tool_sequence": ["execute_python_code"],
            },
        }

        with patch(
            "eval.agent_eval.post_agent_with_meta",
            return_value=ApiResult(payload),
        ):
            result = evaluate_case(case, "http://api", "default", 5)

        self.assertFalse(result["passed"])
        self.assertIn("agent_failed", result["failure_reasons"])
        self.assertIn("category_mismatch", result["failure_reasons"])
        self.assertIn("first_tool_mismatch", result["failure_reasons"])
        self.assertIn("forbidden_first_tool", result["failure_reasons"])
        self.assertIn("allowed_tools_missing", result["failure_reasons"])
        self.assertIn("answer_missing_sections", result["failure_reasons"])
        self.assertIn("answer_missing_keywords", result["failure_reasons"])
        self.assertIn("answer_forbidden_keywords", result["failure_reasons"])
        self.assertIn("debug_field_missing", result["failure_reasons"])

    def test_evaluate_case_reports_endpoint_failure(self):
        case = {"id": "endpoint", "question": "问题"}

        with patch("eval.agent_eval.post_agent_with_meta", side_effect=RuntimeError("down")):
            result = evaluate_case(case, "http://api", "default", 5)

        self.assertFalse(result["passed"])
        self.assertEqual(result["failure_reasons"], ["endpoint_check_failed"])

    def test_build_report_counts_failure_reasons(self):
        cases = [
            {"id": "ok", "question": "问题"},
            {"id": "bad", "question": "问题", "expected_first_tool": "search_web"},
        ]
        payloads = [
            ApiResult({
                "success": True,
                "answer": "ok",
                "agent_steps": [],
                "debug_info": {},
            }),
            ApiResult({
                "success": True,
                "answer": "ok",
                "agent_steps": [{"tool": "search_knowledge_base"}],
                "debug_info": {"tool_sequence": ["search_knowledge_base"]},
            }),
        ]

        with patch("eval.agent_eval.post_agent_with_meta", side_effect=payloads):
            report = build_report(cases, "http://api", "default", 5)

        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["passed"], 1)
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(report["summary"]["failure_reason_counts"]["first_tool_mismatch"], 1)


if __name__ == "__main__":
    unittest.main()
