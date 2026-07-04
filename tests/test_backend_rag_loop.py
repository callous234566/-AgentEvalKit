"""End-to-end backend RAG loop tests with temporary Chroma storage."""

from __future__ import annotations

import hashlib
import gc

from fastapi.testclient import TestClient


class FakeEmbeddings:
    """Small deterministic embedding function for Chroma integration tests."""

    def _embed(self, text: str) -> list[float]:
        normalized = (text or "").lower()
        buckets = [0.0] * 8
        for token in normalized.split():
            digest = hashlib.md5(token.encode("utf-8")).digest()
            buckets[digest[0] % len(buckets)] += 1.0
        if "retrieval" in normalized or "检索" in normalized:
            buckets[0] += 3.0
        if "embedding" in normalized or "向量" in normalized:
            buckets[1] += 2.0
        if "citation" in normalized or "引用" in normalized:
            buckets[2] += 2.0
        total = sum(value * value for value in buckets) ** 0.5 or 1.0
        return [value / total for value in buckets]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class FakeLLM:
    def invoke(self, prompt: str):
        raise AssertionError(f"retrieve-only loop should not call LLM: {prompt[:80]}")


def test_upload_then_retrieve_uses_temp_chroma_and_exports_source_scores(temp_dir, monkeypatch):
    import main
    import rag.vector_store as vector_store_module
    from rag.vector_store import VectorStoreManager

    fake_embeddings = FakeEmbeddings()
    temp_chroma_dir = temp_dir / "chroma"
    temp_vector_store = VectorStoreManager(db_path=str(temp_chroma_dir))

    monkeypatch.setattr(main.config, "check_api_key", lambda: True)
    monkeypatch.setattr(main.config, "ENABLE_MULTIMODAL_PARSING", False)
    monkeypatch.setattr(main, "vector_store", temp_vector_store)
    monkeypatch.setattr(main, "_get_llm", lambda temperature: FakeLLM())
    monkeypatch.setattr(vector_store_module, "get_embedding_model", lambda: fake_embeddings)
    main._qa_chain_cache.clear()

    try:
        client = TestClient(main.app)
        collection_name = "闭环测试知识库"
        document_content = "\n".join([
            "# RAG 闭环测试",
            "",
            "Retrieval metadata should preserve source citation and chunk score fields.",
            "Embedding retrieval connects upload, chunking, vector storage, and source citation.",
            "本段用于验证检索、向量、引用和 chunk score 元数据可以完整返回。",
        ])

        upload_response = client.post(
            "/upload",
            data={
                "collection_name": collection_name,
                "chunk_size": "300",
                "chunk_overlap": "20",
                "enable_multimodal": "false",
            },
            files={
                "file": (
                    "rag_loop.md",
                    document_content.encode("utf-8"),
                    "text/markdown",
                ),
            },
        )

        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        assert upload_data["success"] is True
        assert upload_data["chunks_added"] >= 1
        assert not (temp_dir / "chroma_db" / "collection_name_mapping.json").exists()
        assert (temp_chroma_dir / "collection_name_mapping.json").exists()

        retrieve_response = client.post(
            "/retrieve",
            json={
                "question": "How does retrieval preserve source citation and chunk score metadata?",
                "collection_name": collection_name,
                "enable_query_rewrite": False,
                "enable_contextual_compression": False,
                "top_k": 3,
            },
        )

        assert retrieve_response.status_code == 200
        retrieve_data = retrieve_response.json()
        assert retrieve_data["success"] is True
        assert retrieve_data["documents"]
        assert retrieve_data["sources"]

        top_source = retrieve_data["sources"][0]
        assert top_source["source"] == "rag_loop.md"
        assert top_source["score"] > 0
        assert top_source["vector_score"] > 0
        assert "keyword_score" in top_source
        assert "candidate_source" in top_source

        final_document = retrieve_data["trace"]["final_documents"][0]
        assert final_document["source"] == "rag_loop.md"
        assert final_document["score"] == top_source["score"]
        assert "candidate_source" in final_document
    finally:
        main._qa_chain_cache.clear()
        temp_vector_store._stores.clear()
        temp_vector_store._collection_cache.clear()
        try:
            from chromadb.api.client import SharedSystemClient

            SharedSystemClient.clear_system_cache()
        except Exception:
            pass
        gc.collect()
