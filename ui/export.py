"""Export functions: PDF, Markdown, plain text."""

import re
import time

from ui.text_utils import _normalize_message_text, get_source_display_name


def build_conversation_markdown(session_name: str, messages: list) -> str:
    """Build a clean Markdown export for a conversation."""
    lines = [
        f"# {session_name or '未命名会话'}",
        "",
        f"> 导出时间：{time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    for idx, msg in enumerate(messages, 1):
        role = "用户" if msg.get("role") == "user" else "AI"
        lines.append(f"## {idx}. {role}")
        lines.append("")
        lines.append(_normalize_message_text(msg.get("content", "")))
        sources = msg.get("sources") or []
        if sources:
            lines.append("")
            lines.append("### 引用来源")
            for source in sources:
                name = get_source_display_name(source)
                content = _normalize_message_text(source.get("content", ""))
                score = source.get("score", 0)
                lines.append(f"- **{name}**（相似度：{score:.2f}）：{content}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_conversation_plain_text(session_name: str, messages: list) -> str:
    """Build a plain-text export for sharing."""
    lines = [session_name or "未命名会话", f"导出时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    for idx, msg in enumerate(messages, 1):
        role = "用户" if msg.get("role") == "user" else "AI"
        lines.append(f"{idx}. {role}")
        lines.append(_normalize_message_text(msg.get("content", "")))
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_conversation_pdf(markdown_text: str) -> bytes:
    """使用内置 PDF 语法生成简易 PDF，避免新增依赖。"""
    text = re.sub(r"^#{1,6}\s*", "", markdown_text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = text.replace("`", "")

    wrapped_lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            wrapped_lines.append("")
            continue
        while len(line) > 42:
            wrapped_lines.append(line[:42])
            line = line[42:]
        wrapped_lines.append(line)

    lines_per_page = 42
    pages = [
        wrapped_lines[start:start + lines_per_page]
        for start in range(0, len(wrapped_lines), lines_per_page)
    ] or [[]]

    objects = []

    def add_object(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    catalog_id = add_object(b"")
    pages_id = add_object(b"")
    font_descriptor_id = add_object(
        b"<< /Type /FontDescriptor /FontName /STSong-Light /Flags 4 "
        b"/FontBBox [0 -200 1000 900] /ItalicAngle 0 /Ascent 880 /Descent -120 /CapHeight 700 /StemV 80 >>"
    )
    cid_font_id = add_object(
        f"<< /Type /Font /Subtype /CIDFontType0 /BaseFont /STSong-Light "
        f"/CIDSystemInfo << /Registry (Adobe) /Ordering (GB1) /Supplement 2 >> "
        f"/FontDescriptor {font_descriptor_id} 0 R /DW 1000 >>".encode("ascii")
    )
    font_id = add_object(
        f"<< /Type /Font /Subtype /Type0 /BaseFont /STSong-Light "
        f"/Encoding /UniGB-UCS2-H /DescendantFonts [{cid_font_id} 0 R] >>".encode("ascii")
    )

    page_ids = []
    for page_lines in pages:
        commands = ["BT", "/F1 11 Tf", "50 790 Td", "16 TL"]
        for line in page_lines:
            encoded = line.encode("utf-16-be").hex().upper()
            commands.append(f"<{encoded}> Tj")
            commands.append("T*")
        commands.append("ET")
        stream = "\n".join(commands).encode("ascii")
        content_id = add_object(
            b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
        )
        page_id = add_object(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>".encode("ascii")
        )
        page_ids.append(page_id)

    objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii")
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for idx, body in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode("ascii"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(pdf)


def get_safe_export_name(name: str) -> str:
    """Return a filesystem-safe export filename stem."""
    return re.sub(r"[\\/:*?\"<>|]+", "_", name or "conversation")[:40] or "conversation"
