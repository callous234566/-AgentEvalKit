"""Tests for rag.session_state load/persist logic (JSON file operations only)."""

import json
import tempfile
import unittest
from pathlib import Path

from rag.session_state import load_persisted_sessions


class LoadPersistedSessionsTest(unittest.TestCase):
    def test_missing_file_returns_defaults(self):
        result = load_persisted_sessions(Path("/nonexistent/path.json"))
        self.assertEqual(result["sessions"], {})
        self.assertIsNone(result["current_session_id"])
        self.assertEqual(result["input_history"], [])

    def test_valid_file(self):
        data = {
            "sessions": {"abc": {"name": "test", "messages": []}},
            "current_session_id": "abc",
            "input_history": ["q1", "q2"],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            path = Path(f.name)
        try:
            result = load_persisted_sessions(path)
            self.assertEqual(result["sessions"]["abc"]["name"], "test")
            self.assertEqual(result["current_session_id"], "abc")
            self.assertEqual(result["input_history"], ["q1", "q2"])
        finally:
            path.unlink()

    def test_corrupted_json_returns_defaults(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("not valid json{{{")
            path = Path(f.name)
        try:
            result = load_persisted_sessions(path)
            self.assertEqual(result["sessions"], {})
        finally:
            path.unlink()

    def test_non_dict_sessions_field_returns_empty(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=json.__name__, delete=False, encoding="utf-8"
        ) as f:
            json.dump({"sessions": "not a dict", "current_session_id": "x"}, f)
            path = Path(f.name)
        try:
            result = load_persisted_sessions(path)
            self.assertEqual(result["sessions"], {})
        finally:
            path.unlink()

    def test_empty_file_returns_defaults(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            path = Path(f.name)
        try:
            result = load_persisted_sessions(path)
            self.assertEqual(result["sessions"], {})
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
