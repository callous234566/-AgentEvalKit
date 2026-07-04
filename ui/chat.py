"""Chat section: main Q&A interface, empty state, thinking process, regenerate."""

import html
import re
import time

import streamlit as st

import config
from rag.session_state import (
    init_session_state,
    create_new_session,
    get_session_name,
    switch_session,
    delete_current_session,
    save_current_session,
    persist_sessions,
)
from ui.api_wrappers import (
    retrieve_documents_api,
    generate_answer_api,
    agent_query_api,
    format_last_response_diagnostic_suffix,
)
from ui.assets import icon_svg
from ui.components import (
    render_empty_state,
    render_user_message_html,
    render_ai_message_html,
    render_answer_status_bar,
    render_source_evidence_html,
)
from ui.export import build_conversation_markdown, build_conversation_pdf
from ui.js_injection import inject_chat_enhancement_script, render_force_chat_bottom, render_one_time_latest_scroll
from ui.text_utils import _normalize_message_text

# Injected by streamlit_app.py at startup
SESSION_STORE_PATH = None


def init_chat(store_path):
    global SESSION_STORE_PATH
    SESSION_STORE_PATH = store_path


def _clear_input_js(disabled: bool = False, focus: bool = False):
    """注入 JS 清空输入框（合并 4 处重复代码）。"""
    disable_attr = "input.disabled = true;" if disabled else "input.disabled = false;"
    focus_attr = "input.focus();" if focus else ""
    st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const input = document.querySelector('div[data-testid="stTextArea"] textarea');
            if (input) {{
                input.value = '';
                {disable_attr}
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                {focus_attr}
            }}
        }});
    </script>
    """, unsafe_allow_html=True)


def render_chat_empty_state(collection_name: str) -> None:
    """Render first-run guidance for the chat workspace."""
    render_empty_state(
        "bot",
        "3 步开始一次可追溯问答",
        f"当前知识库：{collection_name or '未选择'}。先确认知识库，再提问，最后查看回答下方的引用、分数和检索线索。",
        [
            ("database", "选择知识库", "在左侧切到有文档的知识库。"),
            ("upload", "上传示例文档", "首次公开演示时先上传一份脱敏资料。"),
            ("library", "提问看引用", "回答下方会展示来源、分数和片段证据。"),
        ],
    )
    suggestions = [
        "BM25 在 RAG 检索中有什么作用？",
        "这些资料是否说明了火星基地厨房的虚构配置项？",
        "总结当前知识库的核心内容，并列出引用来源",
    ]
    with st.expander("试试这些问题", expanded=True):
        for idx, prompt in enumerate(suggestions):
            if st.button(
                prompt,
                key=f"sample_question_{idx}",
                use_container_width=True,
                disabled=st.session_state.is_generating,
            ):
                st.session_state.queued_question = prompt
                st.rerun()


def regenerate_answer_at(message_index: int):
    """删除目标 AI 回答并重新生成其前一条用户问题。"""
    if st.session_state.is_generating:
        return

    messages = st.session_state.chat_history
    if not (0 <= message_index < len(messages)):
        return
    if messages[message_index].get("role") != "assistant":
        return

    previous_user_index = None
    for idx in range(message_index - 1, -1, -1):
        if messages[idx].get("role") == "user":
            previous_user_index = idx
            break

    if previous_user_index is None:
        return

    st.session_state.chat_history = messages[:message_index]
    st.session_state.is_generating = True
    st.session_state.user_input = ""
    st.session_state.input_counter += 1
    st.session_state.scroll_to_bottom = False
    save_current_session(SESSION_STORE_PATH)
    st.rerun()


def render_thinking_process(placeholder, steps: list):
    """用普通 AI 气泡临时渲染真实执行步骤。"""
    with placeholder.container():
        step_html = []
        for step in steps:
            status = step.get("status", "")
            text = html.escape(step.get("text", ""))
            step_html.append(
                f"<div class='process-step {status}'>"
                f"<span class='process-dot'></span><span>{text}</span></div>"
            )

        st.html(
            f"""
            <div class="message-row">
                <div class="avatar ai-avatar">{icon_svg("bot")}</div>
                <div class="ai-message">
                    {''.join(step_html)}
                </div>
            </div>
            """,
        )


def _render_export_controls():
    """渲染对话导出控件（Markdown/PDF 下载）。"""
    if not st.session_state.chat_history:
        return
    export_name = get_session_name(st.session_state.current_session_id)
    export_md = build_conversation_markdown(export_name, st.session_state.chat_history)
    safe_export_name = re.sub(r"[\\/:*?\"<>|]+", "_", export_name)[:40] or "conversation"
    st.html(
        f"""
        <div class="chat-export-bar">
            <div><strong>会话导出</strong>：将当前对话保存为 Markdown 或 PDF，便于复盘、分享和归档。</div>
            <div class="chat-export-meta">{len(st.session_state.chat_history)} 条消息</div>
        </div>
        """
    )
    export_col1, export_col2, _ = st.columns([1.6, 1.6, 5.6])
    with export_col1:
        st.download_button(
            "导出 Markdown",
            data=export_md.encode("utf-8"),
            file_name=f"{safe_export_name}.md",
            mime="text/markdown",
            icon=":material/download:",
            use_container_width=True,
            key="chat_export_markdown",
        )
    with export_col2:
        st.download_button(
            "导出 PDF",
            data=build_conversation_pdf(export_md),
            file_name=f"{safe_export_name}.pdf",
            mime="application/pdf",
            icon=":material/picture_as_pdf:",
            use_container_width=True,
            key="chat_export_pdf",
        )


def _render_chat_history(chat_container, collection_name: str):
    """渲染聊天历史消息列表。"""
    with chat_container:
        if not st.session_state.chat_history and not st.session_state.is_generating:
            render_chat_empty_state(collection_name)

        for idx, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.html(render_user_message_html(
                    message["content"],
                    anchor_id=message.get("scroll_anchor"),
                ))
            else:
                raw_sources = message.get("sources") or []
                filtered_sources = [
                    s for s in raw_sources
                    if s.get("score", 0) > 0.7
                ]
                status_html = render_answer_status_bar(
                    filtered_sources,
                    message.get("agent_steps", []),
                    message.get("debug_info", {}),
                    message.get("content", ""),
                )
                st.html(render_ai_message_html(
                    message["content"],
                    message_index=idx,
                    anchor_id=message.get("scroll_anchor"),
                    status_html=status_html,
                ))
                if st.button(
                    "",
                    key=f"regen_trigger_{idx}",
                    help="重新生成回答",
                    icon=":material/refresh:",
                    disabled=st.session_state.is_generating,
                ):
                    regenerate_answer_at(idx)

                if filtered_sources:
                    st.html(render_source_evidence_html(filtered_sources))
                if message.get("agent_steps") and st.session_state.get("settings_agent_debug", config.AGENT_DEBUG):
                    render_agent_debug_panel(message.get("agent_steps", []), message.get("debug_info", {}))
        st.html('<div id="rag-chat-bottom" class="chat-scroll-sentinel" aria-hidden="true"></div>')


def _get_first_user_message() -> str:
    """Return the first user message as the conversation title seed."""
    for message in st.session_state.get("chat_history", []):
        if message.get("role") == "user" and message.get("content"):
            return _normalize_message_text(message.get("content", ""))
    return ""


def _render_chat_topbar(collection_name: str) -> None:
    """Render a Doubao-like conversation header."""
    first_question = _get_first_user_message()
    session_name = get_session_name(st.session_state.get("current_session_id", ""))
    title = first_question or session_name or "新的知识库对话"
    if len(title) > 34:
        title = title[:34].rstrip() + "..."
    message_count = len(st.session_state.get("chat_history", []))
    st.html(
        f"""
        <div class="chat-topbar">
            <div class="chat-topbar-title" title="{html.escape(first_question or session_name or '新的知识库对话')}">
                {html.escape(title)}
            </div>
            <div class="chat-topbar-subtitle">
                内容由 AI 生成，请仔细甄别 · 当前知识库：{html.escape(collection_name or '未选择')} · {message_count} 条消息
            </div>
        </div>
        """
    )


def _render_input_form() -> tuple:
    """Render the fixed chat input panel."""
    input_key = f"chat_input_{st.session_state.input_counter}"
    user_input = ""
    submitted = False
    clear_clicked = False
    stop_clicked = False

    shortcut_prompts = [
        ("BM25 作用", "BM25 在 RAG 检索中有什么作用？"),
        ("拒答演示", "这些资料是否说明了火星基地厨房的虚构配置项？"),
        ("引用总结", "请总结当前知识库的核心内容，并列出最关键的引用来源。"),
        ("查找矛盾", "请找出当前知识库中可能存在的矛盾、重复或需要核实的内容。"),
    ]

    with st.container(border=False, key="chat_input_area"):
        with st.form("chat_form", clear_on_submit=False):
            input_col, send_col, clear_col = st.columns(
                [15.8, 1.35, 1.35],
                gap="small",
                vertical_alignment="bottom",
            )

            with input_col:
                user_input = st.text_area(
                    "请输入您的问题...",
                    key=input_key,
                    label_visibility="collapsed",
                    disabled=st.session_state.is_generating,
                    placeholder="请输入您的问题..." if not st.session_state.is_generating else "AI 正在回答中...",
                    height=52,
                )

            with send_col:
                if st.session_state.is_generating:
                    stop_clicked = st.form_submit_button(
                        "停止",
                        key="stop_generation_button",
                        help="停止当前回答",
                        use_container_width=True,
                    )
                else:
                    submitted = st.form_submit_button(
                        "发送",
                        key="send_button",
                        icon=":material/send:",
                        help="发送消息",
                        use_container_width=True,
                        type="primary",
                    )

            with clear_col:
                clear_clicked = st.form_submit_button(
                    "重置",
                    key="clear_button",
                    help="删除当前会话",
                    icon=":material/delete:",
                    use_container_width=True,
                    disabled=st.session_state.is_generating,
                )

        with st.container(key="chat_prompt_tools"):
            with st.expander("快捷提问", expanded=False):
                for idx, (label, prompt) in enumerate(shortcut_prompts):
                    if st.button(
                        label,
                        key=f"quick_prompt_{idx}",
                        use_container_width=True,
                        disabled=st.session_state.is_generating,
                    ):
                        st.session_state.queued_question = prompt
                        st.rerun()
                st.html('<span class="chat-input-hint"><kbd>Ctrl</kbd><kbd>Enter</kbd> 快速发送</span>')

    return user_input, submitted, clear_clicked, stop_clicked


@st.dialog("确认清空会话")
def render_clear_session_dialog() -> None:
    """Render destructive current-session clear confirmation as a modal dialog."""
    message_count = len(st.session_state.get("chat_history", []))
    st.html(
        f"""
        <div class="doc-confirm-panel">
            <div class="doc-confirm-icon">{icon_svg("trash")}</div>
            <div>
                <div class="doc-confirm-title">确定清空当前会话吗？</div>
                <div class="doc-confirm-copy">当前会话共有 {message_count} 条消息，清空后会创建一个新的空会话。</div>
                <div class="doc-confirm-hint">此操作不会删除知识库文档，但当前对话内容不可恢复。</div>
            </div>
        </div>
        """
    )
    confirm_col, cancel_col = st.columns(2)
    with confirm_col:
        if st.button("确认清空", icon=":material/delete_forever:", type="primary", use_container_width=True, key="confirm_clear"):
            delete_current_session(SESSION_STORE_PATH)
            st.session_state.show_clear_confirm = False
            st.session_state.user_input = ""
            st.session_state.input_counter += 1
            st.rerun()
    with cancel_col:
        if st.button("取消", icon=":material/close:", use_container_width=True, key="cancel_clear"):
            st.session_state.show_clear_confirm = False
            st.rerun()


def _handle_clear_confirm(clear_clicked: bool):
    """处理删除会话确认对话框。"""
    if clear_clicked and not st.session_state.is_generating:
        st.session_state.show_clear_confirm = True
        st.session_state.input_counter += 1
        st.rerun()

    if st.session_state.show_clear_confirm:
        render_clear_session_dialog()


def _handle_stop_generation(stop_clicked: bool) -> None:
    """Stop the active UI generation flow and restore the composer."""
    if not (stop_clicked and st.session_state.is_generating):
        return

    if st.session_state.chat_history and st.session_state.chat_history[-1].get("role") == "user":
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "已停止生成。您可以调整问题后重新发送。",
            "sources": [],
            "scroll_anchor": f"rag-message-{st.session_state.scroll_request_id}-answer",
        })
        save_current_session(SESSION_STORE_PATH)

    st.session_state.is_generating = False
    st.session_state.user_input = ""
    st.session_state.input_counter += 1
    st.session_state.scroll_to_bottom = False
    st.session_state.answer_scroll_pending = False
    _clear_input_js(focus=True)
    st.toast("已停止当前回答")
    st.rerun()


def _handle_submit(user_input, submitted):
    """处理用户提交问题。"""
    queued_question = (st.session_state.pop("queued_question", "") or "").strip()
    question = queued_question or (user_input or "").strip()
    if not ((submitted or queued_question) and question and not st.session_state.is_generating):
        return None

    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history[-1]["scroll_anchor"] = (
        f"rag-message-{st.session_state.scroll_request_id + 1}-question"
    )
    if not st.session_state.input_history or st.session_state.input_history[-1] != question:
        st.session_state.input_history.append(question)
        st.session_state.input_history = st.session_state.input_history[-20:]
        persist_sessions(SESSION_STORE_PATH)

    save_current_session(SESSION_STORE_PATH)
    st.session_state.user_input = ""
    st.session_state.is_generating = True
    st.session_state.input_counter += 1
    st.session_state.scroll_request_id += 1
    st.session_state.scroll_to_bottom = True
    st.session_state.answer_scroll_pending = True
    _clear_input_js()
    return question


# 工具名称中文映射
_TOOL_NAMES = {
    "search_knowledge_base": "知识库检索",
    "search_web": "网页搜索",
    "execute_python_code": "代码执行",
}


def _build_agent_debug_steps(agent_steps: list, debug_info: dict | None = None) -> list:
    """Build compact Agent debug steps for the UI."""
    steps = []
    debug_info = debug_info or {}
    evidence_summary = debug_info.get("evidence_summary") or {}
    if evidence_summary:
        evidence_mode = {
            "local_plus_web": "本地资料 + 外部补充",
            "local_only": "本地资料",
            "web_only": "外部搜索",
            "code_only": "代码验证",
            "no_tool": "未调用工具",
        }.get(evidence_summary.get("mode", ""), evidence_summary.get("mode", "未知"))
        summary_parts = [f"证据摘要: {evidence_mode}"]
        if evidence_summary.get("local_fallback_used"):
            summary_parts.append("本地兜底")
        if evidence_summary.get("web_used"):
            provider = evidence_summary.get("web_provider") or "网页搜索"
            attempts = evidence_summary.get("web_attempt_count", 0)
            results = evidence_summary.get("web_result_count", 0)
            web_text = f"Web: {provider}，{attempts} 次尝试，{results} 条结果"
            if evidence_summary.get("web_fallback_used"):
                web_text += "，Web 已降级"
            summary_parts.append(web_text)
        violations = evidence_summary.get("policy_violations") or []
        if violations:
            summary_parts.append(f"策略提醒: {', '.join(violations)}")
        steps.append({"text": "，".join(summary_parts), "status": "done"})
    tool_policy = debug_info.get("tool_policy") or {}
    if tool_policy:
        first_tool = _TOOL_NAMES.get(
            tool_policy.get("recommended_first_tool", ""),
            tool_policy.get("recommended_first_tool", ""),
        )
        category = tool_policy.get("category", "未分类")
        steps.append({
            "text": f"工具策略: {category}，推荐首选 {first_tool}",
            "status": "done",
        })
    source_layers = debug_info.get("source_layers") or {}
    if source_layers:
        layer_label = {
            "local_plus_web": "本地资料 + 外部补充",
            "local_only": "本地资料",
            "web_only": "外部搜索",
            "code_only": "代码验证",
            "no_tool": "未调用工具",
        }.get(source_layers.get("mode", ""), source_layers.get("mode", "未知"))
        priority = "，本地优先" if source_layers.get("local_priority") else ""
        steps.append({
            "text": f"来源层级: {layer_label}{priority}",
            "status": "done",
        })
    for step in agent_steps or []:
        tool_name = _TOOL_NAMES.get(step.get("tool", ""), step.get("tool", ""))
        tool_input = step.get("input", "")
        output = (step.get("output", "") or "").replace("\n", " ")
        text = f"调用 {tool_name}: {tool_input[:60]}"
        if output:
            text += f" | 返回: {output[:90]}"
        steps.append({"text": text, "status": "done"})

    search_trace = debug_info.get("search_trace") or {}
    attempts = search_trace.get("attempts") or []
    if attempts:
        provider = search_trace.get("provider") or "网页搜索"
        result_count = search_trace.get("result_count", 0)
        fallback = "，已降级" if search_trace.get("fallback_used") else ""
        steps.append({
            "text": f"搜索服务: {provider}，结果 {result_count} 条，尝试 {len(attempts)} 次{fallback}",
            "status": "done",
        })
    tool_budget = debug_info.get("tool_budget") or {}
    counts = tool_budget.get("counts") or {}
    limits = tool_budget.get("limits") or {}
    if counts:
        budget_text = (
            f"工具预算: 总 {counts.get('total', 0)}/{limits.get('max_tool_calls', '-')}"
            f"，Web {counts.get('search_web', 0)}/{limits.get('max_web_searches', '-')}"
            f"，代码 {counts.get('execute_python_code', 0)}/{limits.get('max_code_executions', '-')}"
        )
        violations = tool_budget.get("violations") or []
        if violations:
            budget_text += f"，策略提醒: {', '.join(violations)}"
        steps.append({"text": budget_text, "status": "done"})
    if debug_info.get("elapsed_ms"):
        steps.append({"text": f"Agent 耗时: {debug_info.get('elapsed_ms')} ms", "status": "done"})
    return steps


def render_agent_debug_panel(agent_steps: list, debug_info: dict | None = None):
    """Render persisted Agent debug details under an answer."""
    steps = _build_agent_debug_steps(agent_steps, debug_info)
    if not steps:
        return
    step_html = []
    for step in steps:
        status = html.escape(step.get("status", "done"))
        text = html.escape(step.get("text", ""))
        step_html.append(
            f"<div class='process-step {status}'>"
            f"<span class='process-dot'></span><span>{text}</span></div>"
        )
    st.html(
        "<div class='ai-message agent-debug-panel'>"
        "<div class='agent-debug-title'>执行轨迹</div>"
        f"{''.join(step_html)}"
        "</div>"
    )


def _run_agent_pipeline(chat_container, collection_name: str):
    """执行 Agent 模式流水线：自主选择工具 → 多步推理 → 生成回答。"""
    if not (st.session_state.is_generating and st.session_state.chat_history):
        return

    _clear_input_js(disabled=True)

    last_user_message = None
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break

    if not last_user_message:
        return

    recent_history = [
        {"role": msg.get("role"), "content": msg.get("content", "")}
        for msg in st.session_state.chat_history[:-1][-config.CHAT_HISTORY_TURNS * 2:]
        if msg.get("role") in ("user", "assistant") and msg.get("content")
    ]

    # 显示 Agent 启动步骤
    show_thinking = bool(st.session_state.get("settings_show_thinking", True))
    process_placeholder = chat_container.empty() if show_thinking else None
    process_steps = [{"text": "Agent 已接收问题，正在分析...", "status": "active"}]
    if show_thinking:
        render_thinking_process(process_placeholder, process_steps)

    # 调用 Agent 后端
    result = agent_query_api(last_user_message, collection_name, recent_history)

    if process_placeholder is not None:
        process_placeholder.empty()

    agent_steps = result.get("agent_steps", [])
    debug_info = result.get("debug_info", {})

    if result.get("success"):
        answer = _normalize_message_text(result.get("answer", ""))

        # 流式显示最终答案
        if answer:
            stream_container = chat_container.empty()
            displayed_text = ""
            for i in range(0, len(answer), 18):
                displayed_text += answer[i:i + 18]
                with stream_container:
                    st.html(render_ai_message_html(displayed_text, show_actions=False, typing=True))
                time.sleep(0.015)
            with stream_container:
                st.html(render_ai_message_html(
                    displayed_text,
                    show_actions=False,
                    status_html=render_answer_status_bar([], agent_steps, debug_info, answer),
                ))
                render_force_chat_bottom()

        # 显示 Agent 工具调用追踪
        if agent_steps and show_thinking:
            trace_steps = _build_agent_debug_steps(agent_steps, debug_info)
            if trace_steps:
                trace_container = chat_container.empty()
                render_thinking_process(trace_container, trace_steps)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": _normalize_message_text(answer) if answer else "Agent 未能生成回答。",
            "sources": [],
            "agent_steps": agent_steps,
            "debug_info": debug_info,
            "scroll_anchor": f"rag-message-{st.session_state.scroll_request_id}-answer",
        })
    else:
        error_msg = result.get("error", "未知错误")
        diagnostic_suffix = format_last_response_diagnostic_suffix()
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"抱歉，Agent 执行出错：{error_msg}{diagnostic_suffix}",
            "sources": [],
            "agent_steps": agent_steps,
            "debug_info": debug_info,
            "scroll_anchor": f"rag-message-{st.session_state.scroll_request_id}-answer",
        })

    save_current_session(SESSION_STORE_PATH)
    st.session_state.is_generating = False
    st.session_state.user_input = ""
    st.session_state.input_counter += 1
    st.session_state.scroll_to_bottom = False
    _clear_input_js(focus=True)
    st.rerun()


def _run_generation_pipeline(chat_container, collection_name: str):
    """执行 AI 生成流水线：检索 → 重排 → 生成 → 流式显示。"""
    if not (st.session_state.is_generating and st.session_state.chat_history):
        return

    _clear_input_js(disabled=True)

    last_user_message = None
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break

    if not last_user_message:
        return

    recent_history = [
        {"role": msg.get("role"), "content": msg.get("content", "")}
        for msg in st.session_state.chat_history[:-1][-config.CHAT_HISTORY_TURNS * 2:]
        if msg.get("role") in ("user", "assistant") and msg.get("content")
    ]

    show_thinking = bool(st.session_state.get("settings_show_thinking", True))
    process_placeholder = chat_container.empty() if show_thinking else None
    process_steps = [{"text": "已接收您的问题", "status": "done"}]
    if show_thinking:
        render_thinking_process(process_placeholder, process_steps)
        time.sleep(0.05)

    process_steps.append({"text": "正在检索知识库...", "status": "active"})
    if show_thinking:
        render_thinking_process(process_placeholder, process_steps)

    retrieval_result = retrieve_documents_api(last_user_message, collection_name, recent_history)

    if retrieval_result.get("success"):
        retrieved_count = retrieval_result.get("retrieved_count", 0)
        selected_count = retrieval_result.get("selected_count", 0)
        process_steps[-1] = {"text": f"已检索到 {retrieved_count} 个相关片段", "status": "done"}
        process_steps.append({"text": "正在智能重排序...", "status": "active"})
        if show_thinking:
            render_thinking_process(process_placeholder, process_steps)
            time.sleep(0.05)

        process_steps[-1] = {"text": f"已筛选出最相关的 {selected_count} 个片段", "status": "done"}
        process_steps.append({"text": "正在准备生成...", "status": "active"})
        if show_thinking:
            render_thinking_process(process_placeholder, process_steps)

        result = generate_answer_api(
            last_user_message, collection_name,
            retrieval_result.get("documents", []), recent_history,
        )
    else:
        result = {"success": False, "error": retrieval_result.get("error", "检索失败"), "answer": "", "sources": []}

    if process_placeholder is not None:
        process_placeholder.empty()

    if result.get("success"):
        answer = _normalize_message_text(result.get("answer", ""))
        sources = result.get("sources", [])
        if answer:
            stream_container = chat_container.empty()
            displayed_text = ""
            for i in range(0, len(answer), 18):
                displayed_text += answer[i:i + 18]
                with stream_container:
                    st.html(render_ai_message_html(displayed_text, show_actions=False, typing=True))
                time.sleep(0.015)
            with stream_container:
                filtered_sources = [
                    s for s in sources
                    if s.get("score", 0) > 0.7
                ]
                st.html(render_ai_message_html(
                    displayed_text,
                    show_actions=False,
                    status_html=render_answer_status_bar(filtered_sources, answer=answer),
                ))
                render_force_chat_bottom()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": _normalize_message_text(answer),
                "sources": sources,
                "scroll_anchor": f"rag-message-{st.session_state.scroll_request_id}-answer",
            })
    else:
        error_msg = result.get("error", "未知错误")
        diagnostic_suffix = format_last_response_diagnostic_suffix()
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"抱歉，回答问题时出现错误：{error_msg}{diagnostic_suffix}",
            "sources": [],
            "scroll_anchor": f"rag-message-{st.session_state.scroll_request_id}-answer",
        })

    save_current_session(SESSION_STORE_PATH)
    st.session_state.is_generating = False
    st.session_state.user_input = ""
    st.session_state.input_counter += 1
    st.session_state.scroll_to_bottom = False
    _clear_input_js(focus=True)
    st.rerun()


def render_chat_section(collection_name: str):
    """渲染问答区域 - 聊天式布局"""
    init_session_state(SESSION_STORE_PATH)

    if st.session_state.is_generating:
        _clear_input_js(disabled=True)

    if not st.session_state.current_session_id or st.session_state.current_session_id not in st.session_state.sessions:
        new_session_id = create_new_session(SESSION_STORE_PATH)
        switch_session(new_session_id, SESSION_STORE_PATH)
    _render_chat_topbar(collection_name)

    _render_export_controls()

    chat_container = st.container(border=False, key="chat_flow_area")
    _render_chat_history(chat_container, collection_name)

    user_input, submitted, clear_clicked, stop_clicked = _render_input_form()

    if st.session_state.get("scroll_to_bottom", False):
        render_one_time_latest_scroll(st.session_state.scroll_request_id, phase="question")
        st.session_state.scroll_to_bottom = False

    if st.session_state.get("answer_scroll_pending", False) and not st.session_state.is_generating:
        render_one_time_latest_scroll(st.session_state.scroll_request_id, phase="answer", respect_manual_scroll=True)
        st.session_state.answer_scroll_pending = False

    inject_chat_enhancement_script(st.session_state.input_history, st.session_state.dark_mode)

    _handle_stop_generation(stop_clicked)
    _handle_clear_confirm(clear_clicked)
    submitted_question = _handle_submit(user_input, submitted)
    if submitted_question:
        with chat_container:
            st.html(render_user_message_html(
                submitted_question,
                anchor_id=f"rag-message-{st.session_state.scroll_request_id}-question",
            ))
            st.html('<div id="rag-chat-bottom-live" class="chat-scroll-sentinel" aria-hidden="true"></div>')
        render_force_chat_bottom(respect_manual_scroll=False)

    if st.session_state.get("settings_agent_mode"):
        _run_agent_pipeline(chat_container, collection_name)
    else:
        _run_generation_pipeline(chat_container, collection_name)
