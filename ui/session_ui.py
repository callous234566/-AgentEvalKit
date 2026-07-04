"""Session and collection UI helpers: share panel, confirm, badge."""

import html
import json

import streamlit as st
import streamlit.components.v1 as components

from ui.assets import icon_svg
from ui.export import (
    build_conversation_markdown,
    build_conversation_plain_text,
    build_conversation_pdf,
    get_safe_export_name,
)


def render_pending_session_share():
    """Copy text requested by lightweight share controls."""
    share_text = st.session_state.pop("pending_clipboard_text", "")
    if not share_text:
        return

    payload = json.dumps(share_text)
    components.html(
        f"""
        <script>
        (function () {{
            const text = {payload};
            const parentWindow = window.parent;
            function copyText(value) {{
                if (parentWindow.navigator.clipboard && parentWindow.navigator.clipboard.writeText) {{
                    return parentWindow.navigator.clipboard.writeText(value);
                }}
                const area = parentWindow.document.createElement("textarea");
                area.value = value;
                area.style.position = "fixed";
                area.style.opacity = "0";
                parentWindow.document.body.appendChild(area);
                area.focus();
                area.select();
                parentWindow.document.execCommand("copy");
                parentWindow.document.body.removeChild(area);
                return Promise.resolve();
            }}
            if (parentWindow.navigator.share) {{
                parentWindow.navigator.share({{ text }}).catch(function () {{
                    copyText(text);
                }});
            }} else {{
                copyText(text);
            }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def render_inline_confirm(kind: str, title: str, copy: str):
    """Render a compact inline confirmation panel."""
    panel_class = "inline-confirm-panel danger" if kind == "danger" else "inline-confirm-panel"
    st.markdown(
        f"""
        <div class="{panel_class}">
            <div class="inline-confirm-title">{icon_svg("trash" if kind == "danger" else "info")} {html.escape(title)}</div>
            <div class="inline-confirm-copy">{html.escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_share_panel():
    """Render a lightweight share/export panel for the selected session."""
    session_id = st.session_state.get("share_panel_session_id")
    if not session_id or session_id not in st.session_state.sessions:
        return

    session_data = st.session_state.sessions[session_id]
    session_name = session_data.get("name", "未命名会话")
    messages = session_data.get("messages", [])
    markdown_text = build_conversation_markdown(session_name, messages)
    plain_text = build_conversation_plain_text(session_name, messages)
    safe_name = get_safe_export_name(session_name)

    st.markdown(
        f"""
        <div class="share-panel">
            <div class="share-panel-title">{icon_svg("share")} 分享会话</div>
            <div class="share-panel-copy">{html.escape(session_name)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("复制 Markdown", icon=":material/content_copy:", key=f"share_copy_md_{session_id}", use_container_width=True):
            st.session_state.pending_clipboard_text = markdown_text
            st.toast("已复制 Markdown")
            st.rerun()
        st.download_button(
            "导出 Markdown",
            data=markdown_text.encode("utf-8"),
            file_name=f"{safe_name}.md",
            mime="text/markdown",
            icon=":material/download:",
            key=f"share_download_md_{session_id}",
            use_container_width=True,
        )
    with col2:
        if st.button("复制纯文本", icon=":material/article:", key=f"share_copy_txt_{session_id}", use_container_width=True):
            st.session_state.pending_clipboard_text = plain_text
            st.toast("已复制纯文本")
            st.rerun()
        st.download_button(
            "导出 PDF",
            data=build_conversation_pdf(markdown_text),
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            icon=":material/picture_as_pdf:",
            key=f"share_download_pdf_{session_id}",
            use_container_width=True,
        )
    if st.button("收起分享面板", icon=":material/close:", key=f"share_close_{session_id}", use_container_width=True):
        st.session_state.share_panel_session_id = None
        st.rerun()


def render_current_collection_badge(collection_name: str):
    """Render a compact current-collection status badge."""
    safe_name = html.escape(collection_name or "default")
    st.markdown(
        f"""
        <div class="current-collection-badge">
            {icon_svg("library")}
            <div>
                <span>当前知识库</span>
                <strong>{safe_name}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
