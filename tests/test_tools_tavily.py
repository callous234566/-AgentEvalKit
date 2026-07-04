import sys
import types

from langchain_core.documents import Document


def test_create_tools_keeps_knowledge_base_before_web_search():
    from rag.tools import create_tools

    class FakeVectorStore:
        def similarity_search(self, query, collection_name):
            assert query == "LangChain 的核心模块有哪些？"
            assert collection_name == "中文知识库"
            return [
                Document(
                    page_content="LangChain 核心模块包括模型、提示词、链、检索器和 Agent。",
                    metadata={"source": "langchain.md"},
                )
            ]

    tools = create_tools(FakeVectorStore(), "中文知识库")

    assert [item.name for item in tools] == [
        "search_knowledge_base",
        "search_web",
        "execute_python_code",
    ]
    result = tools[0].invoke({"query": "LangChain 的核心模块有哪些？"})
    assert "LangChain 核心模块" in result
    assert "langchain.md" in result


def test_search_web_uses_tavily_when_api_key_is_configured(monkeypatch):
    import config
    from rag import tools

    class FakeTavilyClient:
        def __init__(self, api_key):
            self.api_key = api_key

        def search(self, **kwargs):
            assert self.api_key == "tvly-test"
            assert kwargs["query"] == "2026 年大模型最新进展"
            return {
                "answer": "结构化摘要",
                "results": [
                    {
                        "title": "新闻标题",
                        "content": "搜索结果摘要",
                        "url": "https://example.com/news",
                    }
                ],
            }

    fake_module = types.SimpleNamespace(TavilyClient=FakeTavilyClient)
    monkeypatch.setattr(config, "TAVILY_API_KEY", "tvly-test")
    monkeypatch.setitem(sys.modules, "tavily", fake_module)
    monkeypatch.setattr(tools, "_search_with_duckduckgo", lambda query: "DuckDuckGo fallback")

    result = tools.search_web.invoke({"query": "2026 年大模型最新进展"})
    trace = tools.get_last_search_trace()

    assert "[AI 摘要] 结构化摘要" in result
    assert "新闻标题" in result
    assert "https://example.com/news" in result
    assert "DuckDuckGo fallback" not in result
    assert trace["provider"] == "Tavily"
    assert trace["fallback_used"] is False
    assert trace["result_count"] == 1
    assert trace["error"] == ""
    assert trace["attempts"] == [
        {"provider": "Tavily", "attempt": 1, "success": True, "error": ""}
    ]


def test_search_web_retries_tavily_and_deduplicates_results(monkeypatch):
    import config
    from rag import tools

    calls = {"count": 0}

    class FakeTavilyClient:
        def __init__(self, api_key):
            self.api_key = api_key

        def search(self, **kwargs):
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("temporary outage")
            return {
                "results": [
                    {
                        "title": "<b>标题 A</b>",
                        "content": "摘要 A &amp; 更多内容",
                        "url": "https://example.com/a",
                    },
                    {
                        "title": "重复标题",
                        "content": "重复摘要",
                        "url": "https://example.com/a/",
                    },
                ],
            }

    fake_module = types.SimpleNamespace(TavilyClient=FakeTavilyClient)
    monkeypatch.setattr(config, "TAVILY_API_KEY", "tvly-test")
    monkeypatch.setattr(config, "TOOL_RETRY_MAX_ATTEMPTS", 2)
    monkeypatch.setattr(config, "TOOL_RETRY_BACKOFF_SECONDS", 0)
    monkeypatch.setitem(sys.modules, "tavily", fake_module)

    result = tools.search_web.invoke({"query": "测试重试"})
    trace = tools.get_last_search_trace()

    assert calls["count"] == 2
    assert "标题 A" in result
    assert "<b>" not in result
    assert result.count("https://example.com/a") == 1
    assert trace["provider"] == "Tavily"
    assert trace["fallback_used"] is False
    assert trace["result_count"] == 1
    assert trace["error"] == ""
    assert len(trace["attempts"]) == 2
    assert trace["attempts"][0]["success"] is False
    assert trace["attempts"][1]["success"] is True


def test_search_web_falls_back_to_duckduckgo_without_api_key(monkeypatch):
    import config
    from rag import tools

    class FakeResponse:
        text = '''
        <a rel="nofollow" class="result__a" href="https://example.com/python">Python</a>
        <a class="result__snippet">Python 版本摘要</a>
        '''

        def raise_for_status(self):
            return None

    def fake_post(url, data, headers, timeout):
        assert data["q"] == "2026 年 Python 最新版本"
        return FakeResponse()

    monkeypatch.setattr(config, "TAVILY_API_KEY", "")
    monkeypatch.setattr(config, "TOOL_RETRY_MAX_ATTEMPTS", 1)
    monkeypatch.setattr(tools.requests, "post", fake_post)

    result = tools.search_web.invoke({"query": "2026 年 Python 最新版本"})
    trace = tools.get_last_search_trace()

    assert "Python 版本摘要" in result
    assert trace["provider"] == "DuckDuckGo"
    assert trace["fallback_used"] is True
    assert trace["result_count"] == 1
    assert trace["error"] == ""
    assert trace["attempts"] == [
        {"provider": "DuckDuckGo", "attempt": 1, "success": True, "error": ""}
    ]


def test_duckduckgo_parser_unwraps_redirect_urls():
    from rag.tools import _parse_duckduckgo_results

    html = '''
    <a rel="nofollow" class="result__a" href="/l/?kh=-1&amp;uddg=https%3A%2F%2Fexample.com%2Freal">标题</a>
    <a class="result__snippet">摘要内容</a>
    '''

    results = _parse_duckduckgo_results(html)

    assert results[0]["url"] == "https://example.com/real"


def test_execute_python_code_guides_retry_when_module_is_missing():
    from rag.tools import execute_python_code

    result = execute_python_code.invoke({"code": "import definitely_missing_rag_eval_lib"})

    assert "未安装第三方库" in result
    assert "definitely_missing_rag_eval_lib" in result
    assert "改用 Python 标准库" in result
    assert "Traceback" not in result


def test_execute_python_code_blocks_file_network_and_system_operations():
    from rag.tools import execute_python_code

    blocked_inputs = [
        "open('secret.txt').read()",
        "import socket\nsocket.socket()",
        "import os\nos.system('echo unsafe')",
    ]

    for code in blocked_inputs:
        result = execute_python_code.invoke({"code": code})
        assert "安全限制" in result


def test_search_web_reports_tavily_error_before_duckduckgo_fallback(monkeypatch):
    import config
    from rag import tools

    class FakeTavilyClient:
        def __init__(self, api_key):
            self.api_key = api_key

        def search(self, **kwargs):
            raise RuntimeError("invalid api key")

    fake_module = types.SimpleNamespace(TavilyClient=FakeTavilyClient)
    monkeypatch.setattr(config, "TAVILY_API_KEY", "bad-key")
    monkeypatch.setattr(config, "TOOL_RETRY_MAX_ATTEMPTS", 1)
    monkeypatch.setitem(sys.modules, "tavily", fake_module)

    class FakeResponse:
        text = '''
        <a rel="nofollow" class="result__a" href="https://example.com/weather">天气</a>
        <a class="result__snippet">DuckDuckGo 结果</a>
        '''

        def raise_for_status(self):
            return None

    monkeypatch.setattr(tools.requests, "post", lambda *args, **kwargs: FakeResponse())

    result = tools.search_web.invoke({"query": "今天天气"})
    trace = tools.get_last_search_trace()

    assert "Tavily 搜索失败（invalid api key），已切换到 DuckDuckGo" in result
    assert "DuckDuckGo 结果" in result
    assert trace["provider"] == "DuckDuckGo"
    assert trace["fallback_used"] is True
    assert trace["result_count"] == 1
    assert trace["error"] == ""
    assert trace["attempts"][0]["provider"] == "Tavily"
    assert trace["attempts"][0]["success"] is False
    assert trace["attempts"][1]["provider"] == "DuckDuckGo"
    assert trace["attempts"][1]["success"] is True


def test_search_web_trace_records_duckduckgo_failure(monkeypatch):
    import config
    from rag import tools

    def fake_post(*args, **kwargs):
        raise RuntimeError("duckduckgo outage")

    monkeypatch.setattr(config, "TAVILY_API_KEY", "")
    monkeypatch.setattr(config, "TOOL_RETRY_MAX_ATTEMPTS", 1)
    monkeypatch.setattr(config, "TOOL_RETRY_BACKOFF_SECONDS", 0)
    monkeypatch.setattr(tools.requests, "post", fake_post)

    result = tools.search_web.invoke({"query": "外部搜索失败"})
    trace = tools.get_last_search_trace()

    assert "duckduckgo outage" in result
    assert trace["provider"] == "DuckDuckGo"
    assert trace["fallback_used"] is True
    assert trace["result_count"] == 0
    assert trace["error"] == "duckduckgo outage"
    assert trace["attempts"] == [
        {
            "provider": "DuckDuckGo",
            "attempt": 1,
            "success": False,
            "error": "duckduckgo outage",
        }
    ]
