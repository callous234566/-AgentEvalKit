import json
import re
from pathlib import Path

from langchain_core.messages import AIMessage, ToolMessage


def test_agent_prompt_discourages_new_runtime_dependencies():
    from rag.agent import AGENT_SYSTEM_PROMPT

    assert "不要默认建议安装新库" in AGENT_SYSTEM_PROMPT
    assert "pip install" in AGENT_SYSTEM_PROMPT
    assert "标准库" in AGENT_SYSTEM_PROMPT
    assert "RAG 评估" in AGENT_SYSTEM_PROMPT
    assert "本地知识库优先" in AGENT_SYSTEM_PROMPT
    assert "实时" in AGENT_SYSTEM_PROMPT


def test_agent_eval_cases_are_valid_json():
    cases = json.loads(Path("eval/agent_eval_cases.json").read_text(encoding="utf-8"))

    assert len(cases) >= 5
    assert all(case.get("id") and case.get("question") for case in cases)


def test_agent_guide_documents_eval_and_debug_contracts():
    guide = Path("docs/AGENT_GUIDE.md").read_text(encoding="utf-8")
    cases = json.loads(Path("eval/agent_eval_cases.json").read_text(encoding="utf-8"))

    for case in cases:
        assert case["id"] in guide

    for field in [
        "routing_decision",
        "tool_sequence",
        "tool_budget",
        "search_trace",
        "evidence_summary",
        "evidence_items",
        "fallback_reason",
        "fallback_used",
    ]:
        assert field in guide


def test_tool_policy_prefers_local_knowledge_for_project_questions():
    from rag.agent import _classify_tool_policy

    policy = _classify_tool_policy("LangChain 的核心模块有哪些？")

    assert policy["category"] == "local_knowledge"
    assert policy["recommended_first_tool"] == "search_knowledge_base"
    assert policy["local_first"] is True
    assert policy["allows_web"] is False


def test_tool_policy_allows_web_for_realtime_questions():
    from rag.agent import _classify_tool_policy

    policy = _classify_tool_policy("2026 年 Python 最新版本是什么？")

    assert policy["category"] == "external_realtime"
    assert policy["recommended_first_tool"] == "search_web"
    assert policy["allows_web"] is True


def test_routing_decision_restricts_local_questions_to_knowledge_base():
    from rag.agent import _classify_tool_policy, _routing_decision

    decision = _routing_decision(_classify_tool_policy("LangChain 的核心模块有哪些？"))

    assert decision["category"] == "local_knowledge"
    assert decision["allowed_tools"] == ["search_knowledge_base"]
    assert decision["preferred_tool"] == "search_knowledge_base"
    assert decision["strong"] is True


def test_routing_decision_allows_web_for_realtime_questions():
    from rag.agent import _classify_tool_policy, _routing_decision

    decision = _routing_decision(_classify_tool_policy("2026 年 Python 最新版本是什么？"))

    assert decision["category"] == "external_realtime"
    assert decision["allowed_tools"] == ["search_web"]
    assert decision["preferred_tool"] == "search_web"
    assert decision["strong"] is True


def test_tool_budget_summary_reports_policy_violations(monkeypatch):
    import config
    from rag.agent import _classify_tool_policy, _tool_budget_summary

    monkeypatch.setattr(config, "AGENT_MAX_TOOL_CALLS", 2)
    monkeypatch.setattr(config, "AGENT_MAX_WEB_SEARCHES", 1)
    monkeypatch.setattr(config, "AGENT_MAX_CODE_EXECUTIONS", 1)
    policy = _classify_tool_policy("LangChain 的核心模块有哪些？")

    summary = _tool_budget_summary(["search_web", "search_web", "execute_python_code"], policy)

    assert summary["counts"]["total"] == 3
    assert "max_tool_calls" in summary["violations"]
    assert "max_web_searches" in summary["violations"]
    assert "local_first_not_followed" in summary["violations"]
    assert "web_used_for_non_realtime_question" in summary["violations"]


def test_source_layers_and_layered_answer_for_local_plus_web():
    from rag.agent import _ensure_layered_answer, _source_layer_summary

    layers = _source_layer_summary(["search_knowledge_base", "search_web"])
    answer = _ensure_layered_answer("综合回答", layers)

    assert layers["mode"] == "local_plus_web"
    assert "### 本地资料" in answer
    assert "### 外部搜索补充" in answer
    assert "### 来源提示" in answer


def test_layered_answer_is_not_wrapped_twice():
    from rag.agent import _ensure_layered_answer

    answer = "### 本地资料\nA\n\n### 外部搜索补充\nB"
    result = _ensure_layered_answer(answer, {"mode": "local_plus_web"})

    assert result == answer


def test_run_agent_returns_debug_info_for_tool_calls(monkeypatch):
    from rag import tools
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 3

        def invoke(self, payload, config):
            assert config["recursion_limit"] == 7
            assert payload["messages"][0].type == "system"
            assert "本次工具策略" in payload["messages"][0].content
            assert "search_knowledge_base" in payload["messages"][0].content
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_web",
                            "args": {"query": "Tavily 测试"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="搜索结果摘要", tool_call_id="call-1"),
                    AIMessage(content="最终回答"),
                ]
            }

    monkeypatch.setattr(tools, "get_last_search_trace", lambda: {
        "provider": "Tavily",
        "attempts": [{"provider": "Tavily", "attempt": 1, "success": True, "error": ""}],
        "fallback_used": False,
        "result_count": 1,
    })

    result = run_agent(FakeAgent(), "问题", debug=True)

    assert result["success"] is True
    assert result["answer"] == "最终回答"
    assert result["agent_steps"][0]["tool"] == "search_web"
    assert result["debug_info"]["enabled"] is True
    assert result["debug_info"]["tool_sequence"] == ["search_web"]
    assert result["debug_info"]["search_trace"]["provider"] == "Tavily"
    assert result["debug_info"]["tool_policy"]["category"] == "local_knowledge"
    assert result["debug_info"]["tool_budget"]["counts"]["search_web"] == 1
    assert "web_used_for_non_realtime_question" in result["debug_info"]["tool_budget"]["violations"]
    assert result["debug_info"]["evidence_summary"]["mode"] == "web_only"
    assert result["debug_info"]["evidence_summary"]["web_provider"] == "Tavily"
    assert result["debug_info"]["evidence_summary"]["web_attempt_count"] == 1
    assert result["debug_info"]["routing_decision"]["allowed_tools"] == ["search_knowledge_base"]


def test_run_agent_invokes_constrained_agent_for_local_question(monkeypatch):
    import rag.agent as agent_module
    from rag.agent import run_agent

    created_tool_names = []

    class FakeTool:
        def __init__(self, name):
            self.name = name

        def invoke(self, payload):
            return ""

    class OriginalAgent:
        max_iterations = 3
        _rag_llm = object()
        _rag_all_tools = [
            FakeTool("search_knowledge_base"),
            FakeTool("search_web"),
            FakeTool("execute_python_code"),
        ]
        _rag_tools_by_name = {tool.name: tool for tool in _rag_all_tools}

        def invoke(self, payload, config):
            raise AssertionError("original agent should be replaced by constrained agent")

    class ConstrainedAgent:
        max_iterations = 3

        def invoke(self, payload, config):
            return {"messages": [AIMessage(content="本地回答")]}

    def fake_create_react_agent(model, tools, prompt):
        created_tool_names.append([tool.name for tool in tools])
        constrained = ConstrainedAgent()
        constrained._rag_tools_by_name = {tool.name: tool for tool in tools}
        return constrained

    monkeypatch.setattr(agent_module, "create_react_agent", fake_create_react_agent)

    result = run_agent(OriginalAgent(), "LangChain 的核心模块有哪些？", debug=True)

    assert result["success"] is True
    assert result["answer"] == "本地回答"
    assert created_tool_names == [["search_knowledge_base"]]
    assert result["debug_info"]["routing_decision"]["allowed_tools"] == ["search_knowledge_base"]


def test_run_agent_builds_unified_evidence_items_for_local_tool():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 3

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_knowledge_base",
                            "args": {"query": "LangChain"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="[片段 1] (来源: langchain.md)\nLangChain 核心模块。", tool_call_id="call-1"),
                    AIMessage(content="LangChain 核心模块说明"),
                ]
            }

    result = run_agent(FakeAgent(), "LangChain 的核心模块有哪些？", debug=True)

    evidence_items = result["debug_info"]["evidence_items"]
    assert evidence_items[0]["type"] == "local"
    assert evidence_items[0]["tool"] == "search_knowledge_base"
    assert "LangChain" in evidence_items[0]["snippet"]


def test_run_agent_records_fallback_reason_on_execution_error():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 3

        def invoke(self, payload, config):
            raise RuntimeError("agent failed")

    result = run_agent(FakeAgent(), "LangChain 的核心模块有哪些？", debug=True)

    assert result["success"] is False
    assert result["debug_info"]["fallback_reason"] == "agent_execution_error"
    assert "agent failed" in result["error"]


def test_run_agent_enforces_local_first_after_web_only_tool_call(monkeypatch):
    from rag import tools
    from rag.agent import run_agent

    class FakeTool:
        name = "search_knowledge_base"

        def invoke(self, payload):
            assert payload["query"] == "LangChain 的核心模块有哪些？"
            return "[片段 1] (来源: langchain.md)\nLangChain 核心模块包括模型、提示词和链。"

    class FakeAgent:
        max_iterations = 3
        _rag_tools_by_name = {"search_knowledge_base": FakeTool()}

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_web",
                            "args": {"query": "LangChain 核心模块"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="网页搜索结果", tool_call_id="call-1"),
                    AIMessage(content="根据网页搜索，LangChain 有若干模块。"),
                ]
            }

    monkeypatch.setattr(tools, "get_last_search_trace", lambda: {
        "provider": "Tavily",
        "attempts": [{"provider": "Tavily", "attempt": 1, "success": True, "error": ""}],
        "fallback_used": False,
        "result_count": 1,
    })

    result = run_agent(FakeAgent(), "LangChain 的核心模块有哪些？", debug=True)

    assert result["success"] is True
    assert result["debug_info"]["tool_sequence"] == ["search_web", "search_knowledge_base"]
    assert result["agent_steps"][0]["tool"] == "search_web"
    assert result["agent_steps"][1]["tool"] == "search_knowledge_base"
    assert result["debug_info"]["policy_fallbacks"] == ["local_first_enforced"]
    assert result["debug_info"]["source_layers"]["mode"] == "local_plus_web"
    assert "web_used_for_non_realtime_question" in result["debug_info"]["tool_budget"]["violations"]
    assert "local_first_not_followed" in result["debug_info"]["tool_budget"]["violations"]
    summary = result["debug_info"]["evidence_summary"]
    assert summary["mode"] == "local_plus_web"
    assert summary["local_used"] is True
    assert summary["web_used"] is True
    assert summary["local_fallback_used"] is True
    assert summary["web_provider"] == "Tavily"
    assert "web_used_for_non_realtime_question" in summary["policy_violations"]
    assert "### 本地资料" in result["answer"]
    assert "### 外部搜索补充" in result["answer"]
    assert "### 来源提示" in result["answer"]
    assert "langchain.md" in result["answer"]


def test_run_agent_hides_debug_info_when_disabled():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            return {"messages": [AIMessage(content="最终回答")]}

    result = run_agent(FakeAgent(), "问题", debug=False)

    assert result["success"] is True
    assert result["debug_info"] == {}


def test_run_agent_local_question_uses_local_only_debug_layer():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_knowledge_base",
                            "args": {"query": "LangChain 核心模块"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="本地资料片段", tool_call_id="call-1"),
                    AIMessage(content="LangChain 核心模块包括模型、提示词和链。"),
                ]
            }

    result = run_agent(FakeAgent(), "LangChain 的核心模块有哪些？", debug=True)

    assert result["success"] is True
    assert result["debug_info"]["tool_policy"]["category"] == "local_knowledge"
    assert result["debug_info"]["source_layers"]["mode"] == "local_only"
    assert result["debug_info"]["tool_budget"]["violations"] == []
    assert result["debug_info"]["evidence_summary"]["mode"] == "local_only"
    assert result["debug_info"]["evidence_summary"]["local_used"] is True
    assert result["debug_info"]["evidence_summary"]["web_used"] is False
    assert "外部搜索补充" not in result["answer"]


def test_run_agent_enforces_local_first_when_bound_tool_is_available():
    from rag.agent import run_agent

    class FakeTool:
        name = "search_knowledge_base"

        def invoke(self, payload):
            assert payload["query"] == "LangChain 的核心模块有哪些？"
            return "[片段 1] (来源: langchain.md)\nLangChain 核心模块包括模型、提示词和链。"

    class FakeAgent:
        max_iterations = 2
        _rag_tools_by_name = {"search_knowledge_base": FakeTool()}

        def invoke(self, payload, config):
            return {"messages": [AIMessage(content="请补充更多背景。")]}

    result = run_agent(FakeAgent(), "LangChain 的核心模块有哪些？", debug=True)

    assert result["success"] is True
    assert result["debug_info"]["tool_sequence"] == ["search_knowledge_base"]
    assert result["debug_info"]["source_layers"]["mode"] == "local_only"
    assert result["debug_info"]["policy_fallbacks"] == ["local_first_enforced"]
    assert result["debug_info"]["evidence_summary"]["local_fallback_used"] is True
    assert "根据本地知识库检索结果" in result["answer"]
    assert "langchain.md" in result["answer"]


def test_run_agent_realtime_question_allows_web_debug_layer(monkeypatch):
    from rag import tools
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_web",
                            "args": {"query": "2026 Python 最新版本"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="网页搜索结果", tool_call_id="call-1"),
                    AIMessage(content="根据网页搜索，Python 有新版本信息。"),
                ]
            }

    monkeypatch.setattr(tools, "get_last_search_trace", lambda: {
        "provider": "Tavily",
        "attempts": [{"provider": "Tavily", "attempt": 1, "success": True, "error": ""}],
        "fallback_used": False,
        "result_count": 2,
    })

    result = run_agent(FakeAgent(), "2026 年 Python 最新版本是什么？", debug=True)

    assert result["success"] is True
    assert result["debug_info"]["tool_policy"]["category"] == "external_realtime"
    assert result["debug_info"]["source_layers"]["mode"] == "web_only"
    assert "web_used_for_non_realtime_question" not in result["debug_info"]["tool_budget"]["violations"]
    summary = result["debug_info"]["evidence_summary"]
    assert summary["mode"] == "web_only"
    assert summary["local_used"] is False
    assert summary["web_used"] is True
    assert summary["web_provider"] == "Tavily"
    assert summary["web_attempt_count"] == 1
    assert summary["web_result_count"] == 2
    assert summary["web_fallback_used"] is False


def test_run_agent_layers_answer_when_local_and_web_tools_are_used():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 3

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_knowledge_base",
                            "args": {"query": "项目资料"},
                            "id": "call-1",
                        }],
                    ),
                    ToolMessage(content="本地资料片段", tool_call_id="call-1"),
                    AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "search_web",
                            "args": {"query": "最新版本"},
                            "id": "call-2",
                        }],
                    ),
                    ToolMessage(content="网页补充", tool_call_id="call-2"),
                    AIMessage(content="综合回答"),
                ]
            }

    result = run_agent(FakeAgent(), "结合项目资料和最新版本说明", debug=True)

    assert result["success"] is True
    assert result["debug_info"]["source_layers"]["mode"] == "local_plus_web"
    assert "### 本地资料" in result["answer"]
    assert "### 外部搜索补充" in result["answer"]


def test_run_agent_rewrites_rag_eval_answer_to_stdlib_template():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(content="请先 pip install sklearn，然后 from sklearn.metrics import recall_score")
                ]
            }

    result = run_agent(
        FakeAgent(),
        "如何用 Python 生成 RAG 评估报告（自动计算准确率、召回率）？",
        debug=True,
    )

    assert result["success"] is True
    assert "pip install" not in result["answer"]
    assert "sklearn" not in result["answer"].lower()
    assert "Python 标准库" in result["answer"]
    assert "准确率" in result["answer"]
    assert "召回率" in result["answer"]


def test_run_agent_rewrites_generic_rag_eval_report_answer_to_template():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            return {
                "messages": [
                    AIMessage(content="可以用字符串匹配计算准确率和召回率，然后整理成报告。")
                ]
            }

    result = run_agent(
        FakeAgent(),
        "如何用 Python 生成 RAG 评估报告（自动计算准确率、召回率）？",
        debug=True,
    )

    assert result["success"] is True
    assert "rag_eval_report.md" in result["answer"]
    assert "eval_cases.json" in result["answer"]
    assert "def evaluate" in result["answer"]
    assert "def render_markdown" in result["answer"]


def test_run_agent_short_circuits_rag_eval_report_question():
    from rag.agent import run_agent

    class FakeAgent:
        max_iterations = 2

        def invoke(self, payload, config):
            raise AssertionError("RAG 评估报告模板问题不应进入工具循环")

    result = run_agent(
        FakeAgent(),
        "如何用 Python 生成 RAG 评估报告（自动计算准确率、召回率）？",
        debug=True,
    )

    assert result["success"] is True
    assert result["agent_steps"] == []
    assert result["debug_info"]["tool_sequence"] == []
    assert result["debug_info"]["evidence_summary"]["mode"] == "no_tool"
    assert result["debug_info"]["evidence_summary"]["local_used"] is False
    assert result["debug_info"]["evidence_summary"]["web_used"] is False
    assert "rag_eval_report.md" in result["answer"]


def test_stdlib_rag_eval_template_code_compiles():
    from rag.agent import _build_stdlib_rag_eval_answer

    answer = _build_stdlib_rag_eval_answer()
    match = re.search(r"```python\n(.*?)\n```", answer, re.DOTALL)

    assert match is not None
    compile(match.group(1), "rag_eval_report.py", "exec")
