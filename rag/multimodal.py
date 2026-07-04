"""
Multimodal document helpers.

Images embedded in PDF/DOCX files are converted to short Chinese captions by
an OpenAI-compatible vision model. The captions are stored as normal
LangChain documents so the existing RAG pipeline can retrieve them.
"""

import base64
import logging
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict, List

import requests
from langchain_core.documents import Document
from PIL import Image, ImageOps

import config

logger = logging.getLogger(__name__)


def extract_image_documents(file_path: str, suffix: str) -> List[Document]:
    """Extract embedded images and return caption documents."""
    if not config.ENABLE_MULTIMODAL_PARSING or not config.check_api_key():
        return []

    path = Path(file_path)
    if suffix == ".pdf":
        images = _extract_pdf_images(path)
    elif suffix == ".docx":
        images = _extract_docx_images(path)
    else:
        return []

    if not images:
        return []

    documents = []
    for image_index, image_info in enumerate(images[: config.MULTIMODAL_MAX_IMAGES_PER_FILE], 1):
        image_bytes = image_info.get("data") or b""
        if len(image_bytes) < config.MULTIMODAL_IMAGE_MIN_BYTES:
            continue

        data_url = _prepare_image_data_url(image_bytes)
        if not data_url:
            continue

        caption = _caption_image(path.name, image_info, data_url)
        if not caption:
            continue

        page_text = f"第{image_info['page']}页" if image_info.get("page") else "文档内"
        content = (
            f"【图片解析】{path.name} {page_text} 图片{image_index}：\n"
            f"{caption}"
        )
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": path.name,
                    "file_path": str(path.absolute()),
                    "file_type": suffix,
                    "modality": "image",
                    "page": image_info.get("page"),
                    "image_index": image_index,
                    "image_name": image_info.get("name", ""),
                },
            )
        )

    if documents:
        logger.info(f"多模态图片解析完成: {path.name}, 图片片段={len(documents)}")
    return documents


def _extract_pdf_images(path: Path) -> List[Dict]:
    images = []
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        for page_index, page in enumerate(reader.pages, 1):
            for image_index, image in enumerate(getattr(page, "images", []) or [], 1):
                data = getattr(image, "data", None)
                if not data:
                    continue
                images.append({
                    "data": data,
                    "page": page_index,
                    "name": getattr(image, "name", f"page-{page_index}-image-{image_index}"),
                })
    except Exception as e:
        logger.warning(f"PDF 图片提取失败 [{path.name}]: {e}")
    return images


def _extract_docx_images(path: Path) -> List[Dict]:
    images = []
    try:
        with zipfile.ZipFile(path) as archive:
            media_names = [
                name for name in archive.namelist()
                if name.startswith("word/media/") and not name.endswith("/")
            ]
            for image_index, name in enumerate(media_names, 1):
                images.append({
                    "data": archive.read(name),
                    "page": None,
                    "name": Path(name).name or f"image-{image_index}",
                })
    except Exception as e:
        logger.warning(f"Word 图片提取失败 [{path.name}]: {e}")
    return images


def _prepare_image_data_url(image_bytes: bytes) -> str:
    try:
        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)
        image.thumbnail(
            (config.MULTIMODAL_IMAGE_MAX_SIDE, config.MULTIMODAL_IMAGE_MAX_SIDE)
        )

        if image.mode in {"RGBA", "LA", "P"}:
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            alpha = image.getchannel("A") if image.mode in {"RGBA", "LA"} else None
            background.paste(image.convert("RGB"), mask=alpha)
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=85, optimize=True)
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{encoded}"
    except Exception as e:
        logger.warning(f"图片转换失败，跳过该图片: {e}")
        return ""


def _caption_image(file_name: str, image_info: Dict, data_url: str) -> str:
    page_text = f"第{image_info['page']}页" if image_info.get("page") else "文档内"
    prompt = (
        "请用中文解析这张文档图片，提取对知识库问答有价值的信息。"
        "如果图片包含流程图、表格、截图、公式或代码，请说明关键文字、结构和结论。"
        "不要编造看不见的内容，控制在 300 字以内。\n\n"
        f"文件：{file_name}\n位置：{page_text}\n图片名：{image_info.get('name', '')}"
    )
    payload = {
        "model": config.MULTIMODAL_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        "temperature": 0.1,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {config.LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    url = f"{config.MULTIMODAL_API_BASE.rstrip('/')}/chat/completions"

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=config.MULTIMODAL_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        message = (data.get("choices") or [{}])[0].get("message") or {}
        content = message.get("content") or ""
        return str(content).strip()
    except Exception as e:
        logger.warning(f"多模态图片解析失败 [{file_name}]: {e}")
        return ""
