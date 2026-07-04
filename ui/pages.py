"""Document management and settings panel pages."""

import hashlib
import html
from pathlib import Path

import streamlit as st

from ui.api_wrappers import (
    list_documents_api,
    batch_delete_documents_api,
    toggle_document_enabled_api,
    format_last_response_diagnostic_suffix,
)
from ui.assets import icon_svg
from ui.components import (
    render_empty_state,
    render_section_intro,
    render_settings_summary,
    render_status_notice,
)
from ui.text_utils import format_file_size


def _doc_hash(source: str) -> str:
    return hashlib.md5(source.encode("utf-8")).hexdigest()[:10]


def _set_selected_documents(sources: set[str]) -> None:
    """Update selected document sources and keep checkbox widgets in sync."""
    st.session_state.selected_documents = set(sources)
    for source in sources:
        st.session_state[f"doc_sel_{_doc_hash(source)}"] = True


def _clear_selected_documents(all_sources: set[str]) -> None:
    """Clear current document selection and matching checkbox widgets."""
    st.session_state.selected_documents = set()
    for source in all_sources:
        st.session_state[f"doc_sel_{_doc_hash(source)}"] = False


@st.dialog("确认删除文档")
def render_batch_delete_dialog(collection_name: str, documents: list, selected_sources: list[str]) -> None:
    """Render destructive batch delete confirmation as a modal dialog."""
    selected_set = set(selected_sources)
    names = [
        doc.get("name") or Path(doc.get("source", "")).name or "未知文档"
        for doc in documents
        if doc.get("source", "") in selected_set
    ]
    preview = "、".join(f"「{html.escape(name)}」" for name in names[:6])
    if len(names) > 6:
        preview += f" 等共 {len(names)} 个文档"

    st.html(
        f"""
        <div class="doc-confirm-panel">
            <div class="doc-confirm-icon">{icon_svg("trash")}</div>
            <div>
                <div class="doc-confirm-title">确定删除选中的 {len(selected_sources)} 个文档吗？</div>
                <div class="doc-confirm-copy">{preview}</div>
                <div class="doc-confirm-hint">删除会从当前知识库移除这些文档及其向量片段，此操作不可撤销。</div>
            </div>
        </div>
        """
    )
    confirm_col, cancel_col = st.columns(2)
    with confirm_col:
        if st.button("确认删除", icon=":material/delete_forever:", type="primary", use_container_width=True, key="batch_delete_confirm_yes"):
            del_result = batch_delete_documents_api(collection_name, selected_sources)
            if del_result.get("success"):
                _clear_selected_documents(selected_set)
                st.session_state.batch_delete_confirm = False
                st.toast(f"已删除 {del_result.get('deleted_count', 0)} 个文档")
                st.rerun()
            else:
                render_status_notice(
                    "error",
                    f"{del_result.get('message', '批量删除失败')}{format_last_response_diagnostic_suffix()}",
                )
    with cancel_col:
        if st.button("取消", icon=":material/close:", use_container_width=True, key="batch_delete_confirm_no"):
            st.session_state.batch_delete_confirm = False
            st.rerun()


def _toggle_selected_documents(collection_name: str, selected_sources: set[str], enabled: bool) -> tuple[int, int]:
    """Enable or disable selected documents and return success/failure counts."""
    ok, fail = 0, 0
    for source in selected_sources:
        result = toggle_document_enabled_api(collection_name, source, enabled)
        if result.get("success"):
            ok += 1
        else:
            fail += 1
    return ok, fail


def _document_display_name(doc: dict) -> str:
    """Return the user-facing document name."""
    source = doc.get("source", "")
    return doc.get("name") or Path(source).name or "未知文档"


def _document_sort_value(doc: dict, sort_mode: str):
    """Return a stable sort value for document management controls."""
    if sort_mode == "文件名 A-Z":
        return _document_display_name(doc).casefold()
    if sort_mode == "文件大小大到小":
        return int(doc.get("size") or 0)
    if sort_mode == "分块数多到少":
        return int(doc.get("chunk_count") or 0)
    return str(doc.get("upload_time") or "")


def _filter_and_sort_documents(documents: list, query: str, status_filter: str, sort_mode: str) -> list:
    """Apply document search, status filter and sorting."""
    normalized_query = (query or "").strip().casefold()
    filtered = []
    for doc in documents:
        name = _document_display_name(doc)
        source = doc.get("source", "")
        enabled = doc.get("enabled", True)
        if status_filter == "仅启用" and not enabled:
            continue
        if status_filter == "仅禁用" and enabled:
            continue
        if normalized_query and normalized_query not in name.casefold() and normalized_query not in source.casefold():
            continue
        filtered.append(doc)

    reverse = sort_mode in {"上传时间最新", "文件大小大到小", "分块数多到少"}
    return sorted(filtered, key=lambda item: _document_sort_value(item, sort_mode), reverse=reverse)


def render_document_management(collection_name: str):
    """渲染当前知识库的文档管理面板（支持多选删除、启用/禁用）。"""
    render_section_intro(
        "description",
        "资料库 / My Stuff",
        "聚合当前知识空间的文件、启用状态和检索可用性；上传后即可在问答页查看引用证据。",
    )
    pending_notice = st.session_state.pop("document_status_notice", None)
    if pending_notice:
        render_status_notice(
            pending_notice.get("kind", "info"),
            pending_notice.get("message", ""),
            pending_notice.get("title"),
        )
    if not collection_name:
        render_status_notice("info", "请先在左侧选择或创建一个知识库。", "请先选择知识库")
        return

    result = list_documents_api(collection_name)
    if not result.get("success"):
        render_status_notice(
            "error",
            f"{result.get('message', '获取文档列表失败')}{format_last_response_diagnostic_suffix()}",
            "获取文档列表失败",
        )
        return

    documents = result.get("documents", [])
    if not documents:
        render_empty_state(
            "description",
            "当前知识库暂无文档",
            "请先到「文档上传」添加 PDF、TXT、DOCX 或 Markdown，处理完成后再回到这里管理。",
            [
                ("upload", "上传资料", "支持 PDF、TXT、DOCX 和 Markdown。"),
                ("activity", "等待处理", "完成后会写入当前知识库。"),
                ("message", "开始问答", "到问答页基于资料继续提问。"),
            ],
        )
        return

    # --- 数据准备 ---
    all_sources = {doc.get("source", "") for doc in documents}
    selected = st.session_state.selected_documents & all_sources
    st.session_state.selected_documents = selected
    n_sel = len(selected)
    n_total = len(documents)
    n_enabled = sum(1 for doc in documents if doc.get("enabled", True))
    n_disabled = n_total - n_enabled

    with st.container(key="doc_filters"):
        filter_col, status_col, sort_col = st.columns([2.2, 1.1, 1.45], gap="small")
        with filter_col:
            doc_query = st.text_input(
                "搜索文档",
                key="doc_search_query",
                placeholder="按文件名或来源路径搜索",
                label_visibility="collapsed",
            )
        with status_col:
            status_filter = st.selectbox(
                "文档状态",
                ["全部文档", "仅启用", "仅禁用"],
                key="doc_status_filter",
                label_visibility="collapsed",
            )
        with sort_col:
            sort_mode = st.selectbox(
                "排序方式",
                ["上传时间最新", "上传时间最早", "文件名 A-Z", "文件大小大到小", "分块数多到少"],
                key="doc_sort_mode",
                label_visibility="collapsed",
            )

    visible_documents = _filter_and_sort_documents(documents, doc_query, status_filter, sort_mode)
    visible_sources = {doc.get("source", "") for doc in visible_documents}
    visible_selected = selected & visible_sources
    all_selected = bool(visible_sources) and visible_sources.issubset(selected)
    sel_has_disabled = any(
        not doc.get("enabled", True) for doc in documents if doc.get("source", "") in selected
    )
    sel_has_enabled = any(
        doc.get("enabled", True) for doc in documents if doc.get("source", "") in selected
    )

    if st.session_state.batch_delete_confirm and selected:
        render_batch_delete_dialog(collection_name, documents, list(selected))

    selection_state = "has-selection" if n_sel else "empty-selection"

    # --- 工具栏 ---
    st.html(
        f"""
        <div class="doc-toolbar {selection_state}">
            <div class="doc-toolbar-left">
                <span class="doc-status-pill active">{icon_svg("check_circle")} 启用 {n_enabled}</span>
                <span class="doc-status-pill disabled">{icon_svg("block")} 禁用 {n_disabled}</span>
                <span class="doc-status-note">{icon_svg("file")} 当前显示 {len(visible_documents)} / {n_total}</span>
            </div>
            <div class="doc-toolbar-info">
                <span class="doc-toolbar-count">{n_sel}</span>
                <span class="doc-toolbar-label">已选择文档</span>
            </div>
        </div>
        """
    )
    st.html(
        f"""
        <div class="doc-toolbar-hint">
            {icon_svg("info")}
            <span>禁用文档不会参与当前知识库问答检索。当前显示 {len(visible_documents)} 个文档。</span>
        </div>
        """
    )

    with st.container(key="doc_batch_actions"):
        btn1, btn2, btn3, btn4, _ = st.columns([1.18, 1.28, 1.28, 1.28, 8.4], gap="small")
        with btn1:
            sel_text = "取消全选" if all_selected else "全选"
            sel_icon = ":material/deselect:" if all_selected else ":material/select_all:"
            if st.button(
                sel_text,
                icon=sel_icon,
                key="toolbar_select_all",
                help="取消选择当前筛选结果中的全部文档" if all_selected else "选择当前筛选结果中的全部文档",
                use_container_width=True,
            ):
                if all_selected:
                    st.session_state.selected_documents = selected - visible_sources
                    for source in visible_sources:
                        st.session_state[f"doc_sel_{_doc_hash(source)}"] = False
                else:
                    _set_selected_documents(selected | visible_sources)
                st.rerun()
        with btn2:
            if st.button(
                f"删除 ({n_sel})",
                icon=":material/delete_forever:",
                key="toolbar_delete",
                disabled=n_sel == 0,
                help="请先选择至少一个文档" if n_sel == 0 else f"删除已选择的 {n_sel} 个文档",
                use_container_width=True,
            ):
                st.session_state.batch_delete_confirm = True
                st.rerun()
        with btn3:
            if st.button(
                f"禁用 ({n_sel})",
                icon=":material/block:",
                key="toolbar_disable",
                disabled=n_sel == 0 or not sel_has_enabled,
                help=(
                    "请先选择至少一个文档"
                    if n_sel == 0
                    else "已选择的文档均处于禁用状态"
                    if not sel_has_enabled
                    else f"禁用已选择的 {n_sel} 个文档，使其不再参与问答检索"
                ),
                use_container_width=True,
            ):
                ok, fail = _toggle_selected_documents(collection_name, selected, False)
                _clear_selected_documents(all_sources)
                if fail:
                    st.session_state.document_status_notice = {
                        "kind": "warning",
                        "message": f"已禁用 {ok} 个文档，失败 {fail} 个{format_last_response_diagnostic_suffix()}",
                    }
                else:
                    st.session_state.document_status_notice = {
                        "kind": "success",
                        "message": f"已禁用 {ok} 个文档，禁用文档不会参与当前知识库问答检索",
                    }
                st.rerun()
        with btn4:
            if st.button(
                f"启用 ({n_sel})",
                icon=":material/check_circle:",
                key="toolbar_enable",
                disabled=n_sel == 0 or not sel_has_disabled,
                help=(
                    "请先选择至少一个文档"
                    if n_sel == 0
                    else "已选择的文档均处于启用状态"
                    if not sel_has_disabled
                    else f"启用已选择的 {n_sel} 个文档，使其重新参与问答检索"
                ),
                use_container_width=True,
            ):
                ok, fail = _toggle_selected_documents(collection_name, selected, True)
                _clear_selected_documents(all_sources)
                if fail:
                    st.session_state.document_status_notice = {
                        "kind": "warning",
                        "message": f"已启用 {ok} 个文档，失败 {fail} 个{format_last_response_diagnostic_suffix()}",
                    }
                else:
                    st.session_state.document_status_notice = {
                        "kind": "success",
                        "message": f"已启用 {ok} 个文档",
                    }
                st.rerun()

    st.divider()

    # --- 文档列表 ---
    if not visible_documents:
        render_empty_state(
            "search",
            "没有匹配当前条件的文档",
            "当前搜索、状态筛选或排序组合没有返回结果，可以调整条件后继续查看。",
            [
                ("search", "放宽关键词", "尝试使用文件名中的短词。"),
                ("layers", "切换状态", "查看全部、启用或禁用文档。"),
                ("refresh", "重置排序", "按最新上传重新浏览。"),
            ],
        )
        return

    for doc in visible_documents:
        source = doc.get("source", "")
        name = _document_display_name(doc)
        safe_name = html.escape(name)
        is_enabled = doc.get("enabled", True)
        is_sel = source in st.session_state.selected_documents
        h = _doc_hash(source)

        chk_class = " doc-chk-checked" if is_sel else ""
        chk_inner = (
            '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" '
            'stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="3.5 8 6.5 11 12.5 4.5"/></svg>'
            if is_sel
            else ""
        )
        enabled_class = "" if is_enabled else " document-card-disabled"
        disabled_badge = (
            f'<span class="document-disabled-badge">{icon_svg("block")} 已禁用，不参与检索</span>'
            if not is_enabled
            else ""
        )
        enabled_badge = (
            f'<span class="document-enabled-badge">{icon_svg("check_circle")} 已启用</span>'
            if is_enabled
            else ""
        )

        check_col, card_col = st.columns([0.42, 20], gap="small")
        with check_col:
            checkbox_key = f"doc_sel_{h}"
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = is_sel
            checked = st.checkbox(
                "选择" + name,
                key=checkbox_key,
                label_visibility="collapsed",
            )
            if checked != is_sel:
                if checked:
                    st.session_state.selected_documents.add(source)
                else:
                    st.session_state.selected_documents.discard(source)
                st.rerun()
        with card_col:
            st.html(
                f"""
                <div class="document-card{enabled_class}">
                    <div class="document-card-header">
                        <span class="document-card-icon">{icon_svg("description")}</span>
                        <div class="document-card-main">
                            <div class="document-card-title-row">
                                <div class="document-card-name" title="{safe_name}">{safe_name}</div>
                                {enabled_badge}
                            </div>
                            {disabled_badge}
                            <div class="document-card-meta">
                                大小：{html.escape(format_file_size(doc.get('size')))} ·
                                上传时间：{html.escape(str(doc.get('upload_time') or '未知'))} ·
                                分块：{html.escape(str(doc.get('chunk_count', 0)))}
                            </div>
                        </div>
                    </div>
                </div>
                """
            )


def render_settings_panel():
    """渲染系统设置面板。"""
    render_section_intro(
        "settings",
        "系统设置",
        "这些设置会影响后续问答或新上传文档；分块参数不会追溯修改已入库内容。",
    )
    render_settings_summary()
    retrieval_col, generation_col = st.columns(2, gap="large")
    with retrieval_col:
        st.html(
            f"""
            <div class="settings-group-card retrieval">
                {icon_svg("database")}
                <div>
                    <div class="settings-group-title">检索与分块</div>
                    <div class="settings-group-copy">控制召回数量、文档切块和检索前增强。</div>
                </div>
            </div>
            """
        )
        st.session_state.settings_top_k = st.slider(
            "检索返回片段数",
            min_value=1,
            max_value=10,
            value=int(st.session_state.settings_top_k),
            step=1,
            help="影响新问题检索和生成时使用的片段数量",
        )
        st.session_state.settings_chunk_size = st.number_input(
            "分块大小",
            min_value=200,
            max_value=2000,
            value=int(st.session_state.settings_chunk_size),
            step=50,
            help="只影响之后上传的新文档",
        )
        max_overlap = max(0, int(st.session_state.settings_chunk_size) - 1)
        current_overlap = min(int(st.session_state.settings_chunk_overlap), max_overlap)
        st.session_state.settings_chunk_overlap = st.number_input(
            "分块重叠度",
            min_value=0,
            max_value=max_overlap,
            value=current_overlap,
            step=25,
            help="相邻分块共享的字符数，只影响之后上传的新文档",
        )
        st.session_state.settings_query_rewrite = st.toggle(
            "启用查询重写",
            value=bool(st.session_state.settings_query_rewrite),
            help="发送问题前，先由大模型改写成更适合检索的查询语句",
        )
        st.session_state.settings_contextual_compression = st.toggle(
            "启用上下文压缩",
            value=bool(st.session_state.settings_contextual_compression),
            help="使用 reranker 筛选更相关的内容片段",
        )
    with generation_col:
        st.html(
            f"""
            <div class="settings-group-card generation">
                {icon_svg("sparkles")}
                <div>
                    <div class="settings-group-title">生成与增强</div>
                    <div class="settings-group-copy">调整回答发散度、过程展示和图片解析能力。</div>
                </div>
            </div>
            """
        )
        st.session_state.settings_temperature = st.slider(
            "模型 temperature",
            min_value=0.0,
            max_value=1.5,
            value=float(st.session_state.settings_temperature),
            step=0.05,
            help="值越低越稳定，值越高越发散",
        )
        st.session_state.settings_show_thinking = st.toggle(
            "显示思考过程",
            value=bool(st.session_state.settings_show_thinking),
            help="关闭后仍会执行检索和生成，只是不显示等待过程气泡",
        )
        st.session_state.settings_multimodal_parsing = st.toggle(
            "上传时解析文档图片",
            value=bool(st.session_state.settings_multimodal_parsing),
            help="PDF/Word 中的图片会调用多模态模型生成说明并写入知识库",
        )
    st.divider()
    st.html(
        f"""
        <div class="settings-group-card agent">
            {icon_svg("bot")}
            <div>
                <div class="settings-group-title">Agent 模式</div>
                <div class="settings-group-copy">开启后优先查本地资料，必要时补充 Web 搜索或代码工具；调试面板会显示证据摘要、Web 降级和策略提醒。</div>
            </div>
        </div>
        """
    )
    st.session_state.settings_agent_mode = st.toggle(
        "启用 Agent 模式",
        value=bool(st.session_state.settings_agent_mode),
        help="Agent 会优先使用本地知识库，必要时调用网页搜索或代码工具补充证据",
    )
    st.session_state.settings_agent_debug = st.toggle(
        "开启 Agent 调试模式",
        value=bool(st.session_state.settings_agent_debug),
        help="展示证据摘要、工具选择、搜索服务、重试降级和策略提醒，适合面试演示排障链路",
    )
    st.caption("设置会立即生效；公开演示不会提交本地 Chroma、session、日志或密钥，分块参数只影响之后上传的新文档。")
