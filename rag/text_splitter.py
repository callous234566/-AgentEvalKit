"""
文本分块模块
使用MarkdownHeaderTextSplitter和RecursiveCharacterTextSplitter进行智能文本分块
修复：保留标题层级结构，增大重叠度，避免关键信息截断
"""

import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

import config

# 配置日志
logger = logging.getLogger(__name__)


class TextSplitter:
    """
    文本分块器类
    针对Markdown文档使用标题层级分割，其他文档使用递归字符分割
    关键修复：
    1. Markdown按标题分块，保留章节结构
    2. 增大重叠度到200，避免关键信息截断
    3. 优化分隔符优先级，优先在段落和标题处分割
    """

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        separators: List[str] = None,
    ):
        """
        初始化文本分块器

        Args:
            chunk_size: 每个块的最大字符数，默认从配置文件读取
            chunk_overlap: 块之间的重叠字符数，默认从配置文件读取
            separators: 分隔符列表，按优先级排序
        """
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP if chunk_overlap is None else chunk_overlap

        # 优化分隔符：优先在Markdown标题、段落之间分割
        self.separators = separators or [
            "\n## ",    # Markdown二级标题（最高优先级）
            "\n### ",   # Markdown三级标题
            "\n#### ",  # Markdown四级标题
            "\n\n",     # 段落
            "\n",       # 换行
            "。",       # 中文句号
            "．",       # 全角句点
            "！",       # 感叹号
            "？",       # 问号
            "；",       # 分号
            " ",        # 空格
            "",         # 字符级别
        ]

        # 创建递归分割器实例
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False,
        )

        # Markdown标题分割器
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header_1"),
                ("##", "header_2"),
                ("###", "header_3"),
            ]
        )

        logger.info(
            f"文本分块器初始化完成: chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        将文档列表分割成小块
        策略：Markdown文档先按标题分割，再递归分割；其他文档直接递归分割

        Args:
            documents: 原始文档列表

        Returns:
            List[Document]: 分割后的文档块列表
        """
        if not documents:
            logger.warning("输入文档列表为空，无需分块")
            return []

        try:
            all_chunks = []

            for doc in documents:
                file_type = doc.metadata.get("file_type", "")
                content = doc.page_content

                if file_type == ".md" and self._has_markdown_headers(content):
                    # Markdown文档：先按标题层级分割
                    chunks = self._split_markdown(doc)
                else:
                    # 其他文档：使用递归字符分割
                    chunks = self.recursive_splitter.split_documents([doc])

                all_chunks.extend(chunks)

            # 为每个分块添加序号信息
            for idx, doc in enumerate(all_chunks):
                doc.metadata["chunk_index"] = idx

            logger.info(f"文本分块完成: 原始 {len(documents)} 个文档 -> 分割为 {len(all_chunks)} 个块")

            # 打印分块统计
            chunk_info = self.get_chunk_info(all_chunks)
            logger.info(f"分块统计: {chunk_info}")

            return all_chunks

        except Exception as e:
            error_msg = f"文本分块失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def _has_markdown_headers(self, content: str) -> bool:
        """
        检查内容是否包含Markdown标题标记

        Args:
            content: 文本内容

        Returns:
            bool: 是否包含Markdown标题
        """
        import re
        return bool(re.search(r'^#{1,6}\s+', content, re.MULTILINE))

    def _split_markdown(self, document: Document) -> List[Document]:
        """
        按Markdown标题层级分割文档
        保留标题结构，使每个块都有明确的上下文
        修复：对于包含核心概念（如QKV、公式）的块，保持完整性不分割

        Args:
            document: 原始文档

        Returns:
            List[Document]: 分割后的文档块列表
        """
        try:
            # 使用MarkdownHeaderTextSplitter按标题分割
            header_chunks = self.markdown_splitter.split_text(document.page_content)

            # 如果标题分割后的块仍然太大，进行递归二次分割
            final_chunks = []
            for chunk in header_chunks:
                chunk_len = len(chunk.page_content)
                if chunk_len > self.chunk_size:
                    # 检查是否包含核心概念定义（如QKV、公式等），如果是则尽量保持完整
                    if self._contains_core_concept(chunk.page_content):
                        # 包含核心概念，作为大块保留，添加元数据标记
                        chunk.metadata.update(document.metadata)
                        chunk.metadata["is_core_concept"] = True
                        final_chunks.append(chunk)
                        logger.info(f"保留核心概念块: {chunk.metadata.get('header_2', '')[:30]}..., 长度={chunk_len}")
                    else:
                        # 普通内容，进行递归二次分割
                        sub_chunks = self.recursive_splitter.split_documents([chunk])
                        # 为子块添加标题上下文
                        for sub in sub_chunks:
                            header = chunk.metadata.get("header_2", "") or chunk.metadata.get("header_1", "")
                            if header:
                                sub.metadata["section_header"] = header
                            sub.metadata.update(document.metadata)
                        final_chunks.extend(sub_chunks)
                else:
                    # 块大小合适，保留标题元数据
                    chunk.metadata.update(document.metadata)
                    final_chunks.append(chunk)

            return final_chunks

        except Exception as e:
            logger.warning(f"Markdown标题分割失败，回退到递归分割: {e}")
            return self.recursive_splitter.split_documents([document])

    def _contains_core_concept(self, content: str) -> bool:
        """
        检查内容是否包含核心概念定义（如QKV、公式、算法步骤等）
        这类内容不应被分割，以保持语义完整性

        Args:
            content: 文本内容

        Returns:
            bool: 是否包含核心概念
        """
        import re

        # 核心概念标记：公式、关键定义、算法步骤等
        core_patterns = [
            r'[Qq]uery.*[Kk]ey.*[Vv]alue',  # QKV相关
            r'注意力.*机制',  # 注意力机制
            r'公式[:：]',  # 公式标记
            r'[Aa]ttention.*=.*[Ss]oftmax',  # Attention公式
            r'\\[.*?\\]',  # LaTeX公式
            r'```.*?```',  # 代码块
            r'算法[:：]',  # 算法标记
            r'步骤[:：]',  # 步骤标记
        ]

        for pattern in core_patterns:
            if re.search(pattern, content, re.DOTALL):
                return True

        return False

    def split_text(self, text: str) -> List[str]:
        """
        将纯文本分割成小块

        Args:
            text: 原始文本

        Returns:
            List[str]: 分割后的文本块列表
        """
        if not text or not text.strip():
            logger.warning("输入文本为空，无需分块")
            return []

        try:
            chunks = self.recursive_splitter.split_text(text)
            logger.info(f"文本分块完成: 分割为 {len(chunks)} 个块")
            return chunks

        except Exception as e:
            error_msg = f"文本分块失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def get_chunk_info(self, chunks: List[Document]) -> dict:
        """
        获取分块信息的统计

        Args:
            chunks: 分块后的文档列表

        Returns:
            dict: 统计信息
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0,
            }

        sizes = [len(chunk.page_content) for chunk in chunks]

        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": sum(sizes) // len(sizes),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes),
        }
