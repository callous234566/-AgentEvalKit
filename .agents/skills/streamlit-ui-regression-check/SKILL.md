---
name: streamlit-ui-regression-check
description: Use in this personal-rag-assistant repo when checking Streamlit UI regressions after edits to streamlit_app.py, ui/sidebar.py, ui/upload.py, ui/chat.py, ui/pages.py, ui/components.py, ui/js_injection.py, or ui/styles/*. Trigger for requests such as UI regression check, interaction patrol, dark/light validation, sidebar three-dot menu verification, fixed chat input verification, upload UI validation, or confirming default Streamlit alerts/progress did not reappear. Do not use for backend-only FastAPI/RAG changes, dependency upgrades, pure documentation work, or broad redesign implementation unless the user specifically asks to validate regressions.
---

# Streamlit UI Regression Check

Run a safe frontend regression pass without changing business logic.

## Workflow

1. Read project rules in `AGENTS.md`.
2. Check the current map before guessing: `PROJECT_MAP.md`, then `docs/KNOWN_ISSUES.md` if the issue looks familiar.
3. Scan for forbidden default Streamlit page feedback:

```powershell
rg -n "st\.(info|warning|success|error|progress|spinner|balloons)" ui streamlit_app.py
```

4. Confirm unified feedback and theme coverage:

```powershell
rg -n "render_status_notice|status-notice|body\.rag-dark .*status-notice" ui
```

5. Inspect regression-sensitive areas when touched:

- Sidebar menus in `ui/sidebar.py`: one three-dot trigger per row, no duplicate triggers, menu item set stays stable.
- Upload queue in `ui/upload.py`: delete/remove stays session-state driven, no default Streamlit progress or retry panel leaks.
- Chat in `ui/chat.py` and `ui/js_injection.py`: fixed composer, latest-answer scrolling, and user history reading behavior stay intact.
- Styles in `ui/styles/__init__.py`: final dark refinement still loads after component/button layers and before mobile final coverage.

6. Run focused frontend contract tests when present:

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q
```

7. Compile touched UI files with a temp cache prefix:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-ui-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\components.py ui\sidebar.py ui\upload.py ui\chat.py ui\js_injection.py ui\styles\__init__.py
```

8. Run `git diff --check` on touched files.

## Guardrails

- Do not restart services unless explicitly needed.
- Do not restore `st.popover`, default Streamlit alert/progress components, hidden uploader DOM dependence, or old sidebar menu selectors without a deliberate decision.
- Treat sidebar three-dot menus, upload deletion, fixed chat input, and latest-answer scrolling as regression-sensitive.
- If the user says they will refresh the UI, do not spend time restarting just for CSS/HTML edits.
