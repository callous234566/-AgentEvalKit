"""Upload flow: file preview, queue, execution, upload section."""

import hashlib
import html

import streamlit as st

from ui.api_wrappers import upload_file, format_last_response_diagnostic_suffix
from ui.assets import icon_label, icon_svg
from ui.components import render_empty_state, render_section_intro
from ui.text_utils import format_file_size


def get_upload_file_key(file) -> str:
    """Build a stable content fingerprint for uploaded files."""
    size = getattr(file, "size", len(file.getvalue()))
    digest = hashlib.md5(file.getvalue()[:2048]).hexdigest()[:10]
    return f"{file.name}:{size}:{digest}"


def get_upload_file_entries(uploaded_files: list) -> list:
    """Build queue entries with occurrence indexes so duplicate files stay distinct."""
    seen_counts = {}
    entries = []
    for file in uploaded_files:
        base_key = get_upload_file_key(file)
        occurrence = seen_counts.get(base_key, 0) + 1
        seen_counts[base_key] = occurrence
        queue_key = f"{base_key}:#{occurrence}"
        entries.append(
            {
                "file": file,
                "key": queue_key,
                "base_key": base_key,
                "name": file.name,
                "size": getattr(file, "size", len(file.getvalue())),
            }
        )
    return entries


def build_upload_queue(uploaded_files: list) -> list:
    """Create waiting queue rows for the selected files."""
    removed_keys = set(st.session_state.get("upload_removed_keys", []))
    return [
        {
            "key": entry["key"],
            "base_key": entry["base_key"],
            "name": entry["name"],
            "size": entry["size"],
            "status": "waiting",
            "message": "等待上传",
        }
        for entry in get_upload_file_entries(uploaded_files)
        if entry["key"] not in removed_keys
    ]


def merge_upload_queue(uploaded_files: list) -> list:
    """Preserve finished task states while adding newly selected files."""
    existing_by_key = {
        item.get("key"): dict(item)
        for item in st.session_state.get("upload_task_queue", [])
        if item.get("key")
    }
    merged_queue = []
    for new_item in build_upload_queue(uploaded_files):
        existing_item = existing_by_key.get(new_item["key"])
        merged_queue.append(existing_item or new_item)
    return merged_queue


def remove_upload_queue_item(item_key: str) -> None:
    """Remove one upload queue item through Streamlit state, not DOM scripts."""
    if not item_key:
        return

    queue = st.session_state.get("upload_task_queue", [])
    target = next((item for item in queue if item.get("key") == item_key), None)
    if target and target.get("status") == "processing":
        return

    removed_keys = set(st.session_state.get("upload_removed_keys", []))
    removed_keys.add(item_key)
    st.session_state.upload_removed_keys = sorted(removed_keys)
    remaining_queue = [
        item
        for item in queue
        if item.get("key") != item_key
    ]
    st.session_state.upload_task_queue = remaining_queue
    st.session_state.pop("upload_last_result", None)
    if not remaining_queue:
        st.session_state.upload_uploader_reset_nonce = (
            int(st.session_state.get("upload_uploader_reset_nonce", 0)) + 1
        )
        st.session_state.upload_removed_keys = []
        st.session_state.upload_preview_total = 0
        st.session_state.upload_preview_page = 1
        st.session_state.upload_preview_signature = []
    st.rerun()


def filter_removed_upload_queue(queue: list) -> list:
    """Keep queue state consistent after files are removed."""
    removed_keys = set(st.session_state.get("upload_removed_keys", []))
    return [item for item in queue if item.get("key") not in removed_keys]


def reset_upload_selection() -> None:
    """Clear the current uploader widget and queue so users can choose files again."""
    st.session_state.upload_uploader_reset_nonce = (
        int(st.session_state.get("upload_uploader_reset_nonce", 0)) + 1
    )
    st.session_state.upload_removed_keys = []
    st.session_state.upload_task_queue = []
    st.session_state.upload_preview_total = 0
    st.session_state.upload_preview_page = 1
    st.session_state.upload_preview_signature = []
    st.session_state.pop("upload_last_result", None)


def get_upload_failure_guidance(file_name: str, message: str) -> str:
    """Return a short recovery hint for a failed upload queue item."""
    normalized_name = file_name.lower()
    normalized_message = message.lower()
    if normalized_name.endswith(".pdf") and any(
        keyword in normalized_message
        for keyword in ("为空", "扫描", "ocr", "多模态", "图片型", "未添加任何内容")
    ):
        return "可能是扫描版 PDF。请启用图片解析并确认模型权限，或改用 OCR / 可复制文本版本。"
    return "请移除此文件后重新选择；如仍失败，请检查文件内容和当前解析设置。"


def get_upload_signature(uploaded_files: list) -> list:
    """Represent the current uploader selection including duplicate occurrences."""
    return [entry["key"] for entry in get_upload_file_entries(uploaded_files)]


def render_upload_steps(queue: list) -> None:
    """Render a compact upload progress guide from the current queue state."""
    statuses = [item.get("status", "waiting") for item in queue]
    has_processing = "processing" in statuses
    has_finished = bool(statuses) and all(status in {"success", "failed"} for status in statuses)
    active_step = 3 if has_finished else 2 if has_processing else 1 if statuses else 0
    steps = [
        ("1", "解析中", "读取格式与文本"),
        ("2", "已入库", "切分并写入向量库"),
        ("3", "可提问", "回到问答查看引用"),
    ]
    step_html = []
    for index, (number, title, caption) in enumerate(steps):
        state = "done" if index < active_step else "active" if index == active_step else "pending"
        step_html.append(
            f"""
            <div class="upload-step {state}">
                <span class="upload-step-index">{number}</span>
                <span>
                    <strong>{title}</strong>
                    <small>{caption}</small>
                </span>
            </div>
            """
        )
    st.html(f'<div class="upload-flow-steps">{"".join(step_html)}</div>')


def handle_upload_queue_pagination(queue: list, page_size: int = 10) -> None:
    """Render hidden pagination triggers used by the custom queue footer."""
    if not queue:
        return

    total_files = len(queue)
    total_pages = max(1, (total_files + page_size - 1) // page_size)
    current_page = int(st.session_state.get("upload_preview_page", 1))
    current_page = max(1, min(current_page, total_pages))
    st.session_state.upload_preview_page = current_page

    prev_trigger = st.button("上传文件上一页", key="upload_preview_prev")
    next_trigger = st.button("上传文件下一页", key="upload_preview_next")
    if prev_trigger and current_page > 1:
        st.session_state.upload_preview_page = current_page - 1
        st.rerun()
    if next_trigger and current_page < total_pages:
        st.session_state.upload_preview_page = current_page + 1
        st.rerun()


def render_upload_task_queue(
    queue: list,
    placeholder=None,
    page_size: int = 10,
    show_remove_buttons: bool = True,
) -> None:
    """Render selected files and upload progress in one task queue."""
    if not queue:
        return

    def render_queue_body() -> None:
        label_map = {
            "waiting": "等待中",
            "processing": "处理中",
            "success": "成功",
            "failed": "失败",
        }
        total_files = len(queue)
        total_pages = max(1, (total_files + page_size - 1) // page_size)
        current_page = int(st.session_state.get("upload_preview_page", 1))
        current_page = max(1, min(current_page, total_pages))
        st.session_state.upload_preview_page = current_page
        start = (current_page - 1) * page_size
        end = start + page_size
        page_items = queue[start:end]

        success_count = sum(1 for item in queue if item.get("status") == "success")
        failed_count = sum(1 for item in queue if item.get("status") == "failed")
        processing_count = sum(1 for item in queue if item.get("status") == "processing")

        st.html(
            f"""
            <div class="upload-task-panel upload-task-panel-streamlit">
                <div class="upload-task-header">
                    <div class="upload-task-title">{icon_svg("upload")} 文件上传队列</div>
                    <div class="upload-task-summary">
                        <span>{icon_svg("file")} 共 {total_files}</span>
                        <span class="success">{icon_svg("check_circle")} 成功 {success_count}</span>
                        <span class="failed">{icon_svg("block")} 失败 {failed_count}</span>
                        <span class="processing">{icon_svg("activity")} 处理中 {processing_count}</span>
                    </div>
                </div>
            </div>
            """
        )

        for item in page_items:
            status = item.get("status", "waiting")
            item_key = item.get("key", "")
            item_hash = hashlib.md5(item_key.encode("utf-8")).hexdigest()[:10]
            safe_status = html.escape(status)
            safe_name = html.escape(item.get("name", ""))
            safe_size = html.escape(format_file_size(item.get("size", 0)))
            safe_message = html.escape(item.get("message", ""))
            safe_label = html.escape(label_map.get(status, status))
            failure_guidance = ""
            if status == "failed":
                safe_guidance = html.escape(get_upload_failure_guidance(item.get("name", ""), item.get("message", "")))
                failure_guidance = f'<div class="upload-task-guidance">{safe_guidance}</div>'

            row_html = f"""
                <div class="upload-task-row upload-task-row-native {safe_status}">
                    <span class="upload-task-icon">{icon_svg("description")}</span>
                    <div>
                        <div class="upload-task-name" title="{safe_name}">
                            {safe_name}
                        </div>
                        <div class="upload-task-message">
                            {safe_size} · {safe_message}
                        </div>
                        {failure_guidance}
                    </div>
                    <div class="upload-task-actions">
                        <span class="upload-task-badge {safe_status}">{safe_label}</span>
                    </div>
                </div>
            """

            if show_remove_buttons and status != "processing":
                with st.container(key=f"upload_task_native_{item_hash}"):
                    st.html(row_html)
                    if st.button(
                        "删除",
                        key=f"upload_remove_visible_{item_hash}",
                        help=f"移除 {item.get('name', '文件')}",
                    ):
                        remove_upload_queue_item(item_key)
            else:
                st.html(
                    row_html
                )

        st.html(
            f"""
            <div class="upload-task-footer upload-task-footer-native">
                <span>第 {current_page} 页 / 共 {total_pages} 页，每页最多 {page_size} 个文件</span>
            </div>
            """
        )

    if placeholder is None:
        render_queue_body()
    else:
        with placeholder.container():
            render_queue_body()


def run_upload_queue(uploaded_files: list, collection_name: str, retry_key: str = None, queue_placeholder=None) -> None:
    """Upload selected files while updating a per-file task queue."""
    queue = merge_upload_queue(uploaded_files)

    removed_keys = set(st.session_state.get("upload_removed_keys", []))
    queue_by_key = {item["key"]: item for item in queue}
    files_to_upload = [
        entry
        for entry in get_upload_file_entries(uploaded_files)
        if entry["key"] not in removed_keys
        and entry["key"] in queue_by_key
        and (
            (retry_key is None and queue_by_key[entry["key"]].get("status") == "waiting")
            or (retry_key is not None and entry["key"] == retry_key)
        )
    ]
    st.session_state.upload_task_queue = queue

    if queue_placeholder is None:
        queue_placeholder = st.empty()
    render_upload_task_queue(queue, queue_placeholder, show_remove_buttons=False)

    for entry in files_to_upload:
        file = entry["file"]
        file_key = entry["key"]
        if file_key not in queue_by_key:
            continue
        task = queue_by_key[file_key]
        task["status"] = "processing"
        task["message"] = "正在处理并写入知识库"
        render_upload_task_queue(queue, queue_placeholder, show_remove_buttons=False)

        result = upload_file(
            file,
            collection_name,
            chunk_size=st.session_state.settings_chunk_size,
            chunk_overlap=st.session_state.settings_chunk_overlap,
            enable_multimodal=st.session_state.settings_multimodal_parsing,
        )

        if result.get("success"):
            task["status"] = "success"
            task["message"] = result.get("message", "上传成功")
        else:
            task["status"] = "failed"
            task["message"] = (
                f"{result.get('message', '上传失败')}"
                f"{format_last_response_diagnostic_suffix(prefix='；')}"
            )

        st.session_state.upload_task_queue = queue
        render_upload_task_queue(queue, queue_placeholder, show_remove_buttons=False)


def render_upload_section(collection_name: str):
    """渲染文档上传区域。"""
    st.markdown(icon_label("upload", "文档上传"), unsafe_allow_html=True)
    render_section_intro(
        "upload",
        "把资料放进当前知识库",
        f"当前目标知识库：{collection_name or '未选择'}。上传后会按当前分块设置写入本地向量库；公开仓库不包含 Chroma、session、日志或密钥。",
    )

    uploader_nonce = int(st.session_state.get("upload_uploader_reset_nonce", 0))
    uploaded_files = st.file_uploader(
        "选择要上传的文档",
        type=["pdf", "txt", "docx", "md"],
        accept_multiple_files=True,
        help="支持 PDF、TXT、DOCX、Markdown 格式，单个文件最大 200MB",
        key=f"document_upload_{uploader_nonce}",
    )

    if uploaded_files:
        current_count = len(uploaded_files)
        current_signature = get_upload_signature(uploaded_files)
        previous_count = st.session_state.get("upload_preview_total")
        previous_signature = st.session_state.get("upload_preview_signature")
        if previous_count != current_count or previous_signature != current_signature:
            st.session_state.upload_preview_page = 1
            st.session_state.upload_preview_total = current_count
            st.session_state.upload_preview_signature = current_signature
            st.session_state.upload_task_queue = merge_upload_queue(uploaded_files)
            st.session_state.pop("upload_last_result", None)

        queue = st.session_state.get("upload_task_queue", [])
        queue = filter_removed_upload_queue(queue)
        st.session_state.upload_task_queue = queue
        render_upload_steps(queue)
        if not queue:
            st.session_state.pop("upload_last_result", None)
            st.html(
                f"""
                <div class="upload-empty-inline">
                    <span>{icon_svg("check_circle")}</span>
                    <div>
                        <strong>当前上传队列已清空</strong>
                        <small>如需继续上传，请在上方重新选择文件；已移除的文件不会再被本次处理。</small>
                    </div>
                </div>
                """
            )
            return
        handle_upload_queue_pagination(queue, page_size=10)
        queue_placeholder = st.empty()
        render_upload_task_queue(queue, queue_placeholder, page_size=10)

        waiting_tasks = [
            item
            for item in queue
            if item.get("status") == "waiting"
        ]
        if st.button(
            "开始上传并处理",
            key="upload_process_button",
            help=(
                "按当前分块和图片解析设置，将等待中的文件写入当前知识库"
                if waiting_tasks
                else "当前没有等待处理的文件；失败文件请先移除后重新选择"
            ),
            disabled=not waiting_tasks,
            use_container_width=True,
        ):
            run_upload_queue(uploaded_files, collection_name, queue_placeholder=queue_placeholder)
            queue = st.session_state.get("upload_task_queue", [])
            success_count = sum(1 for item in queue if item.get("status") == "success")
            failed_count = sum(1 for item in queue if item.get("status") == "failed")
            result_class = "failed" if failed_count else "success"
            result_text = (
                f"处理完成：成功 {success_count} 个，失败 {failed_count} 个。失败原因已显示在文件行中。"
                if failed_count
                else f"处理完成：{success_count} 个文件已写入知识库。"
            )
            st.session_state.upload_last_result = {
                "class": result_class,
                "text": result_text,
            }
            st.rerun()

        failed_tasks = [item for item in queue if item.get("status") == "failed"]
        last_result = st.session_state.get("upload_last_result")
        if last_result and not failed_tasks:
            result_class = html.escape(last_result.get("class", "success"))
            result_text = html.escape(last_result.get("text", ""))
            st.html(f'<div class="upload-result-inline {result_class}">{result_text}</div>')
    else:
        st.session_state.upload_preview_total = 0
        st.session_state.upload_preview_page = 1
        st.session_state.upload_preview_signature = []
        st.session_state.upload_removed_keys = []
        st.session_state.upload_task_queue = []
        render_upload_steps([])
        render_empty_state(
            "upload",
            "把脱敏资料拖进来，开始构建当前知识库",
            "支持批量选择文件。面试演示建议先上传少量脱敏 Markdown/PDF，方便马上展示问答、引用和拒答守卫。",
            [
                ("library", "同主题归档", "课程、项目和论文建议分库管理。"),
                ("layers", "先小批上传", "便于及时发现格式或大小问题。"),
                ("settings", "设置先确认", "分块参数只影响新上传文档。"),
            ],
        )
