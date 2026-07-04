"""Agent tools: knowledge base search, web search, and Python execution."""

import html
import logging
import re
import subprocess
import sys
import time
from typing import Callable
from urllib.parse import parse_qs, unquote, urlparse

import requests
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

_LAST_SEARCH_TRACE: dict = {}


def get_last_search_trace() -> dict:
    """Return debug details for the most recent web search tool call."""
    return dict(_LAST_SEARCH_TRACE)


def _reset_search_trace(query: str) -> None:
    _LAST_SEARCH_TRACE.clear()
    _LAST_SEARCH_TRACE.update({
        "query": query,
        "provider": "",
        "attempts": [],
        "fallback_used": False,
        "result_count": 0,
        "error": "",
    })


def _record_attempt(provider: str, attempt: int, success: bool, error: str = "") -> None:
    _LAST_SEARCH_TRACE.setdefault("attempts", []).append({
        "provider": provider,
        "attempt": attempt,
        "success": success,
        "error": error,
    })


def _retry_call(provider: str, fn: Callable[[], str]) -> str:
    import config

    attempts = max(1, int(getattr(config, "TOOL_RETRY_MAX_ATTEMPTS", 2)))
    delay = max(0.0, float(getattr(config, "TOOL_RETRY_BACKOFF_SECONDS", 0.5)))
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            result = fn()
            _record_attempt(provider, attempt, True)
            return result
        except Exception as exc:
            last_error = str(exc)
            _record_attempt(provider, attempt, False, last_error)
            logger.warning("%s search attempt %s failed: %s", provider, attempt, exc)
            if attempt < attempts and delay:
                time.sleep(delay * attempt)
    raise RuntimeError(last_error or f"{provider} search failed")


def _clean_text(value: str, max_chars: int = 320) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        return text[:max_chars].rstrip() + "..."
    return text


def _format_search_results(items: list[dict], answer: str = "") -> str:
    import config

    max_results = max(1, int(getattr(config, "WEB_SEARCH_MAX_RESULTS", 5)))
    seen_urls = set()
    formatted = []

    answer = _clean_text(answer, 600)
    if answer:
        formatted.append(f"[AI 摘要] {answer}")

    for item in items:
        title = _clean_text(item.get("title", ""), 120) or "未命名结果"
        snippet = _clean_text(item.get("content") or item.get("snippet") or "", 420)
        url = str(item.get("url") or "").strip()
        if url:
            normalized_url = url.rstrip("/")
            if normalized_url in seen_urls:
                continue
            seen_urls.add(normalized_url)
        if not snippet:
            continue

        index = len(formatted) + (0 if answer else 1)
        entry = f"{index}. {title}\n   摘要: {snippet}"
        if url:
            entry += f"\n   来源: {url}"
        formatted.append(entry)
        if len(formatted) - (1 if answer else 0) >= max_results:
            break

    _LAST_SEARCH_TRACE["result_count"] = len(formatted) - (1 if answer else 0)
    return "\n\n".join(formatted) if formatted else "未搜索到相关结果。"


# ============== 知识库检索工具 ==============


def create_knowledge_base_tool(vector_store, collection_name: str = "default"):
    """Create a retrieval tool bound to one knowledge base."""

    @tool
    def search_knowledge_base(query: str) -> str:
        """从本地知识库中检索相关文档片段。用户问题涉及已有资料时优先使用。

        Args:
            query: 检索查询语句，尽量使用关键词和完整表述
        """
        try:
            docs = vector_store.similarity_search(
                query=query,
                collection_name=collection_name,
            )
            if not docs:
                return "知识库中未找到相关文档。"

            results = []
            for i, doc in enumerate(docs[:5], 1):
                source = doc.metadata.get("source", "未知来源")
                content = _clean_text(doc.page_content, 900)
                if content:
                    results.append(f"[片段 {i}] (来源: {source})\n{content}")

            return "\n\n".join(results) if results else "知识库中未找到相关文档。"
        except Exception as e:
            logger.error("知识库检索失败: %s", e)
            return f"知识库检索出错: {str(e)}"

    return search_knowledge_base


# ============== 网页搜索工具 ==============


def _search_with_tavily(query: str) -> str:
    """Search with Tavily Search API."""
    import config

    if not config.TAVILY_API_KEY:
        return ""

    def call_tavily() -> str:
        from tavily import TavilyClient

        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=getattr(config, "WEB_SEARCH_MAX_RESULTS", 5),
            search_depth=getattr(config, "TAVILY_SEARCH_DEPTH", "basic"),
        )
        return _format_search_results(
            response.get("results", []),
            response.get("answer", ""),
        )

    try:
        result = _retry_call("Tavily", call_tavily)
        _LAST_SEARCH_TRACE["provider"] = "Tavily"
        return result
    except Exception as e:
        _LAST_SEARCH_TRACE["error"] = str(e)
        logger.error("Tavily 搜索失败: %s", e)
        return ""


def _parse_duckduckgo_results(html_text: str) -> list[dict]:
    snippets = re.findall(
        r'class="result__snippet"[^>]*>(.*?)</a>',
        html_text,
        re.DOTALL,
    )
    titles = re.findall(
        r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        html_text,
        re.DOTALL,
    )

    results = []
    for i, snippet in enumerate(snippets):
        url = titles[i][0] if i < len(titles) else ""
        parsed = urlparse(html.unescape(url))
        redirect_target = parse_qs(parsed.query).get("uddg", [""])[0]
        if redirect_target:
            url = unquote(redirect_target)
        title = titles[i][1] if i < len(titles) else ""
        results.append({
            "title": title,
            "content": snippet,
            "url": html.unescape(url),
        })
    return results


def _search_with_duckduckgo(query: str) -> str:
    """DuckDuckGo fallback search through the HTML endpoint."""
    import config

    _LAST_SEARCH_TRACE["provider"] = "DuckDuckGo"

    def call_duckduckgo() -> str:
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.post(
            url,
            data={"q": query},
            headers=headers,
            timeout=getattr(config, "WEB_SEARCH_TIMEOUT", 15),
        )
        resp.raise_for_status()
        return _format_search_results(_parse_duckduckgo_results(resp.text))

    try:
        result = _retry_call("DuckDuckGo", call_duckduckgo)
        _LAST_SEARCH_TRACE["provider"] = "DuckDuckGo"
        _LAST_SEARCH_TRACE["error"] = ""
        return result
    except Exception as e:
        _LAST_SEARCH_TRACE["error"] = str(e)
        logger.error("DuckDuckGo 搜索失败: %s", e)
        return f"网页搜索出错: {str(e)}"


@tool
def search_web(query: str) -> str:
    """在互联网上搜索最新信息。知识库没有相关信息或需要最新数据时使用。

    Args:
        query: 搜索查询语句
    """
    import config

    _reset_search_trace(query)
    result = _search_with_tavily(query)
    if result:
        return result

    if config.TAVILY_API_KEY and _LAST_SEARCH_TRACE.get("error"):
        _LAST_SEARCH_TRACE["fallback_used"] = True
        tavily_error = _LAST_SEARCH_TRACE.get("error", "")
        logger.info("Tavily 搜索失败，降级使用 DuckDuckGo")
        fallback = _search_with_duckduckgo(query)
        return f"Tavily 搜索失败（{tavily_error}），已切换到 DuckDuckGo。\n\n{fallback}"

    logger.info("Tavily API Key 未配置，降级使用 DuckDuckGo")
    _LAST_SEARCH_TRACE["fallback_used"] = True
    return _search_with_duckduckgo(query)


# ============== Python 代码执行工具 ==============

_BLOCKED_PATTERNS = [
    r"\bos\.system\b",
    r"\bos\.popen\b",
    r"\bsubprocess\b",
    r"\bsocket\b",
    r"\bhttp\.server\b",
    r"\bshutil\.rmtree\b",
    r"\bos\.remove\b",
    r"\bos\.unlink\b",
    r"\brmdir\b",
    r"\bopen\s*\(",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\b__import__\b",
]

_CODE_MAX_LENGTH = 2000
_OUTPUT_MAX_LENGTH = 5000


def _missing_module_hint(stderr: str) -> str:
    match = re.search(r"ModuleNotFoundError:\s+No module named ['\"]([^'\"]+)['\"]", stderr or "")
    if not match:
        return ""
    module_name = match.group(1)
    return (
        f"代码执行失败：当前运行环境未安装第三方库 `{module_name}`。"
        "请不要建议用户临时安装依赖，也不要继续使用该库。"
        "请改用 Python 标准库或项目已安装依赖重写代码后再试。"
    )


@tool
def execute_python_code(code: str) -> str:
    """执行 Python 代码并返回输出。用于数学计算、数据处理、格式转换等任务。

    Args:
        code: 要执行的 Python 代码字符串，不要包含 input() 等交互式调用
    """
    if len(code) > _CODE_MAX_LENGTH:
        return f"代码过长（{len(code)} 字符），最大允许 {_CODE_MAX_LENGTH} 字符。"

    for pattern in _BLOCKED_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return f"安全限制：代码中包含禁止的操作（匹配规则: {pattern}）。请使用安全的标准库函数。"

    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )

        output_parts = []
        if result.stdout:
            output_parts.append(f"输出:\n{result.stdout}")
        if result.stderr:
            missing_module_hint = _missing_module_hint(result.stderr)
            if missing_module_hint:
                return missing_module_hint
            output_parts.append(f"错误:\n{result.stderr}")
        if result.returncode != 0 and not output_parts:
            output_parts.append(f"进程退出码: {result.returncode}")

        output = "\n".join(output_parts) if output_parts else "代码执行完成（无输出）。"
        if len(output) > _OUTPUT_MAX_LENGTH:
            output = output[:_OUTPUT_MAX_LENGTH] + f"\n... (输出被截断，共 {len(output)} 字符)"

        return output
    except subprocess.TimeoutExpired:
        return "代码执行超时（限制 10 秒）。请简化代码或减少计算量。"
    except Exception as e:
        return f"代码执行出错: {str(e)}"


def create_tools(vector_store, collection_name: str = "default") -> list:
    """Create Agent tools in priority order."""
    kb_tool = create_knowledge_base_tool(vector_store, collection_name)
    return [kb_tool, search_web, execute_python_code]
