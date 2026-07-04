---
name: streamlit-css-maintenance
description: Use in this personal-rag-assistant repo when maintaining the large Streamlit CSS override system in ui/styles/*. Trigger for inspecting duplicate selectors, orphan rules, loading order, dark/mobile final refinement layers, CSS size, legacy sidebar/upload selectors, or safe cleanup opportunities after the UI is stable. Do not use for normal feature implementation, backend/RAG work, urgent broken-interaction fixes, broad visual redesigns, or changes requiring Streamlit button keys/session-state/DOM hook changes.
---

# Streamlit CSS Maintenance

Maintain CSS safely with scans and tiny changes, not broad rewrites.

## Workflow

1. Inspect CSS module sizes and loading order:

```powershell
Get-ChildItem ui\styles -Filter *.py | Select-Object Name,Length
Get-Content ui\styles\__init__.py
```

2. Preserve current load intent from `ui/styles/__init__.py`: variables/global first, component modules next, button/widgets layers before final dark/mobile refinements.
3. Search for known legacy selectors before deleting anything:

```powershell
rg -n "upload-docs-table|uploaded-files|collection-menu|session-menu|collection_menu_|collection_more_|stPopoverBody|sidebar-new-btn|upload-task-list|mode-select-btn" ui streamlit_app.py
```

4. Treat a rule as removable only when:

- It appears only in style files.
- No current HTML/component code emits the class or key.
- No later module relies on it as an override hook.
- It is not part of sidebar menus, upload queue, fixed composer, document management, dark mode, or mobile final coverage.

5. Preserve final override order:

- Variables first.
- Component/base styles before final refinements.
- Dark final refinements near the end.
- Mobile final refinements after dark refinements.

6. Validate:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-css-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile ui\styles\__init__.py streamlit_app.py
```

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q
git diff --check -- ui\styles tests\test_frontend_ui_contracts.py BUG_LOG.md
```

## Guardrails

- Do not change button keys, session state keys, or DOM hook class names during cleanup.
- Do not large-scale reformat CSS in a dirty worktree.
- Prefer documenting a risky rule over deleting it.
- Do not chase CSS file size while the user is still actively tuning visual details.
