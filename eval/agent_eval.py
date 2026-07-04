"""
Lightweight Agent evaluation runner.

Usage:
    python eval/agent_eval.py --api-base http://127.0.0.1:8000
    python eval/agent_eval.py --api-base http://127.0.0.1:8000 --output-json eval/agent_eval_report.json

The backend service must already be running. Cases focus on Agent routing,
tool usage, debug trace, and answer guardrails. They are intentionally small
so they can be used before demos without changing RAG or Agent strategy.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


DEFAULT_CASES_PATH = Path(__file__).with_name("agent_eval_cases.json")


@dataclass
class ApiResult:
    data: dict[str, Any]
    request_id: str = ""
    process_time_ms: str = ""


def build_headers(api_token: str = "") -> dict[str, str]:
    if not api_token:
        return {}
    return {"Authorization": f"Bearer {api_token}"}


def load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("Agent eval cases must be a JSON array")
    if not cases:
        raise ValueError("Agent eval cases must not be empty")
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"Agent eval case #{index} must be an object")
        if not str(case.get("id") or "").strip():
            raise ValueError(f"Agent eval case #{index} is missing id")
        if not str(case.get("question") or "").strip():
            raise ValueError(f"Agent eval case #{index} is missing question")
        for field_name in (
            "forbidden_first_tools",
            "required_allowed_tools",
            "expected_answer_sections",
            "expected_debug_fields",
            "forbidden_answer_keywords",
            "expected_answer_keywords",
            "tags",
        ):
            value = case.get(field_name, [])
            if value is not None and not isinstance(value, list):
                raise ValueError(f"Agent eval case #{index} field {field_name} must be a list")
    return cases


def post_agent_with_meta(
    api_base: str,
    payload: dict[str, Any],
    timeout: int,
    api_token: str = "",
) -> ApiResult:
    response = requests.post(
        f"{api_base.rstrip('/')}/agent",
        json=payload,
        headers=build_headers(api_token),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("/agent response must be a JSON object")
    return ApiResult(
        data=data,
        request_id=response.headers.get("X-Request-ID", ""),
        process_time_ms=response.headers.get("X-Process-Time-Ms", ""),
    )


def _elapsed_ms(start: float) -> int:
    return int((time.perf_counter() - start) * 1000)


def _get_path(data: Any, dotted_path: str) -> Any:
    current = data
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _first_tool(data: dict[str, Any], debug_info: dict[str, Any]) -> str:
    tool_sequence = debug_info.get("tool_sequence")
    if isinstance(tool_sequence, list) and tool_sequence:
        return str(tool_sequence[0])
    agent_steps = data.get("agent_steps")
    if isinstance(agent_steps, list) and agent_steps:
        first_step = agent_steps[0]
        if isinstance(first_step, dict):
            return str(first_step.get("tool") or "")
    return ""


def _category(debug_info: dict[str, Any]) -> str:
    routing_decision = debug_info.get("routing_decision")
    if isinstance(routing_decision, dict) and routing_decision.get("category"):
        return str(routing_decision["category"])
    tool_policy = debug_info.get("tool_policy")
    if isinstance(tool_policy, dict) and tool_policy.get("category"):
        return str(tool_policy["category"])
    return ""


def _allowed_tools(debug_info: dict[str, Any]) -> list[str]:
    routing_decision = debug_info.get("routing_decision")
    if isinstance(routing_decision, dict) and isinstance(routing_decision.get("allowed_tools"), list):
        return [str(tool) for tool in routing_decision["allowed_tools"]]
    return []


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def evaluate_case(
    case: dict[str, Any],
    api_base: str,
    collection_name: str,
    timeout: int,
    api_token: str = "",
) -> dict[str, Any]:
    started = time.perf_counter()
    errors: list[str] = []
    failure_reasons: list[str] = []
    case_id = str(case.get("id") or "")
    payload = {
        "question": case["question"],
        "collection_name": case.get("collection_name") or collection_name,
        "chat_history": case.get("chat_history", []),
        "debug": True,
    }

    try:
        api_result = post_agent_with_meta(api_base, payload, timeout, api_token)
        data = api_result.data
    except Exception as exc:
        return {
            "id": case_id,
            "passed": False,
            "errors": [str(exc)],
            "failure_reasons": ["endpoint_check_failed"],
            "details": {"elapsed_ms": _elapsed_ms(started)},
        }

    debug_info = data.get("debug_info") if isinstance(data.get("debug_info"), dict) else {}
    answer = str(data.get("answer") or "")
    first_tool = _first_tool(data, debug_info)
    category = _category(debug_info)
    allowed_tools = _allowed_tools(debug_info)

    if data.get("success") is False:
        errors.append(str(data.get("error") or "Agent returned success=false"))
        _append_unique(failure_reasons, "agent_failed")

    expected_category = str(case.get("expected_category") or "")
    if expected_category and category != expected_category:
        errors.append(f"category mismatch: {category or '-'} != {expected_category}")
        _append_unique(failure_reasons, "category_mismatch")

    expected_first_tool = str(case.get("expected_first_tool") or "")
    if expected_first_tool and first_tool != expected_first_tool:
        errors.append(f"first tool mismatch: {first_tool or '-'} != {expected_first_tool}")
        _append_unique(failure_reasons, "first_tool_mismatch")

    forbidden_first_tools = [str(tool) for tool in case.get("forbidden_first_tools", [])]
    if first_tool and first_tool in forbidden_first_tools:
        errors.append(f"forbidden first tool used: {first_tool}")
        _append_unique(failure_reasons, "forbidden_first_tool")

    required_allowed_tools = [str(tool) for tool in case.get("required_allowed_tools", [])]
    missing_allowed_tools = [tool for tool in required_allowed_tools if tool not in allowed_tools]
    if missing_allowed_tools:
        errors.append(f"allowed tools missing: {', '.join(missing_allowed_tools)}")
        _append_unique(failure_reasons, "allowed_tools_missing")

    missing_sections = [
        str(section)
        for section in case.get("expected_answer_sections", [])
        if section and str(section) not in answer
    ]
    if missing_sections:
        errors.append(f"answer missing sections: {', '.join(missing_sections)}")
        _append_unique(failure_reasons, "answer_missing_sections")

    missing_keywords = [
        str(keyword)
        for keyword in case.get("expected_answer_keywords", [])
        if keyword and str(keyword) not in answer
    ]
    if missing_keywords:
        errors.append(f"answer missing keywords: {', '.join(missing_keywords)}")
        _append_unique(failure_reasons, "answer_missing_keywords")

    forbidden_keywords = [
        str(keyword)
        for keyword in case.get("forbidden_answer_keywords", [])
        if keyword and str(keyword) in answer
    ]
    if forbidden_keywords:
        errors.append(f"answer contains forbidden keywords: {', '.join(forbidden_keywords)}")
        _append_unique(failure_reasons, "answer_forbidden_keywords")

    missing_debug_fields = [
        str(path)
        for path in case.get("expected_debug_fields", [])
        if _get_path(debug_info, str(path)) in (None, "")
    ]
    if missing_debug_fields:
        errors.append(f"debug fields missing: {', '.join(missing_debug_fields)}")
        _append_unique(failure_reasons, "debug_field_missing")

    details = {
        "request_id": api_result.request_id,
        "process_time_ms": api_result.process_time_ms,
        "elapsed_ms": _elapsed_ms(started),
        "success": bool(data.get("success")),
        "answer_chars": len(answer),
        "category": category,
        "first_tool": first_tool,
        "allowed_tools": allowed_tools,
        "tool_sequence": debug_info.get("tool_sequence", []),
        "routing_decision": debug_info.get("routing_decision", {}),
        "evidence_summary": debug_info.get("evidence_summary", {}),
        "search_trace": debug_info.get("search_trace", {}),
        "fallback_reason": debug_info.get("fallback_reason", ""),
        "fallback_used": debug_info.get("fallback_used", ""),
    }

    return {
        "id": case_id,
        "passed": not errors,
        "errors": errors,
        "failure_reasons": failure_reasons,
        "details": details,
        "tags": case.get("tags", []),
    }


def build_report(
    cases: list[dict[str, Any]],
    api_base: str,
    collection_name: str,
    timeout: int,
    api_token: str = "",
) -> dict[str, Any]:
    started = time.perf_counter()
    results = [
        evaluate_case(case, api_base, collection_name, timeout, api_token)
        for case in cases
    ]
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    reason_counts: dict[str, int] = {}
    for result in results:
        for reason in result.get("failure_reasons", []):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    return {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total else 0,
            "elapsed_ms": _elapsed_ms(started),
            "failure_reason_counts": reason_counts,
        },
        "results": results,
    }


def print_result(result: dict[str, Any]) -> None:
    marker = "PASS" if result["passed"] else "FAIL"
    details = result.get("details", {})
    print(
        f"[{marker}] {result['id']} "
        f"category={details.get('category') or '-'} "
        f"first_tool={details.get('first_tool') or '-'} "
        f"request_id={details.get('request_id') or '-'}"
    )
    if not result["passed"]:
        reasons = ", ".join(result.get("failure_reasons") or []) or "-"
        print(f"  failure_reasons: {reasons}")
        for error in result.get("errors", []):
            print(f"  - {error}")


def write_report(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Agent routing/debug eval cases.")
    parser.add_argument("--api-base", default="http://127.0.0.1:8000", help="FastAPI base URL")
    parser.add_argument("--api-token", default=os.getenv("API_TOKEN", ""), help="Optional API token")
    parser.add_argument("--cases", default=str(DEFAULT_CASES_PATH), help="Agent eval cases JSON path")
    parser.add_argument("--collection-name", default="default", help="Collection name used by cases without override")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds")
    parser.add_argument("--output-json", default="", help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_cases(Path(args.cases))
    report = build_report(
        cases=cases,
        api_base=args.api_base,
        collection_name=args.collection_name,
        timeout=args.timeout,
        api_token=args.api_token,
    )
    for result in report["results"]:
        print_result(result)
    summary = report["summary"]
    print(
        "Agent eval summary: "
        f"{summary['passed']}/{summary['total']} passed "
        f"({summary['pass_rate']:.0%})"
    )
    if args.output_json:
        write_report(report, Path(args.output_json))
        print(f"Wrote report: {args.output_json}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
