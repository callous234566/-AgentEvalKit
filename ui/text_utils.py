"""Text processing and formatting utility functions."""

import base64
import html
import re
from pathlib import Path


def _normalize_message_text(text: str) -> str:
    """清理展示层不应暴露的 HTML 包装、异常空行和孤立标点。"""
    cleaned = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    cleaned = cleaned.replace("\ufeff", "").replace("\u200b", "")

    # 兼容旧页面曾把气泡 HTML 当正文显示的情况，避免用户看到实现标签。
    cleaned = re.sub(
        r"<button\b[^>]*answer-(?:copy|regenerate)-btn[^>]*>.*?</button>",
        "",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"</?div\b[^>]*class=[\"'][^\"']*(?:message-content|answer-actions|ai-message|message-row|avatar)[^\"']*[\"'][^>]*>",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"(?im)^\s*</div>\s*$", "", cleaned)

    lines = []
    in_code = False
    for raw_line in cleaned.split("\n"):
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            lines.append(stripped)
            continue
        if not in_code and re.fullmatch(r"[、，,。.;；:：!！?？`\"'“”‘’\-_\s]+", stripped or ""):
            continue
        lines.append(line)

    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def _plain_text_to_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def _message_text_to_html(text: str) -> str:
    """转义消息内容，去掉代码围栏标记并把代码块渲染成普通代码框。"""
    cleaned = _normalize_message_text(text)
    if not cleaned:
        return ""

    parts = []
    position = 0
    fence_pattern = re.compile(r"```([A-Za-z0-9_+\-.]*)[ \t]*\n([\s\S]*?)\n?```")

    for match in fence_pattern.finditer(cleaned):
        parts.append(_plain_text_to_html(cleaned[position:match.start()]))
        code = match.group(2).strip("\n")
        parts.append(
            f'<pre class="message-code"><code>{html.escape(code)}</code></pre>'
        )
        position = match.end()

    parts.append(_plain_text_to_html(cleaned[position:]))
    return "".join(parts)


def _copy_payload(text: str) -> str:
    """把复制内容编码到 HTML 属性中，避免引号和换行破坏结构。"""
    return base64.b64encode(_normalize_message_text(text).encode("utf-8")).decode("ascii")


def get_source_display_name(source: dict) -> str:
    """从不同后端字段中提取用户可见文档名。"""
    for key in ("source", "file_name", "filename", "document", "doc_name", "title"):
        value = source.get(key)
        if value:
            return Path(str(value)).name

    metadata = source.get("metadata") or {}
    if isinstance(metadata, dict):
        for key in ("source", "file_name", "filename", "document", "doc_name", "title"):
            value = metadata.get(key)
            if value:
                return Path(str(value)).name

    return "未知文档"


def format_file_size(size: int) -> str:
    """格式化文件大小。"""
    try:
        size = int(size or 0)
    except (TypeError, ValueError):
        size = 0
    if size <= 0:
        return "未知大小"
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"
