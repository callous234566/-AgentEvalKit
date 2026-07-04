"""Sidebar rendering: collection management, session management."""

import hashlib
import html

import streamlit as st

import config
from rag.session_state import (
    create_new_session,
    switch_session,
    delete_session,
    rename_session,
    persist_sessions,
)
from ui.api_wrappers import (
    check_api_connection,
    get_collections,
    list_documents_api,
    create_collection_api,
    delete_collection_api,
    rename_collection_api,
    format_last_response_diagnostic_suffix,
)
from ui.assets import icon_label, icon_svg
from ui.components import render_status_notice
from ui.export import build_conversation_markdown
from ui.session_ui import (
    render_pending_session_share,
    render_current_collection_badge,
    render_session_share_panel,
)

# Injected by streamlit_app.py at startup
API_BASE_URL = None
SESSION_STORE_PATH = None


def _collection_project_meta(collection_name: str) -> str:
    """Return compact project metadata for one knowledge space."""
    result = list_documents_api(collection_name)
    if not result.get("success"):
        return "资料待同步 · 本地知识空间"

    documents = result.get("documents", [])
    enabled_count = sum(1 for doc in documents if doc.get("enabled", True))
    latest_upload = max(
        (str(doc.get("upload_time") or "") for doc in documents if doc.get("upload_time")),
        default="暂无上传",
    )
    if len(latest_upload) > 10:
        latest_upload = latest_upload[:10]
    return f"{enabled_count}/{len(documents)} 文档启用 · 最近 {latest_upload}"


def init_sidebar(api_base, store_path):
    global API_BASE_URL, SESSION_STORE_PATH
    API_BASE_URL = api_base
    SESSION_STORE_PATH = store_path


@st.dialog("确认删除知识库")
def render_delete_collection_dialog(delete_name: str):
    """Confirm deleting a collection in a modal dialog."""
    st.html(
        f"""
        <div class="doc-confirm-panel">
            <div class="doc-confirm-icon">{icon_svg("trash")}</div>
            <div>
                <div class="doc-confirm-title">确定删除知识库「{html.escape(delete_name)}」吗？</div>
                <div class="doc-confirm-copy">该操作会删除知识库中的所有文档和向量片段。</div>
                <div class="doc-confirm-hint">删除后不可恢复，请确认当前知识库不再需要。</div>
            </div>
        </div>
        """
    )
    confirm_col, cancel_col = st.columns(2)
    with confirm_col:
        if st.button("确认删除", icon=":material/delete_forever:", type="primary", key=f"confirm_delete_collection_{delete_name}", use_container_width=True):
            if delete_collection_api(delete_name):
                st.session_state.delete_collection_name = None
                if st.session_state.get("pinned_collection") == delete_name:
                    st.session_state.pinned_collection = None
                remaining = [name for name in get_collections() if name != delete_name]
                st.session_state.current_collection = remaining[0] if remaining else "default"
                st.toast(f"知识库「{delete_name}」已删除")
                st.rerun()
            else:
                render_status_notice("error", f"删除失败，请稍后重试。{format_last_response_diagnostic_suffix()}")
    with cancel_col:
        if st.button("取消", icon=":material/close:", key=f"cancel_delete_collection_{delete_name}", use_container_width=True):
            st.session_state.delete_collection_name = None
            st.rerun()


@st.dialog("确认删除会话")
def render_delete_session_dialog(delete_id: str):
    """Confirm deleting a session in a modal dialog."""
    session_data = st.session_state.sessions.get(delete_id, {})
    delete_name = session_data.get("name", "新会话")
    st.html(
        f"""
        <div class="doc-confirm-panel">
            <div class="doc-confirm-icon">{icon_svg("trash")}</div>
            <div>
                <div class="doc-confirm-title">确定删除会话「{html.escape(delete_name)}」吗？</div>
                <div class="doc-confirm-copy">该操作会删除当前会话中的历史消息。</div>
                <div class="doc-confirm-hint">不会删除知识库文档，但会话内容不可恢复。</div>
            </div>
        </div>
        """
    )
    confirm_col, cancel_col = st.columns(2)
    with confirm_col:
        if st.button("确认删除", icon=":material/delete_forever:", type="primary", key=f"confirm_delete_session_{delete_id}", use_container_width=True):
            delete_session(delete_id, SESSION_STORE_PATH)
            if st.session_state.get("pinned_session_id") == delete_id:
                st.session_state.pinned_session_id = None
            if st.session_state.get("share_panel_session_id") == delete_id:
                st.session_state.share_panel_session_id = None
            st.session_state.delete_session_id = None
            st.session_state.rename_session_id = None
            st.toast(f"会话「{delete_name}」已删除")
            st.rerun()
    with cancel_col:
        if st.button("取消", icon=":material/close:", key=f"cancel_delete_session_{delete_id}", use_container_width=True):
            st.session_state.delete_session_id = None
            st.rerun()


def render_sidebar():
    """Render the compact product-style sidebar."""
    with st.sidebar:
        render_pending_session_share()

        st.markdown(
            f"<div class='sidebar-main-header'>{icon_svg('library')} AI 工作空间</div>",
            unsafe_allow_html=True,
        )

        if not check_api_connection():
            st.html('<div class="sidebar-api-fail">无法连接到后端服务，请确认 FastAPI 服务已启动</div>')
            render_status_notice("info", f"请运行 python main.py，服务应在 {API_BASE_URL} 运行。", "后端服务未连接")
            return None

        if config.check_api_key():
            st.html('<div class="sidebar-api-ok">模型 API 密钥已配置</div>')
        else:
            st.html('<div class="sidebar-api-fail">模型 API 密钥未配置</div>')
            render_status_notice("info", "请复制 .env.example 为 .env，并填写 SiliconFlow API 密钥。", "需要配置密钥")

        st.divider()
        st.markdown(icon_label("library", "知识空间"), unsafe_allow_html=True)

        collections = get_collections()
        with st.expander("创建知识空间", expanded=False):
            new_collection = st.text_input(
                "创建新知识库",
                placeholder="输入知识库名称",
                help="知识库名称支持中文、字母、数字、下划线和横线。",
            )

            if st.button("创建知识空间", icon=":material/add:", use_container_width=True, key="create_collection_btn"):
                if not new_collection:
                    render_status_notice("warning", "请输入知识库名称")
                elif new_collection in collections:
                    render_status_notice("warning", "该知识库已存在")
                else:
                    result = create_collection_api(new_collection)
                    if result.get("success"):
                        st.session_state.current_collection = new_collection
                        st.toast(f"知识库「{new_collection}」已创建")
                        st.rerun()
                    else:
                        render_status_notice(
                            "error",
                            f"{result.get('message', '创建失败')}{format_last_response_diagnostic_suffix()}",
                        )

        if collections:
            if "pinned_collection" not in st.session_state:
                st.session_state.pinned_collection = None
            pinned = st.session_state.pinned_collection
            if pinned in collections:
                collection_options = [pinned] + [name for name in collections if name != pinned]
            else:
                collection_options = collections
                st.session_state.pinned_collection = None

            current_collection = st.session_state.get("current_collection", collection_options[0])
            if current_collection not in collection_options:
                current_collection = collection_options[0]
            st.session_state.current_collection = current_collection

            st.caption("选择项目 / 知识空间")
            for collection_name in collection_options:
                collection_id = hashlib.md5(collection_name.encode("utf-8")).hexdigest()[:10]
                is_active = collection_name == current_collection
                is_pinned = collection_name == st.session_state.get("pinned_collection")
                if st.session_state.rename_collection_name == collection_name:
                    with st.form(f"rename_collection_form_{collection_id}"):
                        new_name = st.text_input("新知识库名称", value=collection_name, max_chars=80, label_visibility="collapsed")
                        save_col, cancel_col = st.columns(2)
                        with save_col:
                            rename_submit = st.form_submit_button("保存", icon=":material/save:", use_container_width=True)
                        with cancel_col:
                            rename_cancel = st.form_submit_button("取消", icon=":material/close:", use_container_width=True)
                        if rename_submit:
                            result = rename_collection_api(collection_name, new_name)
                            if result.get("success"):
                                st.session_state.current_collection = result.get("new_name", new_name)
                                if st.session_state.get("pinned_collection") == collection_name:
                                    st.session_state.pinned_collection = st.session_state.current_collection
                                st.session_state.rename_collection_name = None
                                st.toast("知识库已重命名")
                                st.rerun()
                            else:
                                render_status_notice(
                                    "error",
                                    f"{result.get('message', '重命名失败')}{format_last_response_diagnostic_suffix()}",
                                )
                        if rename_cancel:
                            st.session_state.rename_collection_name = None
                            st.rerun()
                else:
                    with st.container(key=f"collection_item_wrap_{collection_id}"):
                        if is_pinned:
                            st.html('<span class="sidebar-pinned-marker" aria-label="已置顶"></span>')
                        safe_meta = html.escape(_collection_project_meta(collection_name))
                        st.html(f'<div class="sidebar-row-meta">{safe_meta}</div>')
                        select_col, menu_col = st.columns([0.82, 0.18], gap="small")
                        row_label = collection_name
                        with select_col:
                            if st.button(
                                row_label,
                                key=f"collection_row_select_{collection_id}",
                                use_container_width=True,
                            ):
                                st.session_state.current_collection = collection_name
                                st.session_state.open_collection_actions_id = None
                                st.rerun()
                        with menu_col:
                            if st.button(
                                "⋯",
                                key=f"collection_row_more_{collection_id}",
                                use_container_width=True,
                            ):
                                current_menu = st.session_state.get("open_collection_actions_id")
                                st.session_state.open_collection_actions_id = None if current_menu == collection_id else collection_id
                                st.session_state.open_session_actions_id = None

                        if st.session_state.get("open_collection_actions_id") == collection_id:
                            with st.container(key=f"collection_action_panel_{collection_id}"):
                                if st.button(
                                    "已置顶" if is_pinned else "置顶",
                                    key=f"collection_action_pin_{collection_id}",
                                    use_container_width=True,
                                    disabled=is_pinned,
                                ):
                                    st.session_state.pinned_collection = collection_name
                                    st.session_state.open_collection_actions_id = None
                                    st.rerun()
                                if st.button("重命名", key=f"collection_action_rename_{collection_id}", use_container_width=True):
                                    st.session_state.rename_collection_name = collection_name
                                    st.session_state.open_collection_actions_id = None
                                    st.rerun()
                                if st.button("删除", key=f"collection_action_delete_{collection_id}", use_container_width=True):
                                    st.session_state.delete_collection_name = collection_name
                                    st.session_state.open_collection_actions_id = None
                                    st.rerun()

        else:
            render_status_notice("info", "暂无知识库，请先创建一个。")
            if "current_collection" not in st.session_state:
                st.session_state.current_collection = "default"

        current = st.session_state.get("current_collection", "default")
        render_current_collection_badge(current)

        if st.session_state.delete_collection_name:
            render_delete_collection_dialog(st.session_state.delete_collection_name)

        st.divider()
        st.markdown(icon_label("message", "最近对话"), unsafe_allow_html=True)
        st.html('<div class="sidebar-section-copy">跟随当前知识空间，适合像 ChatGPT Projects 一样复盘同一主题。</div>')

        if st.button("新建会话", icon=":material/add_comment:", use_container_width=True, key="new_session_btn"):
            new_session_id = create_new_session(SESSION_STORE_PATH)
            switch_session(new_session_id, SESSION_STORE_PATH)
            st.rerun()

        if st.session_state.sessions:
            if "pinned_session_id" not in st.session_state:
                st.session_state.pinned_session_id = None
            session_items = list(st.session_state.sessions.items())
            pinned_session_id = next(
                (session_id for session_id, data in session_items if data.get("pinned")),
                st.session_state.get("pinned_session_id"),
            )
            if pinned_session_id in st.session_state.sessions:
                st.session_state.pinned_session_id = pinned_session_id
                session_items = [(sid, data) for sid, data in session_items if sid == pinned_session_id] + [
                    (sid, data) for sid, data in session_items if sid != pinned_session_id
                ]
            else:
                st.session_state.pinned_session_id = None

            for session_id, session_data in session_items:
                session_name = session_data.get("name", "新会话")
                is_active = session_id == st.session_state.current_session_id
                is_pinned = session_id == st.session_state.get("pinned_session_id")
                share_text = build_conversation_markdown(session_name, session_data.get("messages", []))

                with st.container(key=f"session_item_wrap_{session_id}"):
                    if is_pinned:
                        st.html('<span class="sidebar-pinned-marker" aria-label="已置顶"></span>')
                    select_col, menu_col = st.columns([0.82, 0.18], gap="small")
                    row_label = session_name
                    with select_col:
                        if st.button(
                            row_label,
                            key=f"session_row_select_{session_id}",
                            use_container_width=True,
                        ):
                            switch_session(session_id, SESSION_STORE_PATH)
                            st.session_state.open_session_actions_id = None
                            st.rerun()
                    with menu_col:
                        if st.button(
                            "⋯",
                            key=f"session_row_more_{session_id}",
                            use_container_width=True,
                        ):
                            current_menu = st.session_state.get("open_session_actions_id")
                            st.session_state.open_session_actions_id = None if current_menu == session_id else session_id
                            st.session_state.open_collection_actions_id = None

                    if st.session_state.get("open_session_actions_id") == session_id:
                        with st.container(key=f"session_action_panel_{session_id}"):
                            if st.button("分享", key=f"session_action_share_{session_id}", use_container_width=True):
                                st.session_state.share_panel_session_id = session_id
                                st.session_state.pending_clipboard_text = share_text
                                st.session_state.open_session_actions_id = None
                                st.toast("已复制会话内容")
                                st.rerun()
                            if st.button(
                                "已置顶" if is_pinned else "置顶",
                                key=f"session_action_pin_{session_id}",
                                use_container_width=True,
                                disabled=is_pinned,
                            ):
                                st.session_state.pinned_session_id = session_id
                                for item in st.session_state.sessions.values():
                                    item["pinned"] = False
                                st.session_state.sessions[session_id]["pinned"] = True
                                persist_sessions(SESSION_STORE_PATH)
                                st.session_state.open_session_actions_id = None
                                st.rerun()
                            if st.button("重命名", key=f"session_action_rename_{session_id}", use_container_width=True):
                                st.session_state.rename_session_id = session_id
                                st.session_state.delete_session_id = None
                                st.session_state.open_session_actions_id = None
                                st.rerun()
                            if st.button("删除", key=f"session_action_delete_{session_id}", use_container_width=True):
                                st.session_state.delete_session_id = session_id
                                st.session_state.rename_session_id = None
                                st.session_state.open_session_actions_id = None
                                st.rerun()

        else:
            render_status_notice("info", "暂无会话")

        render_session_share_panel()

        if st.session_state.rename_session_id in st.session_state.sessions:
            rename_id = st.session_state.rename_session_id
            current_name = st.session_state.sessions[rename_id].get("name", "新会话")
            with st.form("rename_session_form"):
                new_name = st.text_input("重命名会话", value=current_name, max_chars=40, key=f"rename_input_{rename_id}")
                save_col, cancel_col = st.columns(2)
                with save_col:
                    save_rename = st.form_submit_button("保存", icon=":material/save:", use_container_width=True)
                with cancel_col:
                    cancel_rename = st.form_submit_button("取消", icon=":material/close:", use_container_width=True)
                if save_rename:
                    rename_session(rename_id, new_name, SESSION_STORE_PATH)
                    st.session_state.rename_session_id = None
                    st.rerun()
                if cancel_rename:
                    st.session_state.rename_session_id = None
                    st.rerun()

        if st.session_state.delete_session_id in st.session_state.sessions:
            render_delete_session_dialog(st.session_state.delete_session_id)

        st.divider()
        with st.expander("使用说明", expanded=False):
            st.markdown(
                """
                1. **创建知识库**：在左侧输入名称创建新的知识库。
                2. **上传文档**：在主界面选择文件上传，支持 PDF、TXT、DOCX、MD。
                3. **开始问答**：文档处理完成后，在问答页输入问题。
                4. **查看引用**：答案下方会显示引用的文档来源。
                5. **管理会话**：可以为不同主题创建独立会话。
                """
            )

        return current
