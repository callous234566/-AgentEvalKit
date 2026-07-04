"""Tests for rag.logging_utils.setup_logging."""

import logging
import tempfile
import unittest
from pathlib import Path
from logging.handlers import RotatingFileHandler
from unittest.mock import patch

from rag.logging_utils import (
    RequestIdFilter,
    get_request_id,
    reset_request_id,
    set_request_id,
    setup_logging,
)


def _close_file_handlers():
    """Close all RotatingFileHandler instances so temp files can be deleted on Windows."""
    root = logging.getLogger()
    for handler in root.handlers[:]:
        if isinstance(handler, RotatingFileHandler):
            handler.close()
            root.removeHandler(handler)


class SetupLoggingTest(unittest.TestCase):
    def setUp(self):
        root = logging.getLogger()
        self._original_handlers = root.handlers[:]
        self._original_level = root.level
        # Clear handlers for a clean test
        root.handlers.clear()

    def tearDown(self):
        _close_file_handlers()
        root = logging.getLogger()
        root.handlers = self._original_handlers
        root.setLevel(self._original_level)

    def test_creates_log_dir_and_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("rag.logging_utils.config") as mock_config:
                mock_config.LOG_DIR = tmp
                mock_config.LOG_FILE = "test.log"
                mock_config.LOG_MAX_BYTES = 1024
                mock_config.LOG_BACKUP_COUNT = 1
                setup_logging()
                log_path = Path(tmp) / "test.log"
                self.assertTrue(log_path.parent.exists())
            _close_file_handlers()

    def test_no_duplicate_handlers_on_repeated_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("rag.logging_utils.config") as mock_config:
                mock_config.LOG_DIR = tmp
                mock_config.LOG_FILE = "test.log"
                mock_config.LOG_MAX_BYTES = 1024
                mock_config.LOG_BACKUP_COUNT = 1

                setup_logging()
                handler_count_after_first = len(logging.getLogger().handlers)

                setup_logging()
                handler_count_after_second = len(logging.getLogger().handlers)

                self.assertEqual(handler_count_after_first, handler_count_after_second)
            _close_file_handlers()

    def test_root_logger_level_is_info(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("rag.logging_utils.config") as mock_config:
                mock_config.LOG_DIR = tmp
                mock_config.LOG_FILE = "test.log"
                mock_config.LOG_MAX_BYTES = 1024
                mock_config.LOG_BACKUP_COUNT = 1

                setup_logging()
                self.assertEqual(logging.getLogger().level, logging.INFO)
            _close_file_handlers()

    def test_formatter_includes_request_id_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("rag.logging_utils.config") as mock_config:
                mock_config.LOG_DIR = tmp
                mock_config.LOG_FILE = "test.log"
                mock_config.LOG_MAX_BYTES = 1024
                mock_config.LOG_BACKUP_COUNT = 1

                setup_logging()

                formats = [
                    handler.formatter._fmt
                    for handler in logging.getLogger().handlers
                    if handler.formatter is not None
                ]
                self.assertTrue(any("request_id=%(request_id)s" in fmt for fmt in formats))
            _close_file_handlers()

    def test_request_id_filter_adds_safe_default(self):
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )

        RequestIdFilter().filter(record)

        self.assertEqual(record.request_id, "-")

    def test_request_id_context_can_be_set_and_reset(self):
        token = set_request_id("req-ctx")
        try:
            self.assertEqual(get_request_id(), "req-ctx")
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname=__file__,
                lineno=1,
                msg="hello",
                args=(),
                exc_info=None,
            )
            RequestIdFilter().filter(record)
            self.assertEqual(record.request_id, "req-ctx")
        finally:
            reset_request_id(token)

        self.assertEqual(get_request_id(), "-")


if __name__ == "__main__":
    unittest.main()
