import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts import check_backend_release as release_check


class BackendReleaseCheckTest(unittest.TestCase):
    def test_detects_unsafe_tracked_files(self):
        tracked = [
            "main.py",
            ".env",
            "chroma_db/chroma.sqlite3",
            "eval/rag_eval_report.json",
            "rag/vector_store.py",
        ]

        unsafe = release_check.find_unsafe_tracked_files(tracked)

        self.assertEqual(
            unsafe,
            [".env", "chroma_db/chroma.sqlite3", "eval/rag_eval_report.json"],
        )

    def test_secret_scan_allows_placeholders_and_flags_real_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bearer_token = "real-token-value-1234567890"
            example = root / ".env.example"
            example.write_text(
                "LLM_API_KEY=sk-your-api-key-here\n"
                "TAVILY_API_KEY=\n"
                "API_TOKEN=your-token\n",
                encoding="utf-8",
            )
            env = root / "config.env"
            env.write_text(
                "LLM_API_KEY=sk-real-secret-value-123456\n"
                f"Authorization: Bearer {bearer_token}\n",
                encoding="utf-8",
            )

            findings = release_check.scan_tracked_secret_like_values(
                root,
                [".env.example", "config.env"],
            )

        self.assertEqual(len(findings), 2)
        self.assertTrue(any("LLM_API_KEY=<redacted>" in item for item in findings))
        self.assertTrue(any("Bearer <redacted>" in item for item in findings))

    def test_secret_scan_ignores_source_env_reads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "config.py"
            source.write_text(
                'LLM_API_KEY = os.getenv("LLM_API_KEY", "")\n'
                'API_TOKEN = os.getenv("API_TOKEN", "").strip()\n'
                'TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")\n',
                encoding="utf-8",
            )

            findings = release_check.scan_tracked_secret_like_values(root, ["config.py"])

        self.assertEqual(findings, [])

    def test_load_mapping_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mapping_file = Path(temp_dir) / "collection_name_mapping.json"
            mapping_file.write_text("{broken", encoding="utf-8")

            mapping, error = release_check.load_mapping(mapping_file)

        self.assertEqual(mapping, {})
        self.assertIsNotNone(error)

    def test_mapping_consistency_reports_missing_and_orphan_hashed_collections(self):
        missing, orphan = release_check.check_mapping_consistency(
            {
                "RAG技术原理": "kb_rag",
                "项目说明": "kb_project",
            },
            ["kb_rag", "kb_orphan", "default"],
        )

        self.assertEqual(missing, ["项目说明->kb_project"])
        self.assertEqual(orphan, ["kb_orphan"])

    def test_remove_missing_mapping_entries_creates_backup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mapping_file = Path(temp_dir) / "collection_name_mapping.json"
            mapping = {
                "keep": "kb_keep",
                "remove": "kb_missing",
            }
            mapping_file.write_text(
                json.dumps(mapping, ensure_ascii=False),
                encoding="utf-8",
            )

            removed = release_check.remove_missing_mapping_entries(
                mapping_file,
                mapping,
                ["kb_keep"],
            )

            saved = json.loads(mapping_file.read_text(encoding="utf-8"))
            backups = list(Path(temp_dir).glob("collection_name_mapping.backup_*.json"))

        self.assertEqual(removed, ["remove"])
        self.assertEqual(saved, {"keep": "kb_keep"})
        self.assertEqual(mapping, {"keep": "kb_keep"})
        self.assertEqual(len(backups), 1)

    @patch("scripts.check_backend_release.urlopen")
    def test_health_check_captures_request_meta(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        response.headers = {
            "X-Request-ID": "req-release-check",
            "X-Process-Time-Ms": "12",
        }
        response.read.return_value = json.dumps({"status": "healthy"}).encode("utf-8")
        response.__enter__.return_value = response
        mock_urlopen.return_value = response

        health, error = release_check.check_health("http://127.0.0.1:8000", "", 1)

        self.assertIsNone(error)
        self.assertEqual(health["request_id"], "req-release-check")
        self.assertEqual(health["process_time_ms"], "12")
        self.assertEqual(health["payload"]["status"], "healthy")

    @patch("scripts.check_backend_release.check_health")
    @patch("scripts.check_backend_release.list_chroma_collections")
    @patch("scripts.check_backend_release.run_git_ls_files")
    def test_build_report_fails_on_tracked_secret_and_health_failure(
        self,
        mock_git_files,
        mock_collections,
        mock_health,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            real_key = "sk-real-secret-value-123456"
            (root / "config.env").write_text(
                f"LLM_API_KEY={real_key}\n",
                encoding="utf-8",
            )
            chroma = root / "chroma_db"
            chroma.mkdir()
            (chroma / "collection_name_mapping.json").write_text(
                json.dumps({"RAG技术原理": "kb_rag"}, ensure_ascii=False),
                encoding="utf-8",
            )

            mock_git_files.return_value = ["config.env"]
            mock_collections.return_value = (["kb_rag"], None)
            mock_health.return_value = ({}, "connection refused")

            args = release_check.parse_args(
                [
                    "--root",
                    str(root),
                    "--api-base",
                    "http://127.0.0.1:8000",
                ]
            )
            report = release_check.build_report(args)

        self.assertFalse(report.ok)
        self.assertTrue(any("secret-like tracked values" in item for item in report.errors))
        self.assertTrue(any("health check failed" in item for item in report.errors))


if __name__ == "__main__":
    unittest.main()
