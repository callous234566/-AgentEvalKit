"""Read-only backend release checks for the personal RAG assistant.

The script is intentionally conservative: it reports risky repository state,
checks Chroma/mapping consistency, and optionally verifies FastAPI health. It
does not modify files, Chroma data, or runtime configuration.
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_UNSAFE_TRACKED_PATTERNS = (
    ".env",
    "chroma_db/**",
    "chroma_db_backup_*/**",
    "chroma_db_dim384_*/**",
    "chroma_export_*.json",
    "eval/rag_eval_report.json",
    "logs/**",
    ".runtime_logs/**",
    ".runlogs/**",
    "outputs/**",
    "data/**",
    ".cache/**",
    ".pytest_cache/**",
    ".claude/settings.local.json",
    "vector_store.restore.tmp",
)

SECRET_ASSIGNMENT_RE = re.compile(
    r"(?m)^[^\S\r\n]*(LLM_API_KEY|DEEPSEEK_API_KEY|TAVILY_API_KEY|API_TOKEN)[^\S\r\n]*=[^\S\r\n]*([^\s#]+)"
)
BEARER_RE = re.compile(r"(?i)\bBearer\s+([A-Za-z0-9._\-]{20,})")
SECRET_LITERAL_RE = re.compile(r"^[A-Za-z0-9._\-]+$")
PLACEHOLDER_MARKERS = (
    "",
    "your",
    "example",
    "placeholder",
    "change-me",
    "changeme",
    "sk-your-api-key-here",
    "your-token",
    "<token>",
)
TEXT_FILE_EXTENSIONS = {
    ".env",
    ".example",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".ps1",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}


@contextlib.contextmanager
def suppress_native_stderr():
    """Silence noisy native-library stderr output during read-only Chroma probes."""
    try:
        stderr_fd = sys.stderr.fileno()
    except (AttributeError, OSError):
        yield
        return

    saved_fd = os.dup(stderr_fd)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(devnull_fd, stderr_fd)
        yield
    finally:
        os.dup2(saved_fd, stderr_fd)
        os.close(saved_fd)
        os.close(devnull_fd)


@dataclass
class CheckReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        self.info.append(message)


def normalize_path(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def run_git_ls_files(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            capture_output=True,
            text=False,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    raw = completed.stdout.decode("utf-8", errors="replace")
    return [item for item in raw.split("\0") if item]


def find_unsafe_tracked_files(
    tracked_files: Iterable[str],
    patterns: Iterable[str] = DEFAULT_UNSAFE_TRACKED_PATTERNS,
) -> list[str]:
    unsafe = []
    normalized_patterns = [normalize_path(pattern) for pattern in patterns]
    for tracked in tracked_files:
        path = normalize_path(tracked)
        if any(fnmatch.fnmatch(path, pattern) for pattern in normalized_patterns):
            unsafe.append(path)
    return sorted(set(unsafe))


def is_text_candidate(path: Path) -> bool:
    if path.name == ".env":
        return True
    suffixes = {suffix.lower() for suffix in path.suffixes}
    return bool(suffixes & TEXT_FILE_EXTENSIONS)


def looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().strip("\"'").lower()
    if not normalized:
        return True
    return any(marker and marker in normalized for marker in PLACEHOLDER_MARKERS)


def looks_like_real_secret_literal(value: str) -> bool:
    raw = value.strip().rstrip(",)")
    if "os.getenv" in raw or "os.environ" in raw:
        return False
    normalized = raw.strip().strip("\"'").strip()
    if looks_like_placeholder(normalized):
        return False
    if normalized.startswith(("sk-", "tvly-")):
        return len(normalized) >= 16
    return len(normalized) >= 20 and bool(SECRET_LITERAL_RE.fullmatch(normalized))


def scan_tracked_secret_like_values(root: Path, tracked_files: Iterable[str]) -> list[str]:
    findings: list[str] = []
    for tracked in tracked_files:
        rel_path = Path(tracked)
        path = root / rel_path
        if not path.is_file() or not is_text_candidate(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError:
            continue

        for match in SECRET_ASSIGNMENT_RE.finditer(text):
            name, value = match.groups()
            if looks_like_real_secret_literal(value):
                findings.append(f"{normalize_path(tracked)}:{match.start()} {name}=<redacted>")

        for match in BEARER_RE.finditer(text):
            token = match.group(1)
            if not looks_like_placeholder(token):
                findings.append(f"{normalize_path(tracked)}:{match.start()} Bearer <redacted>")
    return sorted(set(findings))


def load_mapping(mapping_file: Path) -> tuple[dict[str, str], str | None]:
    if not mapping_file.exists():
        return {}, None
    try:
        data = json.loads(mapping_file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report the exact parse failure.
        return {}, str(exc)
    if not isinstance(data, dict):
        return {}, "mapping file root is not an object"
    invalid = [key for key, value in data.items() if not isinstance(key, str) or not isinstance(value, str)]
    if invalid:
        return {}, f"mapping contains non-string entries: {invalid[:3]}"
    return data, None


def list_chroma_collections(chroma_path: Path) -> tuple[list[str], str | None]:
    if not chroma_path.exists():
        return [], "Chroma path does not exist"
    try:
        with suppress_native_stderr():
            from chromadb import PersistentClient

            client = PersistentClient(path=str(chroma_path))
            names = [
                item if isinstance(item, str) else str(getattr(item, "name", ""))
                for item in client.list_collections()
            ]
        return sorted(name for name in names if name), None
    except Exception as exc:  # noqa: BLE001 - this is a release diagnostic.
        return [], str(exc)


def check_mapping_consistency(
    mapping: dict[str, str],
    collection_names: Iterable[str],
) -> tuple[list[str], list[str]]:
    collection_set = set(collection_names)
    mapped_internal = set(mapping.values())
    missing_mapped = sorted(
        f"{user_name}->{internal_name}"
        for user_name, internal_name in mapping.items()
        if internal_name not in collection_set
    )
    orphan_hashed = sorted(
        collection_name
        for collection_name in collection_set
        if collection_name.startswith("kb_") and collection_name not in mapped_internal
    )
    return missing_mapped, orphan_hashed


def remove_missing_mapping_entries(
    mapping_file: Path,
    mapping: dict[str, str],
    collection_names: Iterable[str],
) -> list[str]:
    """Remove mapping entries whose internal Chroma collection no longer exists."""
    collection_set = set(collection_names)
    cleaned = {
        user_name: internal_name
        for user_name, internal_name in mapping.items()
        if internal_name in collection_set
    }
    removed = sorted(set(mapping) - set(cleaned))
    if not removed:
        return []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = mapping_file.with_name(f"{mapping_file.stem}.backup_{timestamp}{mapping_file.suffix}")
    backup_file.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    mapping_file.write_text(
        json.dumps(cleaned, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    mapping.clear()
    mapping.update(cleaned)
    return removed


def check_health(api_base: str, api_token: str, timeout: float) -> tuple[dict, str | None]:
    url = api_base.rstrip("/") + "/health"
    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return {
                "status_code": response.status,
                "request_id": response.headers.get("X-Request-ID", ""),
                "process_time_ms": response.headers.get("X-Process-Time-Ms", ""),
                "payload": payload,
            }, None
    except HTTPError as exc:
        return {}, f"HTTP {exc.code}"
    except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return {}, str(exc)


def build_report(args: argparse.Namespace) -> CheckReport:
    root = Path(args.root).resolve()
    report = CheckReport()
    report.add_info(f"project_root={root}")

    tracked_files = run_git_ls_files(root)
    if not tracked_files:
        report.add_warning("git tracked file list is empty or unavailable")
    else:
        unsafe = find_unsafe_tracked_files(tracked_files)
        if unsafe:
            report.add_error("unsafe tracked files: " + ", ".join(unsafe[:20]))
        else:
            report.add_info("git tracked file hygiene passed")

        secret_findings = scan_tracked_secret_like_values(root, tracked_files)
        if secret_findings:
            report.add_error("secret-like tracked values: " + ", ".join(secret_findings[:20]))
        else:
            report.add_info("tracked secret scan passed")

    chroma_path = (root / args.chroma_db_path).resolve()
    mapping_file = chroma_path / "collection_name_mapping.json"
    mapping, mapping_error = load_mapping(mapping_file)
    if mapping_error:
        report.add_error(f"mapping JSON invalid: {mapping_file} ({mapping_error})")
    else:
        report.add_info(f"mapping entries={len(mapping)}")

    collection_names, chroma_error = list_chroma_collections(chroma_path)
    if chroma_error:
        report.add_warning(f"Chroma collection listing skipped/failed: {chroma_error}")
    else:
        report.add_info(f"Chroma collections={len(collection_names)}")
        missing_mapped, orphan_hashed = check_mapping_consistency(mapping, collection_names)
        if missing_mapped:
            if args.fix_missing_mapping:
                removed = remove_missing_mapping_entries(mapping_file, mapping, collection_names)
                report.add_info(
                    "removed missing mapping entries: "
                    f"count={len(removed)} backup_created=true"
                )
            else:
                report.add_warning(
                    "mapping points to missing Chroma collections: "
                    f"count={len(missing_mapped)}"
                )
        if orphan_hashed:
            report.add_warning(
                "unmapped hashed Chroma collections: "
                f"count={len(orphan_hashed)}"
            )

    if not args.no_health:
        health, health_error = check_health(args.api_base, args.api_token or os.getenv("API_TOKEN", ""), args.timeout)
        if health_error:
            report.add_error(f"health check failed: {health_error}")
        elif health.get("payload", {}).get("status") != "healthy":
            report.add_error(f"health check returned non-healthy payload: {health.get('payload')}")
        else:
            report.add_info(
                "health ok "
                f"status_code={health.get('status_code')} "
                f"request_id={health.get('request_id') or '-'} "
                f"process_time_ms={health.get('process_time_ms') or '-'}"
            )

    return report


def print_report(report: CheckReport) -> None:
    status = "PASS" if report.ok else "FAIL"
    print(f"Backend release check: {status}")
    for label, items in (("ERROR", report.errors), ("WARNING", report.warnings), ("INFO", report.info)):
        for item in items:
            print(f"[{label}] {item}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run read-only backend release checks.")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], help="project root")
    parser.add_argument("--chroma-db-path", default=os.getenv("CHROMA_DB_PATH", "./chroma_db"))
    parser.add_argument("--api-base", default="http://127.0.0.1:8000")
    parser.add_argument("--api-token", default="")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--no-health", action="store_true", help="skip FastAPI /health check")
    parser.add_argument(
        "--fix-missing-mapping",
        action="store_true",
        help="remove mapping entries whose Chroma collection is missing; creates a backup first",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args)
    print_report(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
