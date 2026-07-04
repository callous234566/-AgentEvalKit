---
name: frontend-change
description: Use in this personal-rag-assistant repo before implementing frontend changes in streamlit_app.py, ui/sidebar.py, ui/upload.py, ui/chat.py, ui/pages.py, ui/components.py, ui/js_injection.py, ui/icons.py, or ui/styles/*. Trigger when the user asks to change Streamlit UI layout, sidebar menus, upload queue, document management, fixed chat input, theme styling, icons, status notices, or interaction behavior. Do not use for backend-only RAG/API changes, dependency work, docs-only edits, or pure verification tasks better covered by streamlit-ui-regression-check.
---

# Frontend Change

Implement Streamlit frontend changes without regressing stable interactions.

## Workflow

1. Read `AGENTS.md`, `PROJECT_MAP.md`, and `docs/KNOWN_ISSUES.md`.
2. Identify the affected UI module:

- Sidebar and three-dot menus: `ui/sidebar.py`, `ui/styles/_sidebar.py`.
- Upload queue: `ui/upload.py`, `ui/styles/_upload.py`.
- Chat and fixed composer: `ui/chat.py`, `ui/js_injection.py`, `ui/styles/_chat.py`.
- Tabs/pages/document management: `ui/pages.py`, `ui/components.py`, `ui/styles/_documents.py`.
- Icons and shared controls: `ui/icons.py`, `ui/styles/_widgets.py`, `ui/styles/_buttons.py`.

3. Before edits, protect these stable contracts:

- Sidebar row text and three-dot button share one aligned capsule.
- Upload queue deletion is based on session state, not hidden DOM.
- Page feedback uses `render_status_notice()` or toast, not large default Streamlit alerts.
- Fixed input stays at the bottom and avoids forced jumps when user is reading history.
- Dark/light mode and mobile final coverage stay synchronized.

4. Use `apply_patch` for file edits. Keep changes small and avoid broad CSS rewrites.
5. Validate with focused commands:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-frontend-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\sidebar.py ui\upload.py ui\chat.py ui\components.py ui\pages.py ui\js_injection.py ui\styles\__init__.py
```

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q
```

## Guardrails

- Do not restart services for small CSS/HTML edits unless runtime code, dependencies, or backend interfaces changed.
- Do not change Streamlit button keys/session-state keys casually; they are part of interaction behavior.
- Do not reintroduce default Streamlit `st.info/error/progress/spinner` UI.
- Update `BUG_LOG.md` after modifications.
