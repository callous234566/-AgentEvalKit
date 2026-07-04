"""Tests for config.py helper functions."""

import os
import unittest
from unittest.mock import patch

import config


class EnvBoolTest(unittest.TestCase):
    """_env_bool 边界值测试。"""

    def _call(self, value, default=False):
        with patch.dict(os.environ, {"TEST_KEY": value} if value is not None else {}, clear=False):
            if value is None:
                os.environ.pop("TEST_KEY", None)
            return config._env_bool("TEST_KEY", default)

    def test_true_values(self):
        for v in ("1", "true", "True", "TRUE", "yes", "Yes", "on", "On", "y", "Y"):
            self.assertTrue(self._call(v), f"Expected True for {v!r}")

    def test_false_values(self):
        for v in ("0", "false", "False", "FALSE", "no", "No", "off", "Off", "n", "N", "anything"):
            self.assertFalse(self._call(v), f"Expected False for {v!r}")

    def test_missing_uses_default(self):
        self.assertFalse(self._call(None, default=False))
        self.assertTrue(self._call(None, default=True))

    def test_whitespace_is_stripped(self):
        self.assertTrue(self._call("  true  "))
        self.assertFalse(self._call("  false  "))


class EnvListTest(unittest.TestCase):
    """_env_list 边界值测试。"""

    def _call(self, value, default=None):
        if default is None:
            default = []
        with patch.dict(os.environ, {"TEST_LIST": value} if value is not None else {}, clear=False):
            if value is None:
                os.environ.pop("TEST_LIST", None)
            return config._env_list("TEST_LIST", default)

    def test_basic_csv(self):
        self.assertEqual(self._call("a,b,c"), ["a", "b", "c"])

    def test_whitespace_trimming(self):
        self.assertEqual(self._call("  a , b , c  "), ["a", "b", "c"])

    def test_empty_string_returns_default(self):
        self.assertEqual(self._call("", default=["fallback"]), ["fallback"])

    def test_missing_returns_default(self):
        self.assertEqual(self._call(None, default=["x"]), ["x"])

    def test_trailing_commas(self):
        self.assertEqual(self._call("a,b,"), ["a", "b"])

    def test_single_item(self):
        self.assertEqual(self._call("only"), ["only"])

    def test_whitespace_only_returns_default(self):
        self.assertEqual(self._call("  ,,  ", default=["d"]), ["d"])


class CheckApiKeyTest(unittest.TestCase):
    """check_api_key 测试。"""

    def test_real_key_is_valid(self):
        with patch.object(config, "LLM_API_KEY", "sk-real-key-123"):
            self.assertTrue(config.check_api_key())

    def test_placeholder_deepseek_is_invalid(self):
        with patch.object(config, "LLM_API_KEY", "your_deepseek_api_key_here"):
            self.assertFalse(config.check_api_key())

    def test_placeholder_generic_is_invalid(self):
        with patch.object(config, "LLM_API_KEY", "sk-your-api-key-here"):
            self.assertFalse(config.check_api_key())

    def test_empty_is_invalid(self):
        with patch.object(config, "LLM_API_KEY", ""):
            self.assertFalse(config.check_api_key())


class ConfigDefaultsTest(unittest.TestCase):
    """验证关键配置常量有合理的默认值。"""

    def test_chunk_size_positive(self):
        self.assertGreater(config.CHUNK_SIZE, 0)

    def test_chunk_overlap_less_than_chunk_size(self):
        self.assertLess(config.CHUNK_OVERLAP, config.CHUNK_SIZE)

    def test_retriever_top_k_positive(self):
        self.assertGreater(config.RETRIEVER_TOP_K, 0)

    def test_supported_extensions_non_empty(self):
        self.assertGreater(len(config.SUPPORTED_EXTENSIONS), 0)
        for ext in config.SUPPORTED_EXTENSIONS:
            self.assertTrue(ext.startswith("."))

    def test_max_upload_size_reasonable(self):
        self.assertGreater(config.MAX_UPLOAD_SIZE, 1024 * 1024)  # > 1MB
        self.assertLessEqual(config.MAX_UPLOAD_SIZE, 100 * 1024 * 1024)  # <= 100MB

    def test_agent_debug_enabled_by_default(self):
        self.assertIsInstance(config.AGENT_DEBUG, bool)
        self.assertTrue(config.AGENT_DEBUG)

    def test_tool_retry_defaults_are_reasonable(self):
        self.assertGreaterEqual(config.TOOL_RETRY_MAX_ATTEMPTS, 1)
        self.assertGreaterEqual(config.TOOL_RETRY_BACKOFF_SECONDS, 0)
        self.assertGreaterEqual(config.WEB_SEARCH_MAX_RESULTS, 1)
        self.assertGreater(config.WEB_SEARCH_TIMEOUT, 0)

    def test_llm_max_tokens_default_supports_code_answers(self):
        self.assertGreaterEqual(config.LLM_MAX_TOKENS, 2000)

    def test_large_file_term_expansion_includes_streaming_keywords(self):
        rule = next(
            item for item in config.TERM_EXPANSION_RULES
            if "大文件" in item["triggers"]
        )
        self.assertIn("stream_read_text", rule["expand"])
        self.assertIn("chunk_size", rule["expand"])


if __name__ == "__main__":
    unittest.main()
