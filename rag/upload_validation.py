"""
上传文件内容校验工具。
用于在文档解析前识别明显伪装或二进制污染的文件。
"""

import logging
from pathlib import Path
from typing import Optional

import config

logger = logging.getLogger(__name__)


def validate_uploaded_file_content(temp_path: str, suffix: str, content_type: Optional[str] = None) -> None:
    """Validate uploaded file content against the claimed extension."""
    path = Path(temp_path)
    with open(path, "rb") as f:
        head = f.read(4096)

    if not head:
        raise ValueError("上传文件为空")

    if suffix == ".pdf":
        if not head.startswith(b"%PDF-"):
            raise ValueError("文件内容不是有效的 PDF 文档")
    elif suffix == ".docx":
        if not head.startswith(b"PK\x03\x04"):
            raise ValueError("文件内容不是有效的 DOCX 文档")
    elif suffix in {".txt", ".md"}:
        if b"\x00" in head:
            raise ValueError("文本文件包含二进制内容")
        control_bytes = sum(
            1
            for byte in head
            if byte < 32 and byte not in (9, 10, 13)
        )
        if control_bytes / max(len(head), 1) > 0.05:
            raise ValueError("文本文件疑似为二进制内容")

    expected_mimes = config.SUPPORTED_MIME_TYPES.get(suffix, set())
    normalized_type = (content_type or "").split(";", 1)[0].strip().lower()
    if normalized_type and expected_mimes and normalized_type not in expected_mimes:
        logger.warning(
            "上传文件 MIME 与扩展名不完全匹配: filename=%s, suffix=%s, content_type=%s",
            path.name,
            suffix,
            normalized_type,
        )
