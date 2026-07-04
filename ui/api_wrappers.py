"""API 包装层：薄封装 RagApiClient，供 UI 模块调用。

通过 init() 注入 api_client 实例，避免从 streamlit_app 反向导入。
读操作（list_collections / list_documents）带 session_state 缓存，
写操作（create / delete / rename / upload / toggle）后主动失效对应缓存。
"""

import time

import streamlit as st

import config

# 由 streamlit_app.py 在启动时调用 init() 注入
_api_client = None

_COLLECTIONS_CACHE_TTL = 5.0
_DOCUMENTS_CACHE_TTL = 5.0


def init(client):
    """注入 RagApiClient 单例，必须在任何 UI 渲染前调用。"""
    global _api_client
    _api_client = client


def check_api_connection() -> bool:
    """检查后端 API 是否可用"""
    return _api_client.health()


def get_last_response_meta() -> dict:
    """Return the last backend response diagnostics captured by the API client."""
    if _api_client is None:
        return {}
    return dict(getattr(_api_client, "last_response_meta", {}) or {})


def format_last_response_diagnostic_suffix(prefix: str = "\n\n") -> str:
    """Return a compact request id suffix for failed frontend messages."""
    meta = get_last_response_meta()
    request_id = str(meta.get("request_id") or "").strip()
    if not request_id:
        return ""

    details = [f"排障 ID：{request_id}"]
    status_code = meta.get("status_code")
    if status_code is not None:
        details.append(f"状态码：{status_code}")
    process_time_ms = str(meta.get("process_time_ms") or "").strip()
    if process_time_ms:
        details.append(f"耗时：{process_time_ms}ms")
    return prefix + " · ".join(details)


def _invalidate_collections_cache():
    st.session_state.pop("_collections_cache_data", None)
    st.session_state.pop("_collections_cache_ts", None)


def _invalidate_documents_cache(collection_name: str = None):
    if collection_name:
        key = f"_documents_cache_{collection_name}"
        st.session_state.pop(f"{key}_data", None)
        st.session_state.pop(f"{key}_ts", None)
    else:
        for k in list(st.session_state.keys()):
            if k.startswith("_documents_cache_"):
                del st.session_state[k]


def get_collections() -> list:
    """获取知识库列表（带缓存）"""
    now = time.monotonic()
    cached_ts = st.session_state.get("_collections_cache_ts", 0)
    if now - cached_ts < _COLLECTIONS_CACHE_TTL:
        return st.session_state.get("_collections_cache_data", [])
    result = _api_client.list_collections()
    st.session_state["_collections_cache_data"] = result
    st.session_state["_collections_cache_ts"] = now
    return result


def upload_file(
    file,
    collection_name: str,
    chunk_size: int = None,
    chunk_overlap: int = None,
    enable_multimodal: bool = None,
) -> dict:
    """上传文件到后端"""
    result = _api_client.upload_file(
        file=file,
        collection_name=collection_name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        enable_multimodal=enable_multimodal,
    )
    if result.get("success"):
        _invalidate_documents_cache(collection_name)
    return result


def retrieve_documents_api(question: str, collection_name: str, chat_history: list = None) -> dict:
    """向后端发送检索请求，返回真实检索片段与分数"""
    return _api_client.retrieve(
        question=question,
        collection_name=collection_name,
        chat_history=chat_history,
        top_k=st.session_state.get("settings_top_k", config.RETRIEVER_TOP_K),
        temperature=st.session_state.get("settings_temperature", config.LLM_TEMPERATURE),
        enable_query_rewrite=st.session_state.get("settings_query_rewrite", config.ENABLE_QUERY_REWRITE),
        enable_contextual_compression=st.session_state.get(
            "settings_contextual_compression",
            config.ENABLE_CONTEXTUAL_COMPRESSION,
        ),
    )


def generate_answer_api(
    question: str,
    collection_name: str,
    documents: list,
    chat_history: list = None,
) -> dict:
    """基于已检索片段生成回答"""
    return _api_client.generate(
        question=question,
        collection_name=collection_name,
        documents=documents,
        chat_history=chat_history,
        temperature=st.session_state.get("settings_temperature", config.LLM_TEMPERATURE),
    )


def create_collection_api(collection_name: str) -> dict:
    """创建新知识库"""
    result = _api_client.create_collection(collection_name)
    if result.get("success"):
        _invalidate_collections_cache()
    return result


def delete_collection_api(collection_name: str) -> bool:
    """删除知识库"""
    success = _api_client.delete_collection(collection_name)
    if success:
        _invalidate_collections_cache()
        _invalidate_documents_cache(collection_name)
    return success


def rename_collection_api(collection_name: str, new_name: str) -> dict:
    """重命名知识库"""
    result = _api_client.rename_collection(collection_name, new_name)
    if result.get("success"):
        _invalidate_collections_cache()
        _invalidate_documents_cache(collection_name)
        _invalidate_documents_cache(new_name)
    return result


def list_documents_api(collection_name: str) -> dict:
    """获取当前知识库文档列表（带缓存）"""
    now = time.monotonic()
    cache_key = f"_documents_cache_{collection_name}"
    cached_ts = st.session_state.get(f"{cache_key}_ts", 0)
    if now - cached_ts < _DOCUMENTS_CACHE_TTL:
        return st.session_state.get(f"{cache_key}_data", {"success": False})
    result = _api_client.list_documents(collection_name)
    st.session_state[f"{cache_key}_data"] = result
    st.session_state[f"{cache_key}_ts"] = now
    return result


def delete_document_api(collection_name: str, source: str) -> dict:
    """删除当前知识库中的文档"""
    result = _api_client.delete_document(collection_name, source)
    if result.get("success"):
        _invalidate_documents_cache(collection_name)
    return result


def batch_delete_documents_api(collection_name: str, sources: list) -> dict:
    """批量删除多个文档"""
    result = _api_client.batch_delete_documents(collection_name, sources)
    if result.get("success"):
        _invalidate_documents_cache(collection_name)
    return result


def toggle_document_enabled_api(collection_name: str, source: str, enabled: bool) -> dict:
    """启用或禁用某个文档"""
    result = _api_client.toggle_document_enabled(collection_name, source, enabled)
    if result.get("success"):
        _invalidate_documents_cache(collection_name)
    return result


def agent_query_api(question: str, collection_name: str, chat_history: list = None) -> dict:
    """Agent 模式问答：自主选择工具来回答问题"""
    return _api_client.agent(
        question,
        collection_name,
        chat_history,
        debug=st.session_state.get("settings_agent_debug", config.AGENT_DEBUG),
    )
