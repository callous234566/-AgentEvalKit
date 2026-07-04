"""
配置文件
集中管理所有环境变量和配置项
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    _HAS_DOTENV = True
except ImportError:
    _HAS_DOTENV = False

# 项目根目录
BASE_DIR = Path(__file__).parent


def _env_bool(name: str, default: bool) -> bool:
    """读取布尔环境变量，支持 true/false、1/0、yes/no。"""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "y"}


def _env_list(name: str, default) -> list:
    """读取逗号分隔的环境变量列表。"""
    raw = os.getenv(name)
    if raw is None:
        return default
    values = [item.strip() for item in raw.split(",") if item.strip()]
    return values or default

# 加载 .env 文件
if _HAS_DOTENV:
    load_dotenv(BASE_DIR / ".env", encoding="utf-8")
else:
    # 回退：手动解析（不支持引号值和行内注释）
    _env_path = BASE_DIR / ".env"
    if _env_path.exists():
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ[_k.strip()] = _v.strip()

# LLM API配置（通用配置，支持多厂商切换）
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-72B-Instruct")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.siliconflow.cn/v1")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2400"))

# Embedding模型配置（使用API，中文兼容）
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5")
EMBEDDING_API_BASE = os.getenv("EMBEDDING_API_BASE", "https://api.siliconflow.cn/v1")

# 兼容旧版DeepSeek配置（如未配置新变量则回退）
if not LLM_API_KEY:
    LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
if not LLM_MODEL:
    LLM_MODEL = os.getenv("DEEPSEEK_CHAT_MODEL", "deepseek-chat")
if not LLM_API_BASE or LLM_API_BASE == "":
    LLM_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.siliconflow.cn/v1")

# 向量数据库配置
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# 文本分块配置
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# 检索配置
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "3"))
RETRIEVER_MIN_SCORE = float(os.getenv("RETRIEVER_MIN_SCORE", "0.35"))
RETRIEVER_INITIAL_K_MULTIPLIER = int(os.getenv("RETRIEVER_INITIAL_K_MULTIPLIER", "6"))
RETRIEVER_INITIAL_K_MIN = int(os.getenv("RETRIEVER_INITIAL_K_MIN", "20"))
RETRIEVER_RERANK_K_MULTIPLIER = int(os.getenv("RETRIEVER_RERANK_K_MULTIPLIER", "4"))
HYBRID_VECTOR_WEIGHT = float(os.getenv("HYBRID_VECTOR_WEIGHT", "0.65"))
HYBRID_BM25_WEIGHT = float(os.getenv("HYBRID_BM25_WEIGHT", "0.35"))
RERANK_VECTOR_WEIGHT = float(os.getenv("RERANK_VECTOR_WEIGHT", "0.65"))
RERANK_KEYWORD_WEIGHT = float(os.getenv("RERANK_KEYWORD_WEIGHT", "0.25"))
RERANK_PHRASE_WEIGHT = float(os.getenv("RERANK_PHRASE_WEIGHT", "0.10"))
KEYWORD_HEADER_WEIGHT = float(os.getenv("KEYWORD_HEADER_WEIGHT", "0.35"))
KEYWORD_PHRASE_WEIGHT = float(os.getenv("KEYWORD_PHRASE_WEIGHT", "0.50"))
KEYWORD_MAX_CANDIDATE_SCORE = float(os.getenv("KEYWORD_MAX_CANDIDATE_SCORE", "2.5"))
KEYWORD_PSEUDO_DISTANCE_FLOOR = float(os.getenv("KEYWORD_PSEUDO_DISTANCE_FLOOR", "0.15"))
KEYWORD_PSEUDO_DISTANCE_MAX_SCORE = float(os.getenv("KEYWORD_PSEUDO_DISTANCE_MAX_SCORE", "0.85"))
ENABLE_QUERY_REWRITE = _env_bool("ENABLE_QUERY_REWRITE", True)
ENABLE_QUERY_REWRITE_FALLBACK = _env_bool("ENABLE_QUERY_REWRITE_FALLBACK", True)
ENABLE_CONTEXTUAL_COMPRESSION = _env_bool("ENABLE_CONTEXTUAL_COMPRESSION", True)

# BGE reranker 上下文压缩配置
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
RERANKER_API_BASE = os.getenv("RERANKER_API_BASE", LLM_API_BASE)
RERANKER_TIMEOUT = int(os.getenv("RERANKER_TIMEOUT", "45"))
RERANKER_MIN_SCORE = float(os.getenv("RERANKER_MIN_SCORE", "0.0"))
CONTEXTUAL_COMPRESSION_SENTENCES_PER_DOC = int(os.getenv("CONTEXTUAL_COMPRESSION_SENTENCES_PER_DOC", "3"))
CONTEXTUAL_COMPRESSION_MAX_CHARS = int(os.getenv("CONTEXTUAL_COMPRESSION_MAX_CHARS", "1800"))
ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION = _env_bool("ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION", True)
CONTEXTUAL_COMPRESSION_PROTECT_TOP_N = int(os.getenv("CONTEXTUAL_COMPRESSION_PROTECT_TOP_N", "1"))
CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE = float(os.getenv("CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE", "0.7"))

# 多模态文档解析配置
ENABLE_MULTIMODAL_PARSING = _env_bool("ENABLE_MULTIMODAL_PARSING", True)
MULTIMODAL_MODEL = os.getenv("MULTIMODAL_MODEL", "Qwen/Qwen2.5-VL-72B-Instruct")
MULTIMODAL_API_BASE = os.getenv("MULTIMODAL_API_BASE", LLM_API_BASE)
MULTIMODAL_MAX_IMAGES_PER_FILE = int(os.getenv("MULTIMODAL_MAX_IMAGES_PER_FILE", "12"))
MULTIMODAL_IMAGE_MAX_SIDE = int(os.getenv("MULTIMODAL_IMAGE_MAX_SIDE", "1280"))
MULTIMODAL_IMAGE_MIN_BYTES = int(os.getenv("MULTIMODAL_IMAGE_MIN_BYTES", "1024"))
MULTIMODAL_TIMEOUT = int(os.getenv("MULTIMODAL_TIMEOUT", "90"))

# 多轮对话配置
CHAT_HISTORY_TURNS = int(os.getenv("CHAT_HISTORY_TURNS", "5"))

# FastAPI服务配置
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TOKEN = os.getenv("API_TOKEN", "").strip()
CORS_ALLOW_ORIGINS = _env_list(
    "CORS_ALLOW_ORIGINS",
    [
        "http://127.0.0.1:8501",
        "http://localhost:8501",
    ],
)

# 日志配置
LOG_DIR = os.getenv("LOG_DIR", "./logs")
LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", str(5 * 1024 * 1024)))
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# 支持的文档格式
SUPPORTED_EXTENSIONS = {
    ".pdf": "PDF文档",
    ".txt": "文本文件",
    ".docx": "Word文档",
    ".md": "Markdown文档",
}

SUPPORTED_MIME_TYPES = {
    ".pdf": {"application/pdf"},
    ".txt": {"text/plain", "application/octet-stream"},
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
        "application/octet-stream",
    },
    ".md": {"text/markdown", "text/x-markdown", "text/plain", "application/octet-stream"},
}

# 最大上传文件大小 (20MB)
MAX_UPLOAD_SIZE = 20 * 1024 * 1024


def check_api_key() -> bool:
    """
    检查API密钥是否已配置

    Returns:
        bool: API密钥是否有效
    """
    return bool(LLM_API_KEY and LLM_API_KEY != "your_deepseek_api_key_here" and LLM_API_KEY != "sk-your-api-key-here")


# ============== 检索增强配置（可自定义） ==============

# 指代消解触发词（用于多轮对话中检测代词引用）
CONTEXTUAL_PRONOUNS = ["它", "其中", "这个", "那个", "上述", "前面", "那"]

# 关键词扩展规则：触发词 -> 扩展词集合
# 用于 BM25/关键词检索时扩展查询，提升召回率
# 可根据实际知识库领域自定义
TERM_EXPANSION_RULES = [
    {
        "triggers": ["chain", "链"],
        "expand": ["chain", "chains", "链", "链模块", "llmchain",
                    "sequentialchain", "routerchain", "transformchain", "工作流"],
    },
    {
        "triggers": ["agent", "代理", "智能体"],
        "expand": ["agent", "agents", "代理", "智能体", "工具",
                    "执行器", "agentexecutor", "react"],
    },
    {
        "triggers": ["rag"],
        "expand": ["rag", "检索", "生成", "嵌入", "向量", "上下文"],
    },
    {
        "triggers": ["代码", "示例"],
        "expand": ["代码", "示例", "python", "运行"],
    },
    {
        "triggers": ["大文件", "分块", "内存"],
        "expand": ["大文件", "分块", "内存", "内存溢出", "oom",
                    "流式读取", "逐块读取", "逐行读取", "stream_read_text",
                    "chunk_size", "read()", "generator", "Generator"],
    },
    {
        "triggers": ["检索链"],
        "expand": ["retrievalqa", "retriever", "retrievers",
                    "检索器", "向量存储", "similarity_search"],
    },
    {
        "triggers": ["生成组件", "生成"],
        "expand": ["生成", "生成组件", "生成优化", "大语言模型", "llm",
                    "prompt", "提示词", "提示词优化", "上下文压缩", "链式思考", "模型"],
    },
]


# ============== Agent 配置 ==============

AGENT_ENABLED = _env_bool("AGENT_ENABLED", True)
AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", "5"))
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0"))
AGENT_DEBUG = _env_bool("AGENT_DEBUG", True)
AGENT_MAX_TOOL_CALLS = int(os.getenv("AGENT_MAX_TOOL_CALLS", "4"))
AGENT_MAX_WEB_SEARCHES = int(os.getenv("AGENT_MAX_WEB_SEARCHES", "1"))
AGENT_MAX_CODE_EXECUTIONS = int(os.getenv("AGENT_MAX_CODE_EXECUTIONS", "1"))
TOOL_RETRY_MAX_ATTEMPTS = int(os.getenv("TOOL_RETRY_MAX_ATTEMPTS", "2"))
TOOL_RETRY_BACKOFF_SECONDS = float(os.getenv("TOOL_RETRY_BACKOFF_SECONDS", "0.5"))

# ============== 网页搜索配置 ==============

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_SEARCH_DEPTH = os.getenv("TAVILY_SEARCH_DEPTH", "basic")
WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
WEB_SEARCH_TIMEOUT = int(os.getenv("WEB_SEARCH_TIMEOUT", "15"))
