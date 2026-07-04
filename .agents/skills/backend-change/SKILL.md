---
name: backend-change
description: Use in this personal-rag-assistant repo before implementing backend changes in main.py, config.py, rag/*.py, API wrappers, startup scripts, or tests that affect FastAPI endpoints, RAG flow, Chroma persistence, caches, model configuration, upload parsing, or external API behavior. Trigger when the user asks to modify backend logic, fix backend bugs, add API behavior, adjust persistence, or change model/RAG settings. Do not use for frontend-only Streamlit styling, project skill/docs-only changes, or read-only backend explanation unless no code will be changed.
---

# Backend Change

Make backend changes safely and keep data/state semantics intact.

## Workflow

1. Read `AGENTS.md`, `PROJECT_MAP.md`, and the relevant section of `docs/KNOWN_ISSUES.md`.
2. Map the change to real files:

- API routes and request/response behavior: `main.py`.
- Environment and settings: `config.py`, `.env.example` when variables change.
- RAG orchestration: `rag/qa_chain.py`, `rag/agent.py`, `rag/tools.py`.
- Vector store, collections, cache invalidation: `rag/vector_store.py`.
- Upload parsing/validation: `rag/document_loader.py`, `rag/upload_validation.py`, `rag/text_splitter.py`, `rag/multimodal.py`.
- API helper behavior used by UI: `ui/api_wrappers.py`.

3. Make the smallest code change that fixes the behavior; do not refactor unrelated modules.
4. Preserve persistence contracts:

- Chinese collection names must keep disk mapping.
- Upload/delete/rename/toggle must invalidate affected caches.
- API errors must be logged and returned as user-friendly messages.

5. Run focused validation based on touched files:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-backend-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py config.py rag\qa_chain.py rag\vector_store.py rag\document_loader.py
```

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_main_endpoints.py tests\test_vector_store.py tests\test_api_client.py -q
```

6. If a dependency or environment variable changes, update `requirements.txt` or `.env.example` and document the impact.

## Guardrails

- Do not use `--reload` for long-running/production backend guidance; prefer `start_backend_stable.ps1`.
- Do not swallow exceptions or skip validation to make a failing path appear successful.
- Do not reset/revert/clean untracked files in this dirty worktree.
- Update `BUG_LOG.md` after modifications.
