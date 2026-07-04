"""HTML rendering components: messages, sources, items, hero, overview."""

import html
import streamlit as st

from rag.session_state import get_session_name
from ui.api_wrappers import list_documents_api
from ui.assets import icon_svg
from ui.text_utils import (
    _normalize_message_text,
    _message_text_to_html,
    _copy_payload,
    get_source_display_name,
    format_file_size,
)


def render_section_intro(icon_name: str, title: str, copy: str) -> None:
    """Render a compact guidance card above a main workspace section."""
    st.html(
        f"""
        <div class="section-intro">
            {icon_svg(icon_name)}
            <div>
                <div class="section-intro-title">{html.escape(title)}</div>
                <div class="section-intro-copy">{html.escape(copy)}</div>
            </div>
        </div>
        """
    )


def render_status_notice(kind: str, message: str, title: str = None) -> None:
    """Render a compact app-native status notice instead of Streamlit alert blocks."""
    kind_map = {
        "info": ("info", "提示"),
        "success": ("check_circle", "已完成"),
        "warning": ("block", "请注意"),
        "error": ("block", "操作失败"),
    }
    icon_name, fallback_title = kind_map.get(kind, kind_map["info"])
    icon_class = _safe_icon_class("status-icon", icon_name)
    safe_kind = html.escape(kind if kind in kind_map else "info")
    safe_title = html.escape(title or fallback_title)
    safe_message = html.escape(str(message or ""))
    st.html(
        f"""
        <div class="status-notice {safe_kind}" role="status">
            <span class="status-notice-icon {icon_class}" aria-hidden="true"></span>
            <span class="status-notice-copy">
                <strong>{safe_title}</strong>
                <small>{safe_message}</small>
            </span>
        </div>
        """
    )


def _safe_icon_class(prefix: str, icon_name: str) -> str:
    """Return a safe CSS class for icon mask rendering."""
    safe_name = "".join(ch for ch in str(icon_name or "") if ch.isalnum() or ch in {"_", "-"})
    return f"{prefix}-{safe_name or 'info'}"


def _empty_icon_class(icon_name: str) -> str:
    """Return a safe CSS class for empty-state icon masks."""
    return _safe_icon_class("empty-icon", icon_name)


def render_empty_state(icon_name: str, title: str, copy: str, steps: list[tuple[str, str, str]]) -> None:
    """Render a shared empty-state card for primary workspace pages."""
    step_html = "".join(
        f"""
        <div class="workspace-empty-step">
            <span class="workspace-empty-step-icon {_empty_icon_class(step_icon)}" aria-hidden="true"></span>
            <span>
                <strong>{html.escape(step_title)}</strong>
                <small>{html.escape(step_copy)}</small>
            </span>
        </div>
        """
        for step_icon, step_title, step_copy in steps
    )
    st.html(
        f"""
        <div class="workspace-empty-state">
            <div class="workspace-empty-heading">
                <span class="workspace-empty-icon {_empty_icon_class(icon_name)}" aria-hidden="true"></span>
                <div>
                    <div class="workspace-empty-title">{html.escape(title)}</div>
                    <div class="workspace-empty-copy">{html.escape(copy)}</div>
                </div>
            </div>
            <div class="workspace-empty-steps">{step_html}</div>
        </div>
        """
    )


def render_settings_summary() -> None:
    """Render the effective frontend settings as compact status chips."""
    toggles = [
        ("refresh", "查询重写", bool(st.session_state.settings_query_rewrite)),
        ("layers", "上下文压缩", bool(st.session_state.settings_contextual_compression)),
        ("activity", "思考过程", bool(st.session_state.settings_show_thinking)),
        ("file", "图片解析", bool(st.session_state.settings_multimodal_parsing)),
    ]
    chips = [
        (
            f'<span class="settings-chip">{icon_svg("database")}'
            f'检索片段 <strong>{int(st.session_state.settings_top_k)}</strong></span>'
        ),
        (
            f'<span class="settings-chip">{icon_svg("layers")}分块 '
            f'<strong>{int(st.session_state.settings_chunk_size)} / {int(st.session_state.settings_chunk_overlap)}</strong>'
            '</span>'
        ),
        (
            f'<span class="settings-chip">{icon_svg("activity")}'
            f'Temperature <strong>{float(st.session_state.settings_temperature):.2f}</strong></span>'
        ),
    ]
    chips.extend(
        f'<span class="settings-chip {"on" if enabled else "off"}">{icon_svg(icon)}{html.escape(label)} '
        f'<strong>{"开启" if enabled else "关闭"}</strong></span>'
        for icon, label, enabled in toggles
    )
    st.html(f'<div class="settings-summary">{"".join(chips)}</div>')


def render_chat_context_bar(collection_name: str) -> None:
    """Render compact context for the active conversation."""
    session_name = get_session_name(st.session_state.get("current_session_id", ""))
    message_count = len(st.session_state.get("chat_history", []))
    rewrite_label = "开" if st.session_state.settings_query_rewrite else "关"
    compression_label = "开" if st.session_state.settings_contextual_compression else "关"
    st.html(
        f"""
        <div class="chat-context-bar">
            <span class="chat-context-item">知识库 <strong title="{html.escape(collection_name or '未选择')}">{html.escape(collection_name or '未选择')}</strong></span>
            <span class="chat-context-dot"></span>
            <span class="chat-context-item">会话 <strong title="{html.escape(session_name)}">{html.escape(session_name)}</strong></span>
            <span class="chat-context-dot"></span>
            <span class="chat-context-item">消息 <strong>{message_count} 条</strong></span>
            <span class="chat-context-dot"></span>
            <span class="chat-context-item">检索 <strong>Top {int(st.session_state.settings_top_k)}</strong></span>
            <span class="chat-context-dot"></span>
            <span class="chat-context-item">增强 <strong>重写{rewrite_label} / 压缩{compression_label}</strong></span>
        </div>
        """
    )


def render_workspace_overview(collection_name: str) -> None:
    """Render high-level state so the main workspace feels anchored."""
    documents_label = "暂未加载"
    documents_copy = "文档管理页会显示详情"
    document_health = ""
    result = list_documents_api(collection_name) if collection_name else {"success": False}
    if result.get("success"):
        documents = result.get("documents", [])
        enabled_count = sum(1 for doc in documents if doc.get("enabled", True))
        disabled_count = len(documents) - enabled_count
        upload_times = [str(doc.get("upload_time") or "") for doc in documents if doc.get("upload_time")]
        latest_upload = max(upload_times) if upload_times else "暂无上传记录"
        documents_label = f"{enabled_count} 启用 / {disabled_count} 禁用"
        documents_copy = f"最近上传：{latest_upload}"
        document_health = f"""
            <div class="workspace-mini-stats">
                <span class="workspace-mini-stat active">启用 {enabled_count}</span>
                <span class="workspace-mini-stat muted">禁用 {disabled_count}</span>
                <span class="workspace-mini-stat">总计 {len(documents)}</span>
            </div>
        """

    current_session = get_session_name(st.session_state.get("current_session_id", ""))
    message_count = len(st.session_state.get("chat_history", []))
    st.html(
        f"""
        <div class="workspace-overview">
            <div class="workspace-card workspace-card-primary">
                <div class="workspace-card-top">
                    <span class="workspace-icon-badge">{icon_svg("database")}</span>
                    <span class="workspace-card-label">当前知识库</span>
                </div>
                <div class="workspace-card-value" title="{html.escape(collection_name or '未选择')}">{html.escape(collection_name or '未选择')}</div>
                <div class="workspace-card-copy">本地持久化，中文名称映射，公开演示不提交私有向量库</div>
            </div>
            <div class="workspace-card workspace-card-docs">
                <div class="workspace-card-top">
                    <span class="workspace-icon-badge">{icon_svg("layers")}</span>
                    <span class="workspace-card-label">文档状态</span>
                </div>
                <div class="workspace-card-value">{html.escape(documents_label)}</div>
                {document_health}
                <div class="workspace-card-copy">{html.escape(documents_copy)} · 支持引用、分数和检索 trace</div>
            </div>
            <div class="workspace-card workspace-card-session">
                <div class="workspace-card-top">
                    <span class="workspace-icon-badge">{icon_svg("message")}</span>
                    <span class="workspace-card-label">当前会话</span>
                </div>
                <div class="workspace-card-value" title="{html.escape(current_session)}">{html.escape(current_session)}</div>
                <div class="workspace-card-copy">已有 {message_count} 条消息，可导出复盘，并用排障 ID 对齐后端日志</div>
            </div>
        </div>
        """
    )


def render_app_hero() -> None:
    """Render the product header without relying on Streamlit heading defaults."""
    st.html(
        f"""
        <div class="app-hero">
            <div class="app-hero-orb">{icon_svg("sparkles")}</div>
            <div class="app-hero-kicker">{icon_svg("activity")} Interview-ready RAG Workbench</div>
            <div class="app-hero-title">{icon_svg("bot")} 个人 RAG 知识库助手</div>
            <div class="app-hero-copy">
                把本地文档变成可追溯、可管理、可评测的中文知识工作台。
                覆盖上传入库、混合检索、Agent/Web 补充、引用证据和 request id 排障闭环。
            </div>
            <div class="app-hero-tags">
                <span>{icon_svg("database")} 本地 RAG</span>
                <span>{icon_svg("layers")} 混合检索</span>
                <span>{icon_svg("bot")} Agent/Web</span>
                <span>{icon_svg("check_circle")} 引用可追溯</span>
                <span>{icon_svg("activity")} 排障 ID</span>
            </div>
        </div>
        """
    )


def render_user_message_html(content: str, anchor_id: str = None) -> str:
    id_attr = f' id="{html.escape(anchor_id, quote=True)}"' if anchor_id else ""
    return f"""
    <div class="message-row user"{id_attr}>
        <div class="avatar user-avatar">{icon_svg("message")}</div>
        <div class="user-message">{_message_text_to_html(content)}</div>
    </div>
    """


def render_ai_message_html(
    content: str,
    message_index: int = None,
    show_actions: bool = True,
    typing: bool = False,
    anchor_id: str = None,
    status_html: str = "",
) -> str:
    """渲染 AI 气泡，历史回答可复制并可重新生成。"""
    content_html = _message_text_to_html(content)
    cursor_class = " typing-cursor" if typing else ""
    action_class = " has-actions" if show_actions else ""
    id_attr = f' id="{html.escape(anchor_id, quote=True)}"' if anchor_id else ""
    disabled_attr = ' disabled aria-disabled="true"' if st.session_state.get("is_generating", False) else ""
    copy_button = ""
    regenerate_action = ""

    if show_actions:
        copy_button = (
            f'<button type="button" class="answer-copy-btn" '
            f'data-copy="{_copy_payload(content)}" title="复制回答" aria-label="复制回答"{disabled_attr}>{icon_svg("copy")} 复制</button>'
        )
        if message_index is not None:
            regenerate_action = f"""
            <div class="answer-actions">
                <button type="button" class="answer-regenerate-btn"
                        data-message-index="{message_index}"
                        title="重新生成回答" aria-label="重新生成回答"{disabled_attr}>{icon_svg("refresh")}</button>
            </div>
            """

    return f"""
    <div class="message-row ai"{id_attr}>
        <div class="avatar ai-avatar">{icon_svg("sparkles")}</div>
        <div class="ai-message{cursor_class}{action_class}">
            {copy_button}
            {status_html}
            <div class="message-content">{content_html}</div>
            {regenerate_action}
        </div>
    </div>
    """


def render_answer_status_bar(
    sources: list = None,
    agent_steps: list = None,
    debug_info: dict = None,
    answer: str = "",
) -> str:
    """Render a compact source/model status row inside an AI answer."""
    sources = sources or []
    agent_steps = agent_steps or []
    debug_info = debug_info or {}
    evidence_summary = debug_info.get("evidence_summary") or {}

    chips = []
    mode = evidence_summary.get("mode") or ""
    if sources or evidence_summary.get("local_used") or mode in {"local_only", "local_plus_web"}:
        chips.append(("database", "本地资料"))
    if evidence_summary.get("web_used") or mode in {"web_only", "local_plus_web"}:
        provider = evidence_summary.get("web_provider") or "Web"
        chips.append(("search", f"{provider} 补充"))
    if agent_steps or debug_info:
        chips.append(("bot", "Agent"))
    if sources:
        highest_score = max(float(source.get("score", 0) or 0) for source in sources)
        chips.append(("library", f"引用 {len(sources)} 条"))
        chips.append(("activity", f"最高分 {highest_score:.2f}"))
    if evidence_summary.get("local_fallback_used"):
        chips.append(("refresh", "本地兜底"))
    if "根据现有资料无法回答该问题" in str(answer or "") and not sources:
        chips.append(("block", "未找到覆盖问题实体的资料"))

    if not chips:
        chips.append(("sparkles", "模型回答"))

    chip_html = "".join(
        f'<span class="answer-status-chip">{icon_svg(icon)}{html.escape(label)}</span>'
        for icon, label in chips[:5]
    )
    return f'<div class="answer-status-bar" aria-label="回答证据状态">{chip_html}</div>'


def render_source_evidence_html(sources: list) -> str:
    """Render compact evidence cards below an AI answer."""
    if not sources:
        return ""

    highest_score = max(float(source.get("score", 0) or 0) for source in sources)
    source_count = len(sources)
    cards = []
    all_citations = []
    for idx, source in enumerate(sources, 1):
        source_name = get_source_display_name(source)
        source_content = source.get("content", "")
        source_score = float(source.get("score", 0) or 0)
        candidate_source = source.get("candidate_source") or source.get("retrieval_source") or "hybrid"
        vector_score = source.get("vector_score")
        keyword_score = source.get("keyword_score")
        chunk_label = source.get("chunk_id") or source.get("chunk_index") or source.get("id") or ""
        trace_bits = [f"候选 {candidate_source}"]
        if vector_score is not None:
            trace_bits.append(f"vector {float(vector_score or 0):.2f}")
        if keyword_score is not None:
            trace_bits.append(f"keyword {float(keyword_score or 0):.2f}")
        if chunk_label != "":
            trace_bits.append(f"chunk {chunk_label}")
        trace_html = "".join(
            f'<span class="source-trace-chip">{html.escape(str(bit))}</span>'
            for bit in trace_bits
        )
        citation_text = (
            f"引用来源：{source_name}\n"
            f"相似度：{source_score:.2f}\n\n"
            f"{_normalize_message_text(source_content)}"
        )
        all_citations.append(f"{idx}. {citation_text}")
        cards.append(
            f"""
            <div class="source-box">
                <div class="source-title">
                    <span class="source-index">来源 #{idx}</span>
                    <span class="source-file">{icon_svg('file')} {html.escape(str(source_name))}</span>
                    <span class="source-score">相似度 {source_score:.2f}</span>
                    <button type="button" class="source-copy-btn" data-copy="{_copy_payload(citation_text)}"
                            title="复制该条引用" aria-label="复制引用：{html.escape(str(source_name), quote=True)}">{icon_svg("copy")} 复制</button>
                </div>
                <div class="source-trace-row">{trace_html}</div>
                <div class="source-label">证据片段</div>
                <div class="source-content">{_message_text_to_html(source_content)}</div>
            </div>
            """
        )

    return f"""
    <details class="source-evidence">
        <summary aria-label="展开或收起引用来源，共 {source_count} 条">
            <span class="source-evidence-title">{icon_svg("library")} 引用证据 {source_count} 条</span>
            <span class="source-evidence-actions">
                <span class="source-evidence-meta">最高相似度 {highest_score:.2f}</span>
                <button type="button" class="source-copy-btn source-copy-all"
                        data-copy="{_copy_payload(chr(10).join(all_citations))}"
                        title="复制全部引用" aria-label="复制全部 {source_count} 条引用"
                        onclick="event.preventDefault(); event.stopPropagation();">{icon_svg("copy")} 全部复制</button>
            </span>
        </summary>
        <div class="source-evidence-body">
            {''.join(cards)}
        </div>
    </details>
    """
