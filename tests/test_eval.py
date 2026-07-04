"""Extended tests for eval.rag_eval helper functions."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from eval.rag_eval import (
    ApiResult,
    build_case_result,
    build_headers,
    build_report,
    evaluate_case,
    extract_trace_summary,
    extract_top_documents,
    forbidden_keyword_matches,
    format_trace_summary,
    format_top_documents,
    keyword_matches,
    load_cases,
    print_case_result,
    source_matches,
    write_report,
)


class BuildHeadersExtendedTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(build_headers(""), {})

    def test_token(self):
        self.assertEqual(build_headers("tok"), {"Authorization": "Bearer tok"})


class SourceMatchesTest(unittest.TestCase):
    def test_empty_expected_always_matches(self):
        self.assertTrue(source_matches([], ""))
        self.assertTrue(source_matches([{"source": "a.txt"}], ""))

    def test_exact_match(self):
        sources = [{"source": "test.pdf", "content": "hello"}]
        self.assertTrue(source_matches(sources, "test.pdf"))

    def test_case_insensitive(self):
        sources = [{"source": "TEST.PDF"}]
        self.assertTrue(source_matches(sources, "test.pdf"))

    def test_partial_match_in_values(self):
        sources = [{"source": "a.txt", "content": "some content here"}]
        self.assertTrue(source_matches(sources, "content"))

    def test_no_match(self):
        sources = [{"source": "a.txt"}]
        self.assertFalse(source_matches(sources, "nonexistent.pdf"))

    def test_multiple_sources(self):
        sources = [
            {"source": "a.txt"},
            {"source": "target.pdf"},
        ]
        self.assertTrue(source_matches(sources, "target"))


class KeywordMatchesTest(unittest.TestCase):
    def test_all_present(self):
        result = keyword_matches("机器学习是AI分支", ["机器学习", "AI"])
        self.assertEqual(result, [])

    def test_some_missing(self):
        result = keyword_matches("机器学习是AI分支", ["机器学习", "深度学习"])
        self.assertEqual(result, ["深度学习"])

    def test_all_missing(self):
        result = keyword_matches("hello", ["机器学习", "深度学习"])
        self.assertEqual(len(result), 2)

    def test_empty_keywords(self):
        result = keyword_matches("anything", [])
        self.assertEqual(result, [])

    def test_empty_answer(self):
        result = keyword_matches("", ["keyword"])
        self.assertEqual(result, ["keyword"])

    def test_empty_keyword_item_skipped(self):
        result = keyword_matches("text", ["", "text"])
        self.assertEqual(result, [])


class ForbiddenKeywordMatchesTest(unittest.TestCase):
    def test_present_forbidden_keywords_reported(self):
        result = forbidden_keyword_matches("答案包含错误结论", ["错误", "不存在"])
        self.assertEqual(result, ["错误"])

    def test_empty_items_skipped(self):
        result = forbidden_keyword_matches("text", ["", "missing"])
        self.assertEqual(result, [])


class TraceSummaryTest(unittest.TestCase):
    def test_extract_trace_summary_keeps_retrieval_diagnostics(self):
        summary = extract_trace_summary({
            "query_rewrite": {
                "enabled": True,
                "fallback_enabled": True,
                "fallback_used": True,
                "attempted_query": "bad rewrite",
                "final_query": "original query",
                "contextual_query": "context query",
            },
            "compression": {
                "enabled": True,
                "input_count": 5,
                "compressed_count": 2,
                "protected_count": 1,
                "fallback_reason": "empty_compressed_results",
            },
            "weights": {
                "hybrid_vector": 0.65,
                "hybrid_bm25": 0.35,
                "ignored": "not exported",
            },
        })

        self.assertTrue(summary["query_rewrite"]["fallback_used"])
        self.assertEqual(summary["compression"]["protected_count"], 1)
        self.assertEqual(summary["weights"]["hybrid_vector"], 0.65)
        self.assertNotIn("ignored", summary["weights"])

    def test_format_trace_summary_reports_fallbacks(self):
        lines = format_trace_summary({
            "query_rewrite": {"enabled": True, "fallback_used": True},
            "compression": {
                "enabled": True,
                "input_count": 3,
                "compressed_count": 0,
                "protected_count": 1,
                "fallback_reason": "compression_error",
            },
            "weights": {"hybrid_vector": 0.65},
        })

        joined = "\n".join(lines)
        self.assertIn("fallback_used=True", joined)
        self.assertIn("protected=1", joined)
        self.assertIn("hybrid_vector=0.650", joined)

    def test_extract_top_documents_prefers_trace_final_documents(self):
        retrieve_data = {
            "sources": [{"source": "source-only.md"}],
            "trace": {
                "final_documents": [
                    {"source": "trace.md", "section": "章节", "score": 0.9}
                ]
            },
        }

        result = extract_top_documents(retrieve_data)

        self.assertEqual(result[0]["source"], "trace.md")

    def test_extract_top_documents_falls_back_to_sources(self):
        retrieve_data = {"sources": [{"source": "source-only.md"}], "trace": {}}

        result = extract_top_documents(retrieve_data)

        self.assertEqual(result[0]["source"], "source-only.md")

    def test_format_top_documents_includes_scores(self):
        result = format_top_documents([
            {
                "source": "a.md",
                "section": "章节",
                "score": 0.91,
                "vector_score": 0.8,
                "keyword_score": 0.7,
                "rerank_score": 0.6,
            }
        ])

        self.assertIn("a.md / 章节", result[0])
        self.assertIn("score=0.910", result[0])
        self.assertIn("vector=0.800", result[0])
        self.assertIn("candidate=-", result[0])


class LoadCasesExtendedTest(unittest.TestCase):
    def test_valid_cases(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([
                {"question": "Q1", "expected_keywords": ["k1"]},
                {"question": "Q2", "expected_keywords": ["k2", "k3"]},
            ], f)
            path = Path(f.name)
        try:
            cases = load_cases(path)
            self.assertEqual(len(cases), 2)
            self.assertEqual(cases[1]["expected_keywords"], ["k2", "k3"])
        finally:
            path.unlink()

    def test_not_array_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"question": "not an array"}, f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_missing_question_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"expected_keywords": ["k"]}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_endpoint_case_without_question_valid(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{
                "id": "health",
                "endpoint": "GET /health",
                "question": "",
                "check": "health_returns_healthy",
            }], f)
            path = Path(f.name)
        try:
            cases = load_cases(path)
            self.assertEqual(cases[0]["endpoint"], "GET /health")
        finally:
            path.unlink()

    def test_forbidden_keywords_must_be_array(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1", "forbidden_keywords": "bad"}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_case_without_keywords_valid(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1"}], f)
            path = Path(f.name)
        try:
            cases = load_cases(path)
            self.assertEqual(len(cases), 1)
        finally:
            path.unlink()

    def test_case_with_optional_fields(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{
                "id": "case1",
                "question": "Q1",
                "collection": "my_col",
                "expected_keywords": ["k"],
                "expected_source_contains": "source",
                "expected_top_source_contains": "source",
                "min_top_score": 0.1,
                "expected_candidate_source": "vector",
                "expected_trace": {"query_rewrite": {"fallback_used": False}},
                "tags": ["trace", "baseline"],
            }], f)
            path = Path(f.name)
        try:
            cases = load_cases(path)
            self.assertEqual(cases[0]["id"], "case1")
            self.assertEqual(cases[0]["collection"], "my_col")
            self.assertEqual(cases[0]["tags"], ["trace", "baseline"])
            self.assertEqual(cases[0]["min_top_score"], 0.1)
        finally:
            path.unlink()

    def test_tags_must_be_array(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1", "tags": "trace"}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_min_top_score_must_be_number(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1", "min_top_score": "0.5"}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_expected_trace_must_be_object(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1", "expected_trace": "fallback"}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()

    def test_answer_length_fields_must_be_numbers(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([{"question": "Q1", "min_answer_chars": "short"}], f)
            path = Path(f.name)
        try:
            with self.assertRaises(ValueError):
                load_cases(path)
        finally:
            path.unlink()


class EvaluateCaseTest(unittest.TestCase):
    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_reports_trace_and_keyword_failures(self, mock_post):
        mock_post.side_effect = [
            {
                "success": True,
                "sources": [{"source": "a.md", "vector_score": 0.8}],
                "retrieved_count": 5,
                "selected_count": 1,
                "trace": {
                    "final_documents": [
                        {
                            "source": "a.md",
                            "section": "章节",
                            "score": 0.9,
                            "candidate_source": "vector",
                        }
                    ],
                    "query_rewrite": {
                        "enabled": True,
                        "fallback_enabled": True,
                        "fallback_used": True,
                        "attempted_query": "bad rewrite",
                        "final_query": "Q",
                        "contextual_query": "Q",
                    },
                    "compression": {
                        "enabled": True,
                        "input_count": 3,
                        "compressed_count": 1,
                        "protected_count": 1,
                        "fallback_reason": "",
                    },
                    "weights": {
                        "hybrid_vector": 0.65,
                        "rerank_keyword": 0.25,
                    },
                },
            },
            {
                "success": True,
                "answer": "答案包含 正确 但也包含 错误",
            },
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "expected_source_contains": "a.md",
            "expected_top_source_contains": "a.md",
            "min_top_score": 0.8,
            "expected_candidate_source": "vector",
            "expected_trace": {
                "query_rewrite": {"fallback_used": True},
                "compression": {"protected_count_min": 1, "fallback_reason": ""},
            },
            "expected_keywords": ["正确", "缺失"],
            "forbidden_keywords": ["错误"],
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertFalse(ok)
        self.assertIn("答案缺少关键词: 缺失", errors)
        self.assertIn("答案包含禁用关键词: 错误", errors)
        self.assertEqual(details["retrieved_count"], 5)
        self.assertEqual(details["top_documents"][0]["source"], "a.md")
        self.assertTrue(details["trace_summary"]["query_rewrite"]["fallback_used"])
        self.assertEqual(details["trace_summary"]["compression"]["protected_count"], 1)
        self.assertEqual(details["trace_summary"]["weights"]["hybrid_vector"], 0.65)
        self.assertEqual(
            details["failure_reasons"],
            ["answer_missing_keywords", "answer_forbidden_keywords"],
        )

    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_reports_retrieval_expectation_failures(self, mock_post):
        mock_post.side_effect = [
            {
                "success": True,
                "sources": [{"source": "wrong.md"}],
                "retrieved_count": 1,
                "selected_count": 1,
                "trace": {
                    "final_documents": [
                        {
                            "source": "wrong.md",
                            "section": "其他章节",
                            "score": 0.2,
                            "candidate_source": "bm25",
                        }
                    ],
                    "query_rewrite": {"fallback_used": False},
                    "compression": {
                        "protected_count": 0,
                        "fallback_reason": "compression_error",
                    },
                },
            },
            {
                "success": True,
                "answer": "答案包含 正确",
            },
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "expected_keywords": ["正确"],
            "expected_top_source_contains": "target.md",
            "min_top_score": 0.9,
            "expected_candidate_source": "vector",
            "expected_trace": {
                "query_rewrite": {"fallback_used": True},
                "compression": {"protected_count_min": 1, "fallback_reason": ""},
            },
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertFalse(ok)
        self.assertIn("top_source_miss", details["failure_reasons"])
        self.assertIn("top_score_below_threshold", details["failure_reasons"])
        self.assertIn("candidate_source_mismatch", details["failure_reasons"])
        self.assertIn("trace_expectation_failed", details["failure_reasons"])
        self.assertTrue(any("Top 来源未命中期望" in error for error in errors))
        self.assertTrue(any("Top 分数低于阈值" in error for error in errors))
        self.assertTrue(any("Top 候选来源不匹配" in error for error in errors))
        self.assertTrue(any("Trace query_rewrite.fallback_used 不匹配" in error for error in errors))

    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_reports_answer_length_failures(self, mock_post):
        mock_post.side_effect = [
            {
                "success": True,
                "sources": [{"source": "a.md"}],
                "retrieved_count": 1,
                "selected_count": 1,
                "trace": {"final_documents": [{"source": "a.md", "score": 0.9}]},
            },
            {
                "success": True,
                "answer": "短答",
            },
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "min_answer_chars": 10,
            "max_answer_chars": 1,
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertFalse(ok)
        self.assertIn("answer_too_short", details["failure_reasons"])
        self.assertIn("answer_too_long", details["failure_reasons"])
        self.assertTrue(any("答案长度低于阈值" in error for error in errors))
        self.assertTrue(any("答案长度高于阈值" in error for error in errors))

    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_accepts_answer_length_within_thresholds(self, mock_post):
        mock_post.side_effect = [
            {
                "success": True,
                "sources": [{"source": "a.md"}],
                "retrieved_count": 1,
                "selected_count": 1,
                "trace": {"final_documents": [{"source": "a.md", "score": 0.9}]},
            },
            {
                "success": True,
                "answer": "长度合适的答案",
            },
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "min_answer_chars": 3,
            "max_answer_chars": 20,
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertTrue(ok)
        self.assertEqual(errors, [])
        self.assertEqual(details["failure_reasons"], [])

    @patch("eval.rag_eval.get_json_with_meta", return_value={"status": "healthy"})
    def test_evaluate_endpoint_health_case(self, mock_get):
        ok, errors, details = evaluate_case(
            "http://example.test",
            {"endpoint": "GET /health", "check": "health_returns_healthy"},
            1,
        )

        self.assertTrue(ok)
        self.assertEqual(errors, [])
        self.assertEqual(details["status"], "healthy")

    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_reports_source_miss_and_retrieve_empty(self, mock_post):
        mock_post.side_effect = [
            {
                "success": True,
                "sources": [],
                "retrieved_count": 0,
                "selected_count": 0,
                "trace": {"final_documents": []},
            },
            {
                "success": True,
                "answer": "答案包含 正确",
            },
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "expected_source_contains": "target.md",
            "expected_keywords": ["正确"],
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertFalse(ok)
        self.assertIn("检索结果为空", errors)
        self.assertIn("未命中期望来源: target.md", errors)
        self.assertEqual(details["failure_reasons"], ["retrieve_empty", "source_miss"])

    @patch("eval.rag_eval.get_json_with_meta", return_value={"status": "down"})
    def test_evaluate_endpoint_failure_reports_reason(self, mock_get):
        ok, errors, details = evaluate_case(
            "http://example.test",
            {"endpoint": "GET /health", "check": "health_returns_healthy"},
            1,
        )

        self.assertFalse(ok)
        self.assertIn("endpoint_check_failed", details["failure_reasons"])
        self.assertIn("健康检查状态异常", errors[0])


    @patch("eval.rag_eval.post_json_with_meta")
    def test_evaluate_case_records_request_ids(self, mock_post):
        mock_post.side_effect = [
            ApiResult(
                data={
                    "success": True,
                    "sources": [{"source": "a.md"}],
                    "retrieved_count": 1,
                    "selected_count": 1,
                    "trace": {"final_documents": [{"source": "a.md", "score": 0.9}]},
                },
                request_id="req-retrieve",
                process_time_ms="12",
            ),
            ApiResult(
                data={"success": True, "answer": "答案包含 正确"},
                request_id="req-ask",
                process_time_ms="34",
            ),
        ]
        case = {
            "question": "Q",
            "collection": "default",
            "expected_keywords": ["正确"],
        }

        ok, errors, details = evaluate_case("http://example.test", case, 1)

        self.assertTrue(ok)
        self.assertEqual(errors, [])
        self.assertEqual(details["retrieve_request_id"], "req-retrieve")
        self.assertEqual(details["retrieve_process_time_ms"], "12")
        self.assertEqual(details["ask_request_id"], "req-ask")
        self.assertEqual(details["ask_process_time_ms"], "34")

    @patch(
        "eval.rag_eval.get_json_with_meta",
        return_value=ApiResult(
            data={"status": "healthy"},
            request_id="req-health",
            process_time_ms="9",
        ),
    )
    def test_evaluate_endpoint_records_request_id(self, mock_get):
        ok, errors, details = evaluate_case(
            "http://example.test",
            {"endpoint": "GET /health", "check": "health_returns_healthy"},
            1,
        )

        self.assertTrue(ok)
        self.assertEqual(errors, [])
        self.assertEqual(details["request_id"], "req-health")
        self.assertEqual(details["process_time_ms"], "9")


class StructuredReportTest(unittest.TestCase):
    def test_print_case_result_includes_failure_reasons(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            print_case_result(
                "bad",
                False,
                ["检索结果为空"],
                {
                    "kind": "rag",
                    "retrieved_count": 0,
                    "selected_count": 0,
                    "retrieve_elapsed_ms": 1,
                    "answer_chars": 0,
                    "ask_elapsed_ms": 1,
                    "failure_reasons": ["retrieve_empty"],
                },
            )

        self.assertIn("failure_reasons: retrieve_empty", output.getvalue())

    def test_print_case_result_includes_request_ids_for_failed_rag_case(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            print_case_result(
                "bad",
                False,
                ["retrieve failed"],
                {
                    "kind": "rag",
                    "retrieved_count": 0,
                    "selected_count": 0,
                    "retrieve_elapsed_ms": 1,
                    "answer_chars": 0,
                    "ask_elapsed_ms": 1,
                    "failure_reasons": ["retrieve_empty"],
                    "retrieve_request_id": "req-retrieve",
                    "ask_request_id": "req-ask",
                },
            )

        self.assertIn("request_ids: retrieve=req-retrieve, ask=req-ask", output.getvalue())

    def test_print_case_result_includes_request_id_for_failed_endpoint_case(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            print_case_result(
                "health",
                False,
                ["health failed"],
                {
                    "kind": "endpoint",
                    "elapsed_ms": 1,
                    "failure_reasons": ["endpoint_check_failed"],
                    "request_id": "req-health",
                },
            )

        self.assertIn("request_id: req-health", output.getvalue())

    def test_build_report_summarizes_case_results(self):
        case_results = [
            build_case_result(
                "ok",
                {"question": "Q1", "collection": "default", "tags": ["baseline"]},
                True,
                [],
                {"retrieved_count": 2},
            ),
            build_case_result(
                "bad",
                {"question": "Q2", "collection": "default"},
                False,
                ["答案缺少关键词: k"],
                {"retrieved_count": 0, "failure_reasons": ["answer_missing_keywords"]},
            ),
        ]

        report = build_report(case_results, "http://example.test", Path("cases.json"), 0.0)

        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["passed"], 1)
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(report["summary"]["pass_rate"], 0.5)
        self.assertEqual(report["cases"][0]["tags"], ["baseline"])
        self.assertEqual(report["cases"][1]["errors"], ["答案缺少关键词: k"])
        self.assertEqual(report["cases"][1]["failure_reasons"], ["answer_missing_keywords"])

    def test_write_report_creates_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "reports" / "rag_eval.json"
            report = {"summary": {"total": 1}, "cases": []}

            write_report(report, output_path)

            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["summary"]["total"], 1)


if __name__ == "__main__":
    unittest.main()
