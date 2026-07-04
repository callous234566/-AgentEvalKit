---
name: rag-backend-smoke
description: Use in this personal-rag-assistant repo when running minimal safe backend smoke checks for FastAPI, RAG retrieval, Chroma collection listing, SiliconFlow embedding compatibility, upload API behavior, or focused backend tests. Trigger for "后端开了吗", health checks, quick RAG sanity checks, collection/read-only API verification, or confirming a backend change did not break core flow. Do not use for destructive delete/reset operations, real data mutation, frontend-only style work, broad performance benchmarking, or full end-to-end ingestion unless explicitly requested.
---

# RAG Backend Smoke

Run minimal safe backend checks without mutating real data unless explicitly requested.

## Workflow

1. Check backend health:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health
```

2. Check frontend availability only if relevant:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8501
```

3. Read-only collection smoke, if backend is available:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/collections
```

4. Prefer focused tests:

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_api_client.py -q
```

5. For embedding/retrieval regressions, confirm:

- `OpenAIEmbeddings` uses `check_embedding_ctx_length=False` for SiliconFlow compatibility.
- Chinese text is sent as raw strings, not token-id arrays.
- Mapping tests use temp directories, not real `chroma_db/collection_name_mapping.json`.

6. For upload backend changes, validate affected formats when practical: PDF, TXT, DOCX, Markdown. Prefer tests around `rag/document_loader.py`, `rag/text_splitter.py`, `rag/upload_validation.py`, and FastAPI `/upload` behavior.

## Guardrails

- Do not run destructive delete/reset operations unless the user explicitly asks.
- Do not mutate real Chroma mapping files for temporary tests.
- Do not silently swallow API errors; inspect returned messages or logs.
- Prefer stable backend startup scripts for long-running service work.
- If a check requires real API keys or external model calls, say so and fall back to local focused tests.
