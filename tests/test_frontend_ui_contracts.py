from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "ui"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _read_ui_sources() -> str:
    paths = list(UI_ROOT.rglob("*.py")) + [ROOT / "streamlit_app.py"]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_agent_query_api_forwards_debug_and_preserves_result(monkeypatch):
    import ui.api_wrappers as api_wrappers

    calls = {}
    expected = {
        "success": True,
        "answer": "ok",
        "agent_steps": [{"tool": "search_web", "input": "q", "output": "o"}],
        "debug_info": {
            "evidence_summary": {
                "mode": "web_only",
                "web_used": True,
                "web_provider": "Tavily",
            },
        },
    }

    class FakeApiClient:
        def agent(self, question, collection_name, chat_history, debug=None):
            calls["question"] = question
            calls["collection_name"] = collection_name
            calls["chat_history"] = chat_history
            calls["debug"] = debug
            return expected

    monkeypatch.setattr(api_wrappers, "_api_client", FakeApiClient())
    monkeypatch.setitem(api_wrappers.st.session_state, "settings_agent_debug", True)

    result = api_wrappers.agent_query_api(
        "agent question",
        "default",
        [{"role": "user", "content": "hi"}],
    )

    assert result is expected
    assert calls == {
        "question": "agent question",
        "collection_name": "default",
        "chat_history": [{"role": "user", "content": "hi"}],
        "debug": True,
    }


def test_get_last_response_meta_returns_copy(monkeypatch):
    import ui.api_wrappers as api_wrappers

    class FakeApiClient:
        last_response_meta = {
            "request_id": "req-frontend",
            "status_code": 500,
            "process_time_ms": "17",
        }

    monkeypatch.setattr(api_wrappers, "_api_client", FakeApiClient())

    result = api_wrappers.get_last_response_meta()
    result["request_id"] = "mutated"

    assert result["status_code"] == 500
    assert api_wrappers._api_client.last_response_meta["request_id"] == "req-frontend"


def test_get_last_response_meta_without_client_returns_empty(monkeypatch):
    import ui.api_wrappers as api_wrappers

    monkeypatch.setattr(api_wrappers, "_api_client", None)

    assert api_wrappers.get_last_response_meta() == {}


def test_format_last_response_diagnostic_suffix_formats_request_id(monkeypatch):
    import ui.api_wrappers as api_wrappers

    monkeypatch.setattr(api_wrappers, "get_last_response_meta", lambda: {
        "request_id": "req-frontend",
        "status_code": 503,
        "process_time_ms": "88",
    })

    suffix = api_wrappers.format_last_response_diagnostic_suffix()

    assert suffix.startswith("\n\n")
    assert "排障 ID：req-frontend" in suffix
    assert "状态码：503" in suffix
    assert "耗时：88ms" in suffix


def test_format_last_response_diagnostic_suffix_supports_inline_prefix(monkeypatch):
    import ui.api_wrappers as api_wrappers

    monkeypatch.setattr(api_wrappers, "get_last_response_meta", lambda: {
        "request_id": "req-upload",
    })

    assert api_wrappers.format_last_response_diagnostic_suffix(prefix="；") == "；排障 ID：req-upload"


def test_format_last_response_diagnostic_suffix_empty_without_request_id(monkeypatch):
    import ui.api_wrappers as api_wrappers

    monkeypatch.setattr(api_wrappers, "get_last_response_meta", lambda: {"status_code": 500})

    assert api_wrappers.format_last_response_diagnostic_suffix() == ""


class FrontendUiContractsTest:
    def test_page_feedback_uses_unified_status_component(self):
        sources = _read_ui_sources()
        forbidden = [
            "st.info(",
            "st.warning(",
            "st.success(",
            "st.error(",
            "st.progress(",
            "st.spinner(",
            "st.balloons(",
        ]
        for token in forbidden:
            assert token not in sources

        components_source = _read("ui/components.py")
        widgets_source = _read("ui/styles/_widgets.py")
        assert "def render_status_notice(" in components_source
        assert "status-notice-icon {icon_class}" in components_source
        assert '<span class="status-notice-icon">{icon_svg(icon_name)}</span>' not in components_source
        assert ".status-notice" in widgets_source
        assert ".status-notice-icon::before" in widgets_source
        assert "--status-icon-info" in widgets_source
        assert ".status-icon-block" in widgets_source
        assert "body.rag-dark .status-notice" in _read("ui/styles/_dark_refinement.py")

    def test_dark_refinement_loads_after_component_styles(self):
        registry = _read("ui/styles/__init__.py")
        widgets_pos = registry.index("_widgets_mod.WIDGETS_CSS")
        buttons_pos = registry.index("_buttons_mod.BUTTONS_CSS")
        dark_refinement_pos = registry.index("_dark_refinement_mod.DARK_REFINEMENT_CSS")
        mobile_refinement_pos = registry.index("_mobile_refinement_mod.MOBILE_REFINEMENT_CSS")

        assert widgets_pos < dark_refinement_pos
        assert buttons_pos < dark_refinement_pos
        assert dark_refinement_pos < mobile_refinement_pos

    def test_upload_internal_triggers_stay_hidden(self):
        upload_css = _read("ui/styles/_upload.py")
        assert 'div[class*="st-key-upload_preview_prev"]' in upload_css
        assert 'div[class*="st-key-upload_preview_next"]' in upload_css
        assert "display: none !important" in upload_css
        assert "visibility: hidden !important" in upload_css

    def test_dark_upload_and_sidebar_tooltips_stay_readable(self):
        sidebar_source = _read("ui/sidebar.py")
        chat_source = _read("ui/chat.py")
        js_source = _read("ui/js_injection.py")
        sidebar_css = _read("ui/styles/_sidebar.py")
        sidebar_refinement = _read("ui/styles/_sidebar_refinement.py")
        dark_css = _read("ui/styles/_dark_refinement.py")

        assert 'key=f"collection_row_more_{collection_id}",\n                                use_container_width=True' in sidebar_source
        assert 'key=f"session_row_more_{session_id}",\n                            use_container_width=True' in sidebar_source
        assert "help=collection_name" not in sidebar_source
        assert "help=session_name" not in sidebar_source
        assert "分享或导出当前会话" not in sidebar_source
        assert "将该会话移到列表顶部" not in sidebar_source
        assert "将该知识库移到列表顶部" not in sidebar_source
        assert "发送示例问题" not in chat_source
        assert 'help="AI 正在回答，请稍候"' not in chat_source
        assert 'help="快速发送' not in chat_source
        assert "button.removeAttribute(\"title\")" in js_source
        assert "{ title: false }" in js_source

        assert 'div[class*="st-key-collection_row_more_"] button:hover' in sidebar_css
        assert 'div[class*="st-key-session_row_more_"] button:hover' in sidebar_refinement
        assert "background: transparent !important" in sidebar_refinement

        assert 'body.rag-dark [data-testid="stFileUploader"] section' in dark_css
        assert 'body.rag-dark [data-testid="stFileUploaderDropzone"]' in dark_css
        assert 'body.rag-dark div[data-testid="stExpander"] summary' in dark_css
        assert 'body.rag-dark div[data-testid="stExpander"] div[class*="st-key-sample_question_"] button' in dark_css
        assert 'body.rag-dark [data-testid="stSidebar"] div[class*="st-key-collection_row_more_"] button:hover' in dark_css
        assert 'body.rag-dark div[data-testid="stTextInput"] > div:focus-within' in dark_css
        assert 'body.rag-dark div[class*="st-key-sample_question_"] button' in dark_css
        assert 'body.rag-dark div[class*="st-key-quick_prompt_"] button:disabled' in dark_css
        assert '[data-testid="stFileUploader"] section svg rect' in _read("ui/styles/_widgets.py")
        assert "color: var(--rag-text-secondary) !important" in dark_css
        assert "fill: none !important" in dark_css
        assert "stroke: currentColor !important" in dark_css

    def test_legacy_frontend_selectors_do_not_reappear(self):
        styles = "\n".join(path.read_text(encoding="utf-8") for path in (UI_ROOT / "styles").glob("*.py"))
        legacy_selectors = [
            "upload-docs-table",
            "uploaded-files",
            "uploaded-file",
            "collection-menu",
            "session-menu",
            "sidebar-new-btn",
            "upload-task-list",
            "mode-select-btn",
        ]
        for selector in legacy_selectors:
            assert selector not in styles

    def test_interview_demo_copy_stays_visible(self):
        components_source = _read("ui/components.py")
        chat_source = _read("ui/chat.py")
        pages_source = _read("ui/pages.py")
        upload_source = _read("ui/upload.py")
        sidebar_source = _read("ui/sidebar.py")

        assert "Interview-ready RAG Workbench" in components_source
        assert "混合检索" in components_source
        assert "Agent/Web" in components_source
        assert "排障 ID" in components_source

        assert "BM25 在 RAG 检索中有什么作用？" in chat_source
        assert "火星基地厨房的虚构配置项" in chat_source
        assert "3 步开始一次可追溯问答" in chat_source

        assert "优先查本地资料" in pages_source
        assert "证据摘要" in pages_source
        assert "公开演示不会提交本地 Chroma" in pages_source
        assert "资料库 / My Stuff" in pages_source
        assert "AI 工作空间" in sidebar_source
        assert "知识空间" in sidebar_source
        assert "最近对话" in sidebar_source

        assert "公开仓库不包含 Chroma、session、日志或密钥" in upload_source
        assert "脱敏 Markdown/PDF" in upload_source
        assert "解析中" in upload_source
        assert "已入库" in upload_source
        assert "可提问" in upload_source

    def test_empty_state_icons_use_css_masks_not_inline_svg(self):
        components_source = _read("ui/components.py")
        empty_state_style = _read("ui/styles/_empty_states.py")
        upload_source = _read("ui/upload.py")

        assert 'render_empty_state(\n            "upload"' in upload_source
        assert "_empty_icon_class" in components_source
        assert "workspace-empty-icon {_empty_icon_class(icon_name)}" in components_source
        assert "workspace-empty-step-icon {_empty_icon_class(step_icon)}" in components_source
        assert ".workspace-empty-icon::before" in empty_state_style
        assert ".workspace-empty-step-icon::before" in empty_state_style
        assert "--empty-icon-upload" in empty_state_style
        assert ".empty-icon-upload" in empty_state_style
        assert "-webkit-mask: var(--empty-icon-mask" in empty_state_style

    def test_source_evidence_panel_keeps_demo_fields(self):
        components_source = _read("ui/components.py")
        chat_style = _read("ui/styles/_chat.py")
        dark_style = _read("ui/styles/_dark_refinement.py")

        assert "引用证据" in components_source
        assert "来源 #" in components_source
        assert "证据片段" in components_source
        assert "render_answer_status_bar" in components_source
        assert "answer-status-bar" in components_source
        assert "source-trace-chip" in components_source
        assert "candidate_source" in components_source
        assert "source-index" in components_source
        assert "source-file" in components_source
        assert "source-score" in components_source

        assert ".answer-status-chip" in chat_style
        assert ".source-trace-chip" in chat_style
        assert ".source-index" in chat_style
        assert ".source-file" in chat_style
        assert ".source-score" in chat_style
        assert ".source-label" in chat_style

        assert "body.rag-dark .source-index" in dark_style
        assert "body.rag-dark .source-score" in dark_style

    def test_agent_debug_panel_shows_policy_and_budget(self):
        chat_source = _read("ui/chat.py")
        assert "evidence_summary" in chat_source
        assert "证据摘要:" in chat_source
        assert "本地兜底" in chat_source
        assert "Web 已降级" in chat_source
        assert "policy_violations" in chat_source
        assert "tool_policy" in chat_source
        assert "工具策略:" in chat_source
        assert "tool_budget" in chat_source
        assert "工具预算:" in chat_source
        assert "source_layers" in chat_source
        assert "来源层级:" in chat_source
        assert "执行轨迹" in chat_source
        assert ".agent-debug-title" in _read("ui/styles/_chat.py")

    def test_agent_debug_steps_render_local_only_evidence_summary(self):
        from ui.chat import _build_agent_debug_steps

        steps = _build_agent_debug_steps([], {
            "evidence_summary": {
                "mode": "local_only",
                "local_used": True,
                "web_used": False,
            },
        })

        assert steps[0]["text"] == "证据摘要: 本地资料"
        assert "Web:" not in steps[0]["text"]

    def test_agent_debug_steps_render_local_web_fallback_and_policy_violation(self):
        from ui.chat import _build_agent_debug_steps

        steps = _build_agent_debug_steps([], {
            "evidence_summary": {
                "mode": "local_plus_web",
                "local_used": True,
                "web_used": True,
                "local_fallback_used": True,
                "web_provider": "Tavily",
                "web_fallback_used": True,
                "web_attempt_count": 1,
                "web_result_count": 2,
                "policy_violations": ["web_used_for_non_realtime_question"],
            },
        })
        text = steps[0]["text"]

        assert text.startswith("证据摘要: 本地资料 + 外部补充")
        assert "本地兜底" in text
        assert "Web: Tavily，1 次尝试，2 条结果" in text
        assert "Web 已降级" in text
        assert "策略提醒: web_used_for_non_realtime_question" in text

    def test_agent_debug_steps_keep_legacy_debug_without_evidence_summary(self):
        from ui.chat import _build_agent_debug_steps

        steps = _build_agent_debug_steps([], {
            "source_layers": {"mode": "web_only", "local_priority": False},
            "search_trace": {
                "provider": "Tavily",
                "result_count": 3,
                "fallback_used": True,
                "attempts": [{"provider": "Tavily"}],
            },
            "tool_budget": {
                "counts": {"total": 1, "search_web": 1, "execute_python_code": 0},
                "limits": {
                    "max_tool_calls": 4,
                    "max_web_searches": 1,
                    "max_code_executions": 0,
                },
                "violations": ["web_used_for_non_realtime_question"],
            },
        })
        texts = [step["text"] for step in steps]

        assert not any(text.startswith("证据摘要:") for text in texts)
        assert any("来源层级: 外部搜索" in text for text in texts)
        assert any(
            "搜索服务:" in text and "Tavily" in text and "已降级" in text
            for text in texts
        )
        assert any(
            "工具预算:" in text
            and "策略提醒: web_used_for_non_realtime_question" in text
            for text in texts
        )

    def test_failed_chat_messages_append_request_diagnostic_suffix(self):
        chat_source = _read("ui/chat.py")

        assert "diagnostic_suffix = format_last_response_diagnostic_suffix()" in chat_source
        assert "_format_request_diagnostic_suffix" not in chat_source
        assert "Agent 执行出错" in chat_source
        assert "回答问题时出现错误" in chat_source

    def test_operation_failure_messages_append_request_diagnostic_suffix(self):
        sidebar_source = _read("ui/sidebar.py")
        pages_source = _read("ui/pages.py")
        upload_source = _read("ui/upload.py")

        assert "format_last_response_diagnostic_suffix" in sidebar_source
        assert "删除失败，请稍后重试" in sidebar_source
        assert "创建失败" in sidebar_source
        assert "重命名失败" in sidebar_source

        assert "format_last_response_diagnostic_suffix" in pages_source
        assert "批量删除失败" in pages_source
        assert "获取文档列表失败" in pages_source
        assert "失败 {fail} 个{format_last_response_diagnostic_suffix()}" in pages_source

        assert "format_last_response_diagnostic_suffix" in upload_source
        assert "上传失败" in upload_source
        assert "format_last_response_diagnostic_suffix(prefix='；')" in upload_source
