"""
Lightweight RAG evaluation runner.

Usage:
    python eval/rag_eval.py --api-base http://127.0.0.1:8000
    python eval/rag_eval.py --api-base http://127.0.0.1:8000 --api-token your-token

The backend service must already be running. Cases are intentionally simple:
they verify that retrieval/generation endpoints respond, expected sources are
present when configured, and answers contain required keywords.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


DEFAULT_CASES_PATH = Path(__file__).with_name("eval_cases.json")


@dataclass
class ApiResult:
    data: Any
    request_id: str = ""
    process_time_ms: str = ""


def load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("评估用例文件必须是 JSON 数组")
    if not cases:
        raise ValueError("评估用例文件不能为空")
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"第 {index} 个评估用例必须是 JSON 对象")
        endpoint = str(case.get("endpoint") or "").strip()
        if not endpoint and not str(case.get("question") or "").strip():
            raise ValueError(f"第 {index} 个评估用例缺少 question")
        for field_name in ("expected_keywords", "forbidden_keywords", "tags"):
            keywords = case.get(field_name, [])
            if keywords is not None and not isinstance(keywords, list):
                raise ValueError(f"第 {index} 个评估用例的 {field_name} 必须是数组")
        if case.get("expected_trace") is not None and not isinstance(case["expected_trace"], dict):
            raise ValueError(f"第 {index} 个评估用例的 expected_trace 必须是对象")
        if case.get("min_top_score") is not None and not isinstance(case["min_top_score"], (int, float)):
            raise ValueError(f"第 {index} 个评估用例的 min_top_score 必须是数字")
        for field_name in ("min_answer_chars", "max_answer_chars"):
            if case.get(field_name) is not None and not isinstance(case[field_name], (int, float)):
                raise ValueError(f"第 {index} 个评估用例的 {field_name} 必须是数字")
    return cases


def build_headers(api_token: str = "") -> dict[str, str]:
    if not api_token:
        return {}
    return {"Authorization": f"Bearer {api_token}"}


def post_json(
    api_base: str,
    endpoint: str,
    payload: dict[str, Any],
    timeout: int,
    api_token: str = "",
) -> dict[str, Any]:
    response = requests.post(
        f"{api_base.rstrip('/')}/{endpoint.lstrip('/')}",
        json=payload,
        headers=build_headers(api_token),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError(f"{endpoint} 返回值不是 JSON 对象")
    return data


def post_json_with_meta(
    api_base: str,
    endpoint: str,
    payload: dict[str, Any],
    timeout: int,
    api_token: str = "",
) -> ApiResult:
    response = requests.post(
        f"{api_base.rstrip('/')}/{endpoint.lstrip('/')}",
        json=payload,
        headers=build_headers(api_token),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError(f"{endpoint} 返回值不是 JSON 对象")
    return ApiResult(
        data=data,
        request_id=response.headers.get("X-Request-ID", ""),
        process_time_ms=response.headers.get("X-Process-Time-Ms", ""),
    )


def get_json(
    api_base: str,
    endpoint: str,
    timeout: int,
    api_token: str = "",
) -> Any:
    response = requests.get(
        f"{api_base.rstrip('/')}/{endpoint.lstrip('/')}",
        headers=build_headers(api_token),
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def get_json_with_meta(
    api_base: str,
    endpoint: str,
    timeout: int,
    api_token: str = "",
) -> ApiResult:
    response = requests.get(
        f"{api_base.rstrip('/')}/{endpoint.lstrip('/')}",
        headers=build_headers(api_token),
        timeout=timeout,
    )
    response.raise_for_status()
    return ApiResult(
        data=response.json(),
        request_id=response.headers.get("X-Request-ID", ""),
        process_time_ms=response.headers.get("X-Process-Time-Ms", ""),
    )


def _as_api_result(value: Any) -> ApiResult:
    if isinstance(value, ApiResult):
        return value
    return ApiResult(data=value)


def source_matches(sources: list[dict[str, Any]], expected: str) -> bool:
    if not expected:
        return True
    expected_lower = expected.lower()
    for source in sources:
        source_text = " ".join(str(value) for value in source.values()).lower()
        if expected_lower in source_text:
            return True
    return False


def keyword_matches(answer: str, keywords: list[str]) -> list[str]:
    return [keyword for keyword in keywords if keyword and keyword not in answer]


def forbidden_keyword_matches(answer: str, keywords: list[str]) -> list[str]:
    return [keyword for keyword in keywords if keyword and keyword in answer]


def add_failure_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def _optional_text(value: Any) -> str:
    return str(value or "").strip()


def _elapsed_ms(start: float) -> int:
    return int((time.perf_counter() - start) * 1000)


def _safe_number(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{value:.3f}"
    if value in ("", None):
        return "-"
    return str(value)


def extract_trace_summary(trace: dict[str, Any]) -> dict[str, Any]:
    """Extract stable retrieval diagnostics for JSON reports."""
    if not isinstance(trace, dict):
        return {}

    summary: dict[str, Any] = {}
    query_rewrite = trace.get("query_rewrite")
    if isinstance(query_rewrite, dict):
        summary["query_rewrite"] = {
            "enabled": bool(query_rewrite.get("enabled")),
            "fallback_enabled": bool(query_rewrite.get("fallback_enabled")),
            "fallback_used": bool(query_rewrite.get("fallback_used")),
            "attempted_query": str(query_rewrite.get("attempted_query") or "")[:300],
            "final_query": str(query_rewrite.get("final_query") or "")[:300],
            "contextual_query": str(query_rewrite.get("contextual_query") or "")[:300],
        }

    compression = trace.get("compression")
    if isinstance(compression, dict):
        summary["compression"] = {
            "enabled": bool(compression.get("enabled")),
            "input_count": compression.get("input_count", 0),
            "compressed_count": compression.get("compressed_count", 0),
            "protected_count": compression.get("protected_count", 0),
            "fallback_reason": str(compression.get("fallback_reason") or ""),
        }

    weights = trace.get("weights")
    if isinstance(weights, dict):
        summary["weights"] = {
            key: weights.get(key)
            for key in (
                "hybrid_vector",
                "hybrid_bm25",
                "rerank_vector",
                "rerank_keyword",
                "rerank_phrase",
                "keyword_header",
                "keyword_phrase",
            )
            if key in weights
        }

    return summary


def format_trace_summary(summary: dict[str, Any]) -> list[str]:
    """Format trace diagnostics as compact console lines."""
    if not summary:
        return []

    lines: list[str] = []
    query_rewrite = summary.get("query_rewrite")
    if isinstance(query_rewrite, dict):
        lines.append(
            "query_rewrite: "
            f"enabled={query_rewrite.get('enabled')}, "
            f"fallback_used={query_rewrite.get('fallback_used')}"
        )

    compression = summary.get("compression")
    if isinstance(compression, dict):
        fallback_reason = compression.get("fallback_reason") or "-"
        lines.append(
            "compression: "
            f"enabled={compression.get('enabled')}, "
            f"input={compression.get('input_count')}, "
            f"compressed={compression.get('compressed_count')}, "
            f"protected={compression.get('protected_count')}, "
            f"fallback={fallback_reason}"
        )

    weights = summary.get("weights")
    if isinstance(weights, dict) and weights:
        weight_text = ", ".join(
            f"{key}={_safe_number(value)}"
            for key, value in weights.items()
        )
        lines.append(f"weights: {weight_text}")

    return lines


def extract_top_documents(retrieve_data: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    trace = retrieve_data.get("trace") or {}
    documents = trace.get("final_documents") or retrieve_data.get("sources") or []
    if not isinstance(documents, list):
        return []
    return [doc for doc in documents[:limit] if isinstance(doc, dict)]


def format_top_documents(documents: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for index, doc in enumerate(documents, start=1):
        source = doc.get("source") or doc.get("candidate_source") or "未知来源"
        section = doc.get("section") or ""
        section_text = f" / {section}" if section else ""
        score = _safe_number(doc.get("score"))
        vector_score = _safe_number(doc.get("vector_score"))
        keyword_score = _safe_number(doc.get("keyword_score"))
        rerank_score = _safe_number(doc.get("rerank_score"))
        candidate_source = doc.get("candidate_source") or "-"
        lines.append(
            f"{index}. {source}{section_text} "
            f"(score={score}, vector={vector_score}, keyword={keyword_score}, "
            f"rerank={rerank_score}, candidate={candidate_source})"
        )
    return lines


def evaluate_retrieval_expectations(
    case: dict[str, Any],
    top_documents: list[dict[str, Any]],
    trace_summary: dict[str, Any],
    errors: list[str],
    failure_reasons: list[str],
) -> None:
    top_document = top_documents[0] if top_documents else {}

    expected_top_source = _optional_text(case.get("expected_top_source_contains"))
    if expected_top_source and not source_matches([top_document], expected_top_source):
        add_failure_reason(failure_reasons, "top_source_miss")
        errors.append(f"Top 来源未命中期望: {expected_top_source}")

    if case.get("min_top_score") is not None:
        min_top_score = float(case["min_top_score"])
        score = top_document.get("score") if top_document else None
        if not isinstance(score, (int, float)) or float(score) < min_top_score:
            add_failure_reason(failure_reasons, "top_score_below_threshold")
            errors.append(f"Top 分数低于阈值: {score if score is not None else '-'} < {min_top_score}")

    expected_candidate_source = _optional_text(case.get("expected_candidate_source"))
    if expected_candidate_source:
        actual_candidate_source = _optional_text(top_document.get("candidate_source")).lower()
        if actual_candidate_source != expected_candidate_source.lower():
            add_failure_reason(failure_reasons, "candidate_source_mismatch")
            errors.append(
                "Top 候选来源不匹配: "
                f"{actual_candidate_source or '-'} != {expected_candidate_source}"
            )

    expected_trace = case.get("expected_trace") or {}
    if isinstance(expected_trace, dict):
        evaluate_trace_expectations(expected_trace, trace_summary, errors, failure_reasons)


def evaluate_trace_expectations(
    expected_trace: dict[str, Any],
    trace_summary: dict[str, Any],
    errors: list[str],
    failure_reasons: list[str],
) -> None:
    query_rewrite_expected = expected_trace.get("query_rewrite")
    if isinstance(query_rewrite_expected, dict) and "fallback_used" in query_rewrite_expected:
        actual = (trace_summary.get("query_rewrite") or {}).get("fallback_used")
        expected = bool(query_rewrite_expected["fallback_used"])
        if actual is not expected:
            add_failure_reason(failure_reasons, "trace_expectation_failed")
            errors.append(f"Trace query_rewrite.fallback_used 不匹配: {actual} != {expected}")

    compression_expected = expected_trace.get("compression")
    if not isinstance(compression_expected, dict):
        return

    compression_summary = trace_summary.get("compression") or {}
    if "protected_count_min" in compression_expected:
        expected_min = float(compression_expected["protected_count_min"])
        actual_count = compression_summary.get("protected_count")
        if not isinstance(actual_count, (int, float)) or float(actual_count) < expected_min:
            add_failure_reason(failure_reasons, "trace_expectation_failed")
            errors.append(
                "Trace compression.protected_count 低于期望: "
                f"{actual_count if actual_count is not None else '-'} < {expected_min}"
            )
    if "fallback_reason" in compression_expected:
        expected_reason = str(compression_expected["fallback_reason"])
        actual_reason = str(compression_summary.get("fallback_reason") or "")
        if actual_reason != expected_reason:
            add_failure_reason(failure_reasons, "trace_expectation_failed")
            errors.append(
                "Trace compression.fallback_reason 不匹配: "
                f"{actual_reason or '-'} != {expected_reason or '-'}"
            )


def run_endpoint_case(
    api_base: str,
    case: dict[str, Any],
    timeout: int,
    api_token: str = "",
) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    failure_reasons: list[str] = []
    details: dict[str, Any] = {"kind": "endpoint", "failure_reasons": failure_reasons}
    endpoint = str(case.get("endpoint") or "")
    method, _, path = endpoint.partition(" ")
    method = method.upper().strip()
    path = path.strip()

    if method != "GET" or not path:
        add_failure_reason(failure_reasons, "endpoint_check_failed")
        return False, [f"暂不支持的 endpoint 用例: {endpoint}"], details

    start = time.perf_counter()
    endpoint_result = _as_api_result(get_json_with_meta(api_base, path, timeout, api_token))
    data = endpoint_result.data
    details["elapsed_ms"] = _elapsed_ms(start)
    details["request_id"] = endpoint_result.request_id
    details["process_time_ms"] = endpoint_result.process_time_ms
    details["check"] = case.get("check", "")

    check = case.get("check")
    if check == "collection_list_returns_array":
        collections = data.get("collections") if isinstance(data, dict) else data
        if not isinstance(collections, list):
            add_failure_reason(failure_reasons, "endpoint_check_failed")
            errors.append("知识库列表不是数组")
        else:
            details["collection_count"] = len(collections)
    elif check == "health_returns_healthy":
        if not isinstance(data, dict) or data.get("status") not in {"healthy", "ok"}:
            add_failure_reason(failure_reasons, "endpoint_check_failed")
            errors.append(f"健康检查状态异常: {data}")
        else:
            details["status"] = data.get("status")
    elif check:
        add_failure_reason(failure_reasons, "endpoint_check_failed")
        errors.append(f"未知检查项: {check}")

    return not errors, errors, details


def evaluate_case(
    api_base: str,
    case: dict[str, Any],
    timeout: int,
    api_token: str = "",
) -> tuple[bool, list[str], dict[str, Any]]:
    if case.get("endpoint"):
        return run_endpoint_case(api_base, case, timeout, api_token)

    errors: list[str] = []
    failure_reasons: list[str] = []
    details: dict[str, Any] = {
        "kind": "rag",
        "collection": case.get("collection", "default"),
        "retrieved_count": 0,
        "selected_count": 0,
        "top_documents": [],
        "failure_reasons": failure_reasons,
        "retrieve_elapsed_ms": 0,
        "ask_elapsed_ms": 0,
    }
    payload = {
        "question": case["question"],
        "collection_name": case.get("collection", "default"),
    }

    retrieve_start = time.perf_counter()
    retrieve_result = _as_api_result(post_json_with_meta(api_base, "/retrieve", payload, timeout, api_token))
    retrieve_data = retrieve_result.data
    details["retrieve_elapsed_ms"] = _elapsed_ms(retrieve_start)
    details["retrieve_request_id"] = retrieve_result.request_id
    details["retrieve_process_time_ms"] = retrieve_result.process_time_ms
    if not retrieve_data.get("success"):
        errors.append(f"检索失败: {retrieve_data.get('error')}")

    sources = retrieve_data.get("sources") or []
    top_documents = extract_top_documents(retrieve_data)
    trace = retrieve_data.get("trace") or {}
    details["retrieved_count"] = retrieve_data.get("retrieved_count", 0)
    details["selected_count"] = retrieve_data.get("selected_count", len(sources))
    details["top_documents"] = top_documents
    details["trace_summary"] = extract_trace_summary(trace)
    details["top_score"] = top_documents[0].get("score") if top_documents else None
    if not sources and not top_documents:
        add_failure_reason(failure_reasons, "retrieve_empty")
        errors.append("检索结果为空")
    expected_source = str(case.get("expected_source_contains") or "")
    if not source_matches(sources + top_documents, expected_source):
        add_failure_reason(failure_reasons, "source_miss")
        errors.append(f"未命中期望来源: {expected_source}")
    evaluate_retrieval_expectations(
        case,
        top_documents,
        details["trace_summary"],
        errors,
        failure_reasons,
    )

    ask_start = time.perf_counter()
    answer_result = _as_api_result(post_json_with_meta(api_base, "/ask", payload, timeout, api_token))
    answer_data = answer_result.data
    details["ask_elapsed_ms"] = _elapsed_ms(ask_start)
    details["ask_request_id"] = answer_result.request_id
    details["ask_process_time_ms"] = answer_result.process_time_ms
    if not answer_data.get("success"):
        errors.append(f"问答失败: {answer_data.get('error')}")

    answer = str(answer_data.get("answer") or "")
    missing_keywords = keyword_matches(answer, case.get("expected_keywords") or [])
    if missing_keywords:
        add_failure_reason(failure_reasons, "answer_missing_keywords")
        errors.append(f"答案缺少关键词: {', '.join(missing_keywords)}")
    forbidden_keywords = forbidden_keyword_matches(answer, case.get("forbidden_keywords") or [])
    if forbidden_keywords:
        add_failure_reason(failure_reasons, "answer_forbidden_keywords")
        errors.append(f"答案包含禁用关键词: {', '.join(forbidden_keywords)}")
    details["missing_keywords"] = missing_keywords
    details["forbidden_keywords"] = forbidden_keywords
    details["answer_chars"] = len(answer)
    min_answer_chars = case.get("min_answer_chars")
    if min_answer_chars is not None and len(answer) < float(min_answer_chars):
        add_failure_reason(failure_reasons, "answer_too_short")
        errors.append(f"答案长度低于阈值: {len(answer)} < {float(min_answer_chars):g}")
    max_answer_chars = case.get("max_answer_chars")
    if max_answer_chars is not None and len(answer) > float(max_answer_chars):
        add_failure_reason(failure_reasons, "answer_too_long")
        errors.append(f"答案长度高于阈值: {len(answer)} > {float(max_answer_chars):g}")

    return not errors, errors, details


def run_case(api_base: str, case: dict[str, Any], timeout: int, api_token: str = "") -> tuple[bool, list[str]]:
    ok, errors, _ = evaluate_case(api_base, case, timeout, api_token)
    return ok, errors


def print_case_result(case_id: str, ok: bool, errors: list[str], details: dict[str, Any]) -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {case_id}")

    if details.get("kind") == "rag":
        print(
            "  retrieve: "
            f"{details.get('retrieved_count', 0)} candidates, "
            f"{details.get('selected_count', 0)} selected, "
            f"{details.get('retrieve_elapsed_ms', 0)} ms"
        )
        print(f"  ask: {details.get('answer_chars', 0)} chars, {details.get('ask_elapsed_ms', 0)} ms")
        if not ok and details.get("failure_reasons"):
            print(f"  failure_reasons: {', '.join(details['failure_reasons'])}")
        if not ok and (details.get("retrieve_request_id") or details.get("ask_request_id")):
            print(
                "  request_ids: "
                f"retrieve={details.get('retrieve_request_id') or '-'}, "
                f"ask={details.get('ask_request_id') or '-'}"
            )
        top_lines = format_top_documents(details.get("top_documents") or [])
        if top_lines:
            print("  top sources:")
            for line in top_lines:
                print(f"    {line}")
        trace_lines = format_trace_summary(details.get("trace_summary") or {})
        if trace_lines:
            print("  diagnostics:")
            for line in trace_lines:
                print(f"    {line}")
    elif details.get("kind") == "endpoint":
        summary_parts = [f"{details.get('elapsed_ms', 0)} ms"]
        if "status" in details:
            summary_parts.append(f"status={details['status']}")
        if "collection_count" in details:
            summary_parts.append(f"collections={details['collection_count']}")
        print(f"  endpoint: {', '.join(summary_parts)}")
        if not ok and details.get("failure_reasons"):
            print(f"  failure_reasons: {', '.join(details['failure_reasons'])}")
        if not ok and details.get("request_id"):
            print(f"  request_id: {details['request_id']}")

    for error in errors:
        print(f"  - {error}")


def build_case_result(case_id: str, case: dict[str, Any], ok: bool, errors: list[str], details: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case_id,
        "question": case.get("question", ""),
        "collection": case.get("collection", "default"),
        "endpoint": case.get("endpoint", ""),
        "tags": case.get("tags", []),
        "success": ok,
        "errors": errors,
        "failure_reasons": details.get("failure_reasons", []),
        "details": details,
    }


def build_report(
    case_results: list[dict[str, Any]],
    api_base: str,
    cases_path: Path,
    started_at: float,
) -> dict[str, Any]:
    total = len(case_results)
    passed = sum(1 for item in case_results if item.get("success"))
    failed = total - passed
    elapsed_ms = _elapsed_ms(started_at)
    return {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) if total else 0.0,
            "elapsed_ms": elapsed_ms,
        },
        "meta": {
            "api_base": api_base,
            "cases_path": str(cases_path),
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        },
        "cases": case_results,
    }


def write_report(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 RAG 基础评估用例")
    parser.add_argument("--api-base", default="http://127.0.0.1:8000")
    parser.add_argument("--api-token", default=os.getenv("API_TOKEN", ""))
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output-json", type=Path, default=None, help="保存结构化评测报告 JSON")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    started_at = time.perf_counter()
    passed = 0
    case_results: list[dict[str, Any]] = []

    for case in cases:
        case_id = str(case.get("id") or case.get("question", "")[:30])
        try:
            ok, errors, details = evaluate_case(args.api_base, case, args.timeout, args.api_token)
        except Exception as exc:
            ok = False
            errors = [str(exc)]
            details = {}

        if ok:
            passed += 1
        case_results.append(build_case_result(case_id, case, ok, errors, details))
        print_case_result(case_id, ok, errors, details)

    total = len(cases)
    print(f"\n评估结果: {passed}/{total} 通过")
    report = build_report(case_results, args.api_base, args.cases, started_at)
    if args.output_json:
        write_report(report, args.output_json)
        print(f"结构化报告已保存: {args.output_json}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
