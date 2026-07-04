---
name: rag-debug-loop
description: Use in this personal-rag-assistant repo when debugging RAG answer quality, retrieval misses, wrong citations, empty context, query rewrite issues, reranker/compression behavior, Chroma mapping problems, or SiliconFlow embedding/generation compatibility. Trigger for RAG-specific defects across rag/qa_chain.py, rag/vector_store.py, rag/document_loader.py, rag/text_splitter.py, rag/reranker.py, rag/multimodal.py, and main.py endpoints. Do not use for frontend-only layout work, CSS cleanup, pure documentation edits, or backend infrastructure changes unrelated to retrieval/generation.
---

# RAG Debug Loop

Debug the RAG path from input document to final answer with minimal, reversible changes.

## Workflow

1. Read `AGENTS.md`, `PROJECT_MAP.md`, and `docs/KNOWN_ISSUES.md` before changing code.
2. Identify the failing stage:

- Upload/parse: `rag/document_loader.py`, `rag/upload_validation.py`, `/upload`.
- Chunking: `rag/text_splitter.py`, configured chunk size/overlap.
- Storage/mapping: `rag/vector_store.py`, `chroma_db`, `collection_name_mapping.json`.
- Retrieval/rerank/compress: `rag/vector_store.py`, `rag/reranker.py`.
- Generation/agent: `rag/qa_chain.py`, `rag/agent.py`, `rag/tools.py`.

3. Reproduce narrowly with existing tests or a small local fixture. Never use the real `chroma_db/collection_name_mapping.json` for temporary mapping tests.
4. Check known compatibility rules:

- SiliconFlow embeddings through `OpenAIEmbeddings` must use `check_embedding_ctx_length=False`.
- Chinese text should remain raw strings; project chunking handles length protection.
- Runtime caches need explicit max size and invalidation after upload/delete/rename/toggle.

5. Prefer focused validation:

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_qa_chain.py tests\test_document_loader.py -q
```

6. Compile touched RAG/API files:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-debug-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py rag\qa_chain.py rag\vector_store.py rag\document_loader.py rag\text_splitter.py
```

## Guardrails

- Do not hide retrieval errors by returning generic empty answers.
- Do not disable reranker, compression, multimodal, or agent paths globally unless explicitly requested.
- Do not mutate production Chroma data for diagnosis unless the user explicitly asks.
- Update `BUG_LOG.md` after code or durable doc changes.
