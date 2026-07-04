"""
文档解析模块
支持PDF、TXT、DOCX、Markdown格式的文档解析
修复：Markdown使用原生文本解析，避免HTML标签污染
"""

import logging
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document

import config
from .multimodal import extract_image_documents

# 配置日志
logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    文档加载器类
    根据文件类型自动选择对应的解析方式
    关键修复：Markdown/TXT直接读取纯文本，避免任何HTML转换
    """

    # 支持的文件扩展名与加载器映射
    SUPPORTED_LOADERS = {
        ".pdf": "PyPDFLoader",
        ".txt": "TextLoader",
        ".docx": "Docx2txtLoader",
        ".md": "RawTextLoader",  # Markdown使用原生文本读取
    }

    def __init__(self):
        """初始化文档加载器"""
        self.errors: List[str] = []

    def load_document(self, file_path: str, enable_multimodal: Optional[bool] = None) -> List[Document]:
        """
        加载单个文档

        Args:
            file_path: 文档路径

        Returns:
            List[Document]: 解析后的文档片段列表

        Raises:
            ValueError: 不支持的文件格式
            FileNotFoundError: 文件不存在
        """
        path = Path(file_path)

        # 检查文件是否存在
        if not path.exists():
            error_msg = f"文件不存在: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # 检查文件大小
        file_size = path.stat().st_size
        max_size = 20 * 1024 * 1024  # 20MB
        if file_size > max_size:
            error_msg = f"文件过大 ({file_size / 1024 / 1024:.1f}MB > 20MB): {file_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 获取文件扩展名
        suffix = path.suffix.lower()

        # 检查是否支持该格式
        if suffix not in self.SUPPORTED_LOADERS:
            error_msg = f"不支持的文件格式 '{suffix}'，仅支持: {list(self.SUPPORTED_LOADERS.keys())}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            documents = self._load_by_type(file_path, suffix)
            use_multimodal = (
                config.ENABLE_MULTIMODAL_PARSING
                if enable_multimodal is None
                else enable_multimodal
            )
            if use_multimodal:
                documents.extend(extract_image_documents(file_path, suffix))
            # 为每个文档添加元数据
            for doc in documents:
                doc.metadata.update({
                    "source": path.name,
                    "file_path": str(path.absolute()),
                    "file_type": suffix,
                })
            logger.info(f"成功加载文档: {path.name}, 共 {len(documents)} 页/段")
            return documents

        except Exception as e:
            error_msg = f"解析文档失败 [{path.name}]: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            raise RuntimeError(error_msg) from e

    def _load_by_type(self, file_path: str, suffix: str) -> List[Document]:
        """
        根据文件类型选择对应的加载器

        Args:
            file_path: 文件路径
            suffix: 文件扩展名

        Returns:
            List[Document]: 解析后的文档列表
        """
        if suffix == ".pdf":
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(file_path)
            return loader.load()

        elif suffix == ".txt" or suffix == ".md":
            # 关键修复：直接读取原始文本，不使用任何转换
            return self._load_raw_text(file_path)

        elif suffix == ".docx":
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(file_path)
            return loader.load()

        else:
            # 理论上不会到达这里，因为前面已经检查了扩展名
            raise ValueError(f"未实现该格式的解析器: {suffix}")

    def _load_raw_text(self, file_path: str) -> List[Document]:
        """
        直接读取文本文件的原始内容
        避免使用任何可能引入HTML标签的转换器

        Args:
            file_path: 文本文件路径

        Returns:
            List[Document]: 包含原始文本的文档列表
        """
        path = Path(file_path)

        # 尝试多种编码读取
        encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312", "latin-1"]
        content = None
        used_encoding = None

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                used_encoding = encoding
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError(f"无法解码文件，尝试了以下编码: {encodings}")

        # 清理BOM头
        if content.startswith("\ufeff"):
            content = content[1:]

        # 基本清理：移除多余的空行，但保留Markdown结构
        lines = content.split("\n")
        cleaned_lines = []
        prev_empty = False

        for line in lines:
            stripped = line.strip()
            # 保留Markdown标题、列表等结构标记
            if stripped == "":
                if not prev_empty:
                    cleaned_lines.append("")
                    prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False

        cleaned_content = "\n".join(cleaned_lines).strip()

        logger.info(f"原生文本加载完成: {path.name}, 编码={used_encoding}, 长度={len(cleaned_content)}")

        return [Document(
            page_content=cleaned_content,
            metadata={
                "source": path.name,
                "file_path": str(path.absolute()),
                "encoding": used_encoding,
            }
        )]

    def load_documents(self, file_paths: List[str], enable_multimodal: Optional[bool] = None) -> List[Document]:
        """
        批量加载多个文档

        Args:
            file_paths: 文档路径列表

        Returns:
            List[Document]: 所有文档的片段列表
        """
        all_documents = []
        self.errors = []

        for file_path in file_paths:
            try:
                docs = self.load_document(file_path, enable_multimodal=enable_multimodal)
                all_documents.extend(docs)
            except Exception as e:
                # 记录错误但继续处理其他文件
                logger.warning(f"跳过文件 [{file_path}]: {str(e)}")
                continue

        logger.info(f"批量加载完成: 成功 {len(file_paths) - len(self.errors)} 个, 失败 {len(self.errors)} 个")
        return all_documents

    def get_errors(self) -> List[str]:
        """
        获取加载过程中的错误信息

        Returns:
            List[str]: 错误信息列表
        """
        return self.errors

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        检查文件是否支持解析

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否支持
        """
        suffix = Path(file_path).suffix.lower()
        return suffix in DocumentLoader.SUPPORTED_LOADERS
