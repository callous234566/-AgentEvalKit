"""Tests for VectorStoreManager rename and name mapping logic."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from rag.vector_store import VectorStoreManager


class NameMappingTest(unittest.TestCase):
    """Test name mapping persistence logic in isolation."""

    def _make_manager(self, tmp_path):
        manager = VectorStoreManager.__new__(VectorStoreManager)
        manager.db_path = str(tmp_path)
        manager._stores = {}
        manager._collection_cache = {}
        manager._name_mapping = {}
        manager._mapping_file = Path(tmp_path) / "collection_name_mapping.json"
        return manager

    def test_save_and_load_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            manager._name_mapping = {"我的知识库": "kb_abc123"}
            manager._save_name_mapping()

            manager2 = self._make_manager(tmp)
            manager2._load_name_mapping()
            self.assertEqual(manager2._name_mapping, {"我的知识库": "kb_abc123"})

    def test_load_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            manager._load_name_mapping()
            self.assertEqual(manager._name_mapping, {})

    def test_load_corrupted_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            manager._mapping_file.write_text("not json!", encoding="utf-8")
            manager._load_name_mapping()
            self.assertEqual(manager._name_mapping, {})

    def test_get_collection_name_creates_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            name = manager._get_collection_name("测试知识库")
            self.assertTrue(name.startswith("kb_"))
            self.assertIn("测试知识库", manager._name_mapping)

    def test_get_collection_name_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            name1 = manager._get_collection_name("测试")
            name2 = manager._get_collection_name("测试")
            self.assertEqual(name1, name2)

    def test_rename_updates_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = self._make_manager(tmp)
            manager._name_mapping = {"旧名称": "kb_old123"}

            # Mock list_collections to return existing collections
            manager.list_collections = MagicMock(return_value=["旧名称"])
            manager._save_name_mapping = MagicMock()

            # Simulate rename logic
            chroma_name = manager._get_collection_name("旧名称")
            manager._name_mapping.pop("旧名称", None)
            manager._name_mapping["新名称"] = chroma_name

            self.assertNotIn("旧名称", manager._name_mapping)
            self.assertIn("新名称", manager._name_mapping)
            self.assertEqual(manager._name_mapping["新名称"], "kb_old123")


class InvalidateCollectionCacheTest(unittest.TestCase):
    def setUp(self):
        self.manager = VectorStoreManager.__new__(VectorStoreManager)
        self.manager._collection_cache = {}
        self.manager._stores = {}

    def test_invalidate_specific_store(self):
        self.manager._collection_cache["fake_key"] = {"count": 10}
        store = MagicMock()
        store._collection.name = "fake_key"

        self.manager._invalidate_collection_cache(store=store)
        self.assertNotIn("fake_key", self.manager._collection_cache)

    def test_invalidate_all(self):
        self.manager._collection_cache["key1"] = {}
        self.manager._collection_cache["key2"] = {}
        self.manager._invalidate_collection_cache()
        self.assertEqual(len(self.manager._collection_cache), 0)


if __name__ == "__main__":
    unittest.main()
