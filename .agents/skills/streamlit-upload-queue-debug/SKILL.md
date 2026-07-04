---
name: streamlit-upload-queue-debug
description: Use in this personal-rag-assistant repo when debugging Streamlit upload queue behavior in ui/upload.py, streamlit_app.py, ui/api_wrappers.py, or related upload styles. Trigger for file removal not working, failed files reappearing, duplicate queued files, waiting/processing/success state drift, retry/reselect confusion, hidden pagination leaking, upload status not refreshing, or upload queue UI showing raw HTML/progress/default alerts. Do not use for backend-only parser failures in rag/document_loader.py, unrelated CSS cleanup, document-management bulk operations, or visual-only upload styling unless queue state behavior is involved.
---

# Streamlit Upload Queue Debug

Debug upload queues from session state first, then UI.

## Workflow

1. Locate upload state and rendering:

```powershell
rg -n "upload_task_queue|upload_removed_keys|merge_upload_queue|remove_upload_queue_item|run_upload_queue|uploaded_files" ui\upload.py streamlit_app.py ui\api_wrappers.py
```

2. Confirm deletion writes to Streamlit session state:

- Removed file keys must be stored in `upload_removed_keys`.
- Queue must be filtered through removed keys before rendering and processing.
- Do not depend on hidden native uploader DOM buttons as the source of truth.
- Failed and waiting rows must be removable from the visible queue without requiring a browser refresh.

3. Confirm queue merging preserves state:

- Newly selected files may be added.
- Removed files must not reappear in the same selection lifecycle.
- Successful files must not be processed again by the main button.
- Processing files should not render a delete button.
- Selecting the same file again after removal should create one clean waiting row, not duplicates.

4. Confirm failure recovery stays inline:

- Failure reason should appear in the file row.
- Avoid large default `st.error` blocks and separate retry panels unless explicitly requested.
- For scanned/image PDFs, surface OCR or multimodal permission guidance.
- Keep a single long upload queue card; avoid separate "selected files" and "task queue" duplicate lists.

5. Validate narrowly:

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-upload-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile ui\upload.py ui\api_wrappers.py streamlit_app.py
```

```powershell
rg -n "st\.(info|warning|success|error|progress|spinner)|upload_failure_actions|upload_reselect_failed|上传文件上一页|上传文件下一页" ui\upload.py ui\styles streamlit_app.py
```

## Guardrails

- Do not clear successful task state unless the user explicitly resets selection.
- Do not change backend parsing when the bug is queue rendering or session state.
- Do not rely on fragile DOM scraping for deletion behavior.
- Do not reset or clean real uploaded files or Chroma data during UI queue debugging.
