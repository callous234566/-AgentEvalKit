"""
FastAPI后端入口
提供文档上传、知识库管理、问答等RESTful API
"""

import asyncio
import logging
import os
import re
import shutil
import tempfile
import threading
import time
import uuid
from collections import OrderedDict
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_core.documents import Document
from pydantic import BaseModel, Field

import config
from rag.document_loader import DocumentLoader
from rag.logging_utils import reset_request_id, set_request_id, setup_logging
from rag.qa_chain import QAChain
from rag.text_splitter import TextSplitter
from rag.upload_validation import validate_uploaded_file_content
from rag.vector_store import VectorStoreManager

# 配置日志
setup_logging()
logger = logging.getLogger(__name__)

# 捕获未处理的异常，防止服务崩溃
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


def log_api_key_status() -> None:
    """Log API key availability during application startup."""
    if not config.check_api_key():
        logger.warning("模型 API 密钥未配置，请在 .env 文件中设置 LLM_API_KEY")
    else:
        logger.info("模型 API 密钥已配置")


async def preload_embedding_model() -> None:
    """Preload the embedding model to reduce first request latency."""
    try:
        from rag.vector_store import get_embedding_model
        logger.info("正在预加载 Embedding 模型...")
        get_embedding_model()
        logger.info("Embedding 模型预加载完成")
    except Exception as e:
        logger.error(f"Embedding 模型预加载失败: {e}")
        logger.error("首次请求可能会较慢，请耐心等待")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan hook replacing deprecated startup events."""
    log_api_key_status()
    await preload_embedding_model()
    yield

# 创建FastAPI应用
app = FastAPI(
    title="个人RAG知识库助手",
    description="基于 SiliconFlow 和 LangChain 的个人知识库问答系统",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置CORS，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}


@app.middleware("http")
async def verify_api_token(request: Request, call_next):
    """当配置 API_TOKEN 时，对非公开接口启用简单访问保护。"""
    if request.method == "OPTIONS" or request.url.path in PUBLIC_PATHS or not config.API_TOKEN:
        return await call_next(request)

    token = request.headers.get("X-API-Token", "").strip()
    authorization = request.headers.get("Authorization", "").strip()
    if authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    if token != config.API_TOKEN:
        return JSONResponse(
            status_code=401,
            content={"detail": "未授权访问，请配置有效 API_TOKEN"},
        )

    return await call_next(request)


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    """Attach request id, timing headers, and structured request logs."""
    started_at = time.perf_counter()
    request_id = request.headers.get("X-Request-ID", "").strip() or uuid.uuid4().hex
    request.state.request_id = request_id
    request_id_token = set_request_id(request_id)

    try:
        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            logger.exception(
                "request_failed request_id=%s method=%s path=%s elapsed_ms=%s error=%s",
                request_id,
                request.method,
                request.url.path,
                elapsed_ms,
                exc,
            )
            response = JSONResponse(
                status_code=500,
                content={"detail": "服务器内部错误，请稍后重试", "request_id": request_id},
            )

        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(elapsed_ms)
        logger.info(
            "request_completed request_id=%s method=%s path=%s status=%s elapsed_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
    finally:
        reset_request_id(request_id_token)


def _get_request_id(request: Request) -> str:
    """Return the request id assigned by middleware, if available."""
    return str(getattr(request.state, "request_id", "") or "")


def _log_endpoint_exception(
    operation: str,
    request: Request,
    error: Exception,
    **context,
) -> None:
    """Log endpoint failures with request id and compact non-sensitive context."""
    context_text = " ".join(
        f"{key}={value!r}"
        for key, value in context.items()
        if value is not None
    )
    if context_text:
        context_text = f" {context_text}"
    logger.exception(
        "endpoint_failed request_id=%s operation=%s%s error=%s",
        _get_request_id(request),
        operation,
        context_text,
        error,
    )


# 全局组件实例
vector_store = VectorStoreManager()
document_loader = DocumentLoader()
text_splitter = TextSplitter()
_qa_chain_cache: OrderedDict[tuple, QAChain] = OrderedDict()
_QA_CHAIN_CACHE_MAX_SIZE = 16
_cache_lock = threading.Lock()

# LLM 客户端缓存（按 temperature 复用）
_llm_clients: dict = {}
_llm_lock = threading.Lock()


def _get_llm(temperature: float):
    """获取或创建指定 temperature 的 LLM 客户端（线程安全单例）。"""
    if temperature in _llm_clients:
        return _llm_clients[temperature]
    with _llm_lock:
        if temperature in _llm_clients:
            return _llm_clients[temperature]
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            api_key=config.LLM_API_KEY,
            model=config.LLM_MODEL,
            base_url=config.LLM_API_BASE,
            temperature=temperature,
            max_tokens=config.LLM_MAX_TOKENS,
        )
        _llm_clients[temperature] = llm
        return llm

# ============== Pydantic模型 ==============

class ChatMessage(BaseModel):
    """多轮对话历史消息"""
    role: str
    content: str


class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    sources: List[str] = Field(..., min_length=1)


class ToggleEnabledRequest(BaseModel):
    """启用/禁用文档请求"""
    source: str
    enabled: bool


class QuestionRequest(BaseModel):
    """问答请求模型"""
    question: str
    collection_name: str = "default"
    chat_history: List[ChatMessage] = Field(default_factory=list)
    top_k: Optional[int] = Field(default=None, ge=1, le=20)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    enable_query_rewrite: Optional[bool] = None
    enable_contextual_compression: Optional[bool] = None


class QuestionResponse(BaseModel):
    """问答响应模型"""
    question: str
    answer: str
    sources: List[dict]
    success: bool
    error: Optional[str] = None


class RetrievedDocument(BaseModel):
    """检索到的文档片段"""
    content: str
    metadata: dict = Field(default_factory=dict)


class RetrieveResponse(BaseModel):
    """检索响应模型"""
    question: str
    retrieval_query: str
    resolved_question: str
    documents: List[RetrievedDocument]
    sources: List[dict]
    retrieved_count: int
    selected_count: int
    trace: dict = Field(default_factory=dict)
    success: bool
    error: Optional[str] = None


class GenerateRequest(BaseModel):
    """基于已检索片段生成回答的请求模型"""
    question: str
    collection_name: str = "default"
    chat_history: List[ChatMessage] = Field(default_factory=list)
    documents: List[RetrievedDocument] = Field(default_factory=list)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)


class AgentRequest(BaseModel):
    """Agent 请求模型"""
    question: str
    collection_name: str = "default"
    chat_history: List[ChatMessage] = Field(default_factory=list)
    debug: Optional[bool] = None


class AgentResponse(BaseModel):
    """Agent 响应模型"""
    question: str
    answer: str
    agent_steps: List[dict] = Field(default_factory=list)
    debug_info: dict = Field(default_factory=dict)
    success: bool
    error: Optional[str] = None


class RenameCollectionRequest(BaseModel):
    """知识库重命名请求"""
    new_name: str = Field(..., min_length=1, max_length=80)


class CollectionInfo(BaseModel):
    """知识库信息模型"""
    collection_name: str
    document_count: int


class UploadResponse(BaseModel):
    """上传响应模型"""
    success: bool
    message: str
    collection_name: str
    chunks_added: int
    errors: List[str] = []


def qa_chain_document_from_payload(document: RetrievedDocument) -> Document:
    """将 API 文档片段载荷转换为 LangChain Document。"""
    return Document(
        page_content=document.content,
        metadata=document.metadata or {},
    )


def _agent_should_fallback_to_rag(result: dict) -> bool:
    """Return whether a failed Agent result can safely fall back to regular RAG."""
    if result.get("success", False):
        return False
    debug_info = result.get("debug_info") or {}
    tool_policy = debug_info.get("tool_policy") or {}
    routing_decision = debug_info.get("routing_decision") or {}
    category = tool_policy.get("category") or routing_decision.get("category")
    return category == "local_knowledge"


def get_qa_chain(
    collection_name: str,
    top_k: Optional[int] = None,
    temperature: Optional[float] = None,
    enable_query_rewrite: Optional[bool] = None,
    enable_contextual_compression: Optional[bool] = None,
) -> QAChain:
    """Reuse QAChain instances for identical runtime settings."""
    resolved_temp = temperature if temperature is not None else config.LLM_TEMPERATURE
    cache_key = (
        collection_name,
        top_k if top_k is not None else config.RETRIEVER_TOP_K,
        resolved_temp,
        enable_query_rewrite if enable_query_rewrite is not None else config.ENABLE_QUERY_REWRITE,
        enable_contextual_compression
        if enable_contextual_compression is not None
        else config.ENABLE_CONTEXTUAL_COMPRESSION,
    )

    with _cache_lock:
        cached = _qa_chain_cache.get(cache_key)
        if cached is not None:
            _qa_chain_cache.move_to_end(cache_key)
            return cached

    qa_chain = QAChain(
        collection_name=collection_name,
        top_k=top_k,
        temperature=temperature,
        enable_query_rewrite=enable_query_rewrite,
        enable_contextual_compression=enable_contextual_compression,
        vector_store=vector_store,
        llm=_get_llm(resolved_temp),
    )
    with _cache_lock:
        _qa_chain_cache[cache_key] = qa_chain
        _qa_chain_cache.move_to_end(cache_key)
        while len(_qa_chain_cache) > _QA_CHAIN_CACHE_MAX_SIZE:
            _qa_chain_cache.popitem(last=False)
    logger.info(f"QAChain 缓存新增: collection={collection_name}, cache_size={len(_qa_chain_cache)}")
    return qa_chain


def sanitize_upload_filename(filename: str) -> str:
    """Return a safe basename for a user-uploaded file."""
    raw_name = str(filename or "").strip()
    name = PureWindowsPath(PurePosixPath(raw_name).name).name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="文件名为空")
    safe_name = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", name)
    safe_name = safe_name.strip("._ ")
    if not safe_name or "." not in safe_name:
        raise HTTPException(status_code=400, detail="文件名为空")
    return safe_name


def save_upload_to_temp(file: UploadFile, temp_dir: str, safe_filename: str) -> tuple[str, int]:
    """Save upload in chunks and stop once it exceeds the configured limit."""
    temp_path = os.path.join(temp_dir, safe_filename)
    file_size = 0
    chunk_size = 1024 * 1024

    with open(temp_path, "wb") as target:
        while True:
            chunk = file.file.read(chunk_size)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > config.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"文件过大 ({file_size / 1024 / 1024:.1f}MB > {config.MAX_UPLOAD_SIZE / 1024 / 1024:.0f}MB)",
                )
            target.write(chunk)

    return temp_path, file_size


# ============== API路由 ==============

@app.get("/")
async def root():
    """根路径，返回服务状态"""
    return {
        "status": "running",
        "service": "个人RAG知识库助手",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "api_key_configured": config.check_api_key(),
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    collection_name: str = Form("default"),
    chunk_size: Optional[int] = Form(None),
    chunk_overlap: Optional[int] = Form(None),
    enable_multimodal: Optional[bool] = Form(None),
):
    """
    上传文档并添加到知识库

    Args:
        file: 上传的文件
        collection_name: 目标知识库名称

    Returns:
        UploadResponse: 上传结果
    """
    logger.info(f"收到上传请求: {file.filename} -> 知识库 '{collection_name}'")

    # 检查API密钥
    if not config.check_api_key():
        raise HTTPException(status_code=500, detail="模型 API 密钥未配置")

    # 检查文件是否为空
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    safe_filename = sanitize_upload_filename(file.filename)

    # 检查文件格式
    suffix = Path(safe_filename).suffix.lower()
    if suffix not in config.SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式 '{suffix}'，仅支持: {list(config.SUPPORTED_EXTENSIONS.keys())}",
        )

    # 创建临时文件保存上传内容
    temp_dir = tempfile.mkdtemp(prefix="rag_upload_")

    try:
        temp_path, file_size = save_upload_to_temp(file, temp_dir, safe_filename)
        try:
            validate_uploaded_file_content(temp_path, suffix, file.content_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

        # 1. 加载文档
        documents = await asyncio.to_thread(
            document_loader.load_document,
            temp_path,
            enable_multimodal=enable_multimodal,
        )
        upload_time = datetime.now().isoformat(timespec="seconds")
        for doc in documents:
            doc.metadata.update({
                "file_size": file_size,
                "upload_time": upload_time,
                "original_filename": file.filename,
                "safe_filename": safe_filename,
                "enabled": True,
            })

        # 2. 文本分块
        splitter = TextSplitter(
            chunk_size=chunk_size or config.CHUNK_SIZE,
            chunk_overlap=chunk_overlap if chunk_overlap is not None else config.CHUNK_OVERLAP,
        )
        chunks = await asyncio.to_thread(splitter.split_documents, documents)

        if not chunks:
            empty_message = "文档解析后内容为空，未添加任何内容"
            if suffix == ".pdf":
                empty_message = (
                    "未从 PDF 中提取到可入库文本。该文件可能是扫描版/图片型 PDF；"
                    "如需解析图片内容，请确认多模态模型权限可用，或上传可复制文本/OCR 后的版本。"
                )
            return UploadResponse(
                success=False,
                message=empty_message,
                collection_name=collection_name,
                chunks_added=0,
            )

        # 3. 添加到向量库
        chunks_added = await asyncio.to_thread(vector_store.add_documents, chunks, collection_name)

        # 获取分块统计信息
        chunk_info = splitter.get_chunk_info(chunks)

        return UploadResponse(
            success=True,
            message=f"文档上传成功！解析为 {chunks_added} 个文本块",
            collection_name=collection_name,
            chunks_added=chunks_added,
            errors=document_loader.get_errors(),
        )

    except HTTPException:
        raise
    except Exception as e:
        _log_endpoint_exception(
            "upload_document",
            request,
            e,
            collection_name=collection_name,
            filename=safe_filename if "safe_filename" in locals() else file.filename,
        )
        raise HTTPException(status_code=500, detail=f"文档处理失败: {str(e)}")

    finally:
        # 清理临时文件
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest, http_request: Request):
    """
    知识库问答

    Args:
        request: 问答请求

    Returns:
        QuestionResponse: 问答结果
    """
    logger.info(f"收到问答请求: '{request.question[:50]}...' -> 知识库 '{request.collection_name}'")

    # 检查API密钥
    if not config.check_api_key():
        raise HTTPException(status_code=500, detail="模型 API 密钥未配置")

    # 检查问题是否为空
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        # 创建或复用问答链并执行问答
        qa_chain = get_qa_chain(
            collection_name=request.collection_name,
            top_k=request.top_k,
            temperature=request.temperature,
            enable_query_rewrite=request.enable_query_rewrite,
            enable_contextual_compression=request.enable_contextual_compression,
        )
        result = await asyncio.to_thread(
            qa_chain.ask,
            request.question,
            chat_history=[msg.model_dump() for msg in request.chat_history],
        )

        return QuestionResponse(**result)

    except Exception as e:
        _log_endpoint_exception(
            "ask_question",
            http_request,
            e,
            collection_name=request.collection_name,
        )
        raise HTTPException(status_code=500, detail=f"问答失败: {str(e)}")


@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(request: QuestionRequest, http_request: Request):
    """
    检索知识库并返回重排序后的相关片段，用于前端展示真实执行步骤。
    """
    logger.info(f"收到检索请求: '{request.question[:50]}...' -> 知识库 '{request.collection_name}'")

    if not config.check_api_key():
        raise HTTPException(status_code=500, detail="模型 API 密钥未配置")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        qa_chain = get_qa_chain(
            collection_name=request.collection_name,
            top_k=request.top_k,
            temperature=request.temperature,
            enable_query_rewrite=request.enable_query_rewrite,
            enable_contextual_compression=request.enable_contextual_compression,
        )
        result = await asyncio.to_thread(
            qa_chain.retrieve,
            request.question,
            chat_history=[msg.model_dump() for msg in request.chat_history],
        )
        return RetrieveResponse(**result)
    except Exception as e:
        _log_endpoint_exception(
            "retrieve_documents",
            http_request,
            e,
            collection_name=request.collection_name,
        )
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")


@app.post("/generate", response_model=QuestionResponse)
async def generate_answer(request: GenerateRequest, http_request: Request):
    """
    使用已经检索出的文档片段生成最终回答，用于前端分步可视化。
    """
    logger.info(f"收到生成请求: '{request.question[:50]}...' -> 知识库 '{request.collection_name}'")

    if not config.check_api_key():
        raise HTTPException(status_code=500, detail="模型 API 密钥未配置")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        qa_chain = get_qa_chain(
            collection_name=request.collection_name,
            temperature=request.temperature,
        )
        result = await asyncio.to_thread(
            qa_chain.generate_from_documents,
            question=request.question,
            documents=[
                qa_chain_document_from_payload(doc)
                for doc in request.documents
            ],
            chat_history=[msg.model_dump() for msg in request.chat_history],
        )
        return QuestionResponse(**result)
    except Exception as e:
        _log_endpoint_exception(
            "generate_answer",
            http_request,
            e,
            collection_name=request.collection_name,
        )
        raise HTTPException(status_code=500, detail=f"回答生成失败: {str(e)}")


@app.post("/agent", response_model=AgentResponse)
async def agent_query(request: AgentRequest, http_request: Request):
    """
    Agent 模式问答：自主选择工具（知识库检索、网页搜索、代码执行）来回答问题。
    """
    logger.info(f"收到 Agent 请求: '{request.question[:50]}...' -> 知识库 '{request.collection_name}'")

    if not config.check_api_key():
        raise HTTPException(status_code=500, detail="模型 API 密钥未配置")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    if not config.AGENT_ENABLED:
        raise HTTPException(status_code=400, detail="Agent 模式未启用，请在配置中设置 AGENT_ENABLED=true")

    try:
        from rag.tools import create_tools
        from rag.agent import create_agent, run_agent

        tools = create_tools(vector_store, request.collection_name)
        llm = _get_llm(config.AGENT_TEMPERATURE)
        executor = create_agent(llm, tools)

        result = await asyncio.to_thread(
            run_agent,
            executor,
            request.question,
            [msg.model_dump() for msg in request.chat_history],
            request.debug,
        )

        if _agent_should_fallback_to_rag(result):
            debug_info = result.get("debug_info") or {}
            debug_info["fallback_reason"] = debug_info.get("fallback_reason") or "agent_local_failure"
            debug_info["fallback_used"] = "rag_qa"
            logger.warning(
                "agent_fallback_to_rag request_id=%s collection_name=%s reason=%s",
                _get_request_id(http_request),
                request.collection_name,
                debug_info.get("fallback_reason"),
            )
            qa_chain = get_qa_chain(collection_name=request.collection_name)
            fallback = await asyncio.to_thread(
                qa_chain.ask,
                request.question,
                chat_history=[msg.model_dump() for msg in request.chat_history],
            )
            debug_info["fallback_sources"] = fallback.get("sources", [])
            result = {
                "success": bool(fallback.get("success", False)),
                "answer": fallback.get("answer", ""),
                "agent_steps": result.get("agent_steps", []) + [{
                    "tool": "fallback_rag",
                    "input": request.question[:200],
                    "output": fallback.get("answer", "")[:500],
                }],
                "debug_info": debug_info,
                "error": None if fallback.get("success", False) else fallback.get("error") or result.get("error"),
            }

        return AgentResponse(
            question=request.question,
            answer=result.get("answer", ""),
            agent_steps=result.get("agent_steps", []),
            debug_info=result.get("debug_info", {}),
            success=result.get("success", False),
            error=result.get("error"),
        )
    except Exception as e:
        _log_endpoint_exception(
            "agent_query",
            http_request,
            e,
            collection_name=request.collection_name,
        )
        raise HTTPException(status_code=500, detail=f"Agent 执行失败: {str(e)}")


@app.get("/collections", response_model=List[str])
async def list_collections(request: Request):
    """
    获取所有知识库列表

    Returns:
        List[str]: 知识库名称列表
    """
    try:
        collections = await asyncio.to_thread(vector_store.list_collections)
        return collections
    except Exception as e:
        _log_endpoint_exception("list_collections", request, e)
        raise HTTPException(status_code=500, detail=f"获取知识库列表失败: {str(e)}")


@app.get("/collections/{collection_name}/info")
async def get_collection_info(collection_name: str, request: Request):
    """
    获取知识库详细信息

    Args:
        collection_name: 知识库名称

    Returns:
        dict: 知识库信息
    """
    try:
        info = await asyncio.to_thread(vector_store.get_collection_info, collection_name)
        return info
    except Exception as e:
        _log_endpoint_exception(
            "get_collection_info",
            request,
            e,
            collection_name=collection_name,
        )
        raise HTTPException(status_code=500, detail=f"获取知识库信息失败: {str(e)}")


@app.get("/collections/{collection_name}/documents")
async def list_collection_documents(collection_name: str, request: Request):
    """列出当前知识库中的源文档。"""
    try:
        documents = await asyncio.to_thread(vector_store.list_documents, collection_name)
        return {
            "success": True,
            "collection_name": collection_name,
            "documents": documents,
        }
    except Exception as e:
        _log_endpoint_exception(
            "list_collection_documents",
            request,
            e,
            collection_name=collection_name,
        )
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")


@app.delete("/collections/{collection_name}/documents")
async def delete_collection_document(collection_name: str, source: str, request: Request):
    """删除当前知识库中的某个源文档及其全部分块。"""
    try:
        success = await asyncio.to_thread(vector_store.delete_document, collection_name, source)
        if not success:
            raise HTTPException(status_code=404, detail="未找到该文档")
        return {
            "success": True,
            "message": f"文档 '{source}' 已删除",
            "collection_name": collection_name,
            "source": source,
        }
    except HTTPException:
        raise
    except Exception as e:
        _log_endpoint_exception(
            "delete_collection_document",
            request,
            e,
            collection_name=collection_name,
            source=source,
        )
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")


@app.post("/collections/{collection_name}/documents/batch_delete")
async def batch_delete_documents(collection_name: str, request: BatchDeleteRequest, http_request: Request):
    """批量删除多个文档。"""
    try:
        result = await asyncio.to_thread(
            vector_store.delete_documents, collection_name, request.sources
        )
        return {
            "success": True,
            "message": f"已删除 {result['deleted_count']} 个文档",
            **result,
        }
    except Exception as e:
        _log_endpoint_exception(
            "batch_delete_documents",
            http_request,
            e,
            collection_name=collection_name,
            source_count=len(request.sources),
        )
        raise HTTPException(status_code=500, detail=f"批量删除文档失败: {str(e)}")


@app.patch("/collections/{collection_name}/documents/enabled")
async def toggle_document_enabled(collection_name: str, request: ToggleEnabledRequest, http_request: Request):
    """启用或禁用某个文档。"""
    try:
        success = await asyncio.to_thread(
            vector_store.set_document_enabled,
            collection_name,
            request.source,
            request.enabled,
        )
        if not success:
            raise HTTPException(status_code=404, detail="未找到该文档")
        action = "启用" if request.enabled else "禁用"
        return {
            "success": True,
            "message": f"文档 '{request.source}' 已{action}",
        }
    except HTTPException:
        raise
    except Exception as e:
        _log_endpoint_exception(
            "toggle_document_enabled",
            http_request,
            e,
            collection_name=collection_name,
            source=request.source,
            enabled=request.enabled,
        )
        raise HTTPException(status_code=500, detail=f"设置文档启用状态失败: {str(e)}")


@app.post("/collections/{collection_name}")
async def create_collection(collection_name: str, request: Request):
    """
    创建新知识库

    Args:
        collection_name: 知识库名称

    Returns:
        dict: 创建结果
    """
    try:
        # 获取或创建 collection（_get_store 会自动创建）
        store = vector_store._get_store(collection_name)
        return {
            "success": True,
            "message": f"知识库 '{collection_name}' 已创建",
            "collection_name": collection_name,
        }
    except Exception as e:
        _log_endpoint_exception(
            "create_collection",
            request,
            e,
            collection_name=collection_name,
        )
        raise HTTPException(status_code=500, detail=f"创建知识库失败: {str(e)}")


@app.post("/collections/{collection_name}/rename")
async def rename_collection(collection_name: str, request: RenameCollectionRequest, http_request: Request):
    """重命名知识库的用户可见名称。"""
    try:
        new_name = request.new_name.strip()
        if not new_name:
            raise HTTPException(status_code=400, detail="新名称不能为空")
        success = vector_store.rename_collection(collection_name, new_name)
        if success:
            return {
                "success": True,
                "message": f"知识库 '{collection_name}' 已重命名为 '{new_name}'",
                "old_name": collection_name,
                "new_name": new_name,
            }
        raise HTTPException(status_code=500, detail="重命名失败")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        _log_endpoint_exception(
            "rename_collection",
            http_request,
            e,
            collection_name=collection_name,
        )
        raise HTTPException(status_code=500, detail=f"重命名知识库失败: {str(e)}")


@app.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str, request: Request):
    """
    删除知识库

    Args:
        collection_name: 知识库名称

    Returns:
        dict: 删除结果
    """
    try:
        success = vector_store.delete_collection(collection_name)
        if success:
            return {"success": True, "message": f"知识库 '{collection_name}' 已删除"}
        else:
            raise HTTPException(status_code=500, detail="删除失败")
    except HTTPException:
        raise
    except Exception as e:
        _log_endpoint_exception(
            "delete_collection",
            request,
            e,
            collection_name=collection_name,
        )
        raise HTTPException(status_code=500, detail=f"删除知识库失败: {str(e)}")


# ============== 主入口 ==============

if __name__ == "__main__":
    import uvicorn

    logger.info(f"启动FastAPI服务: http://{config.API_HOST}:{config.API_PORT}")
    # 生产环境禁用 reload，提高稳定性
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=False,  # 禁用开发模式自动重载，提高稳定性
        workers=1,
        timeout_keep_alive=120,
    )
