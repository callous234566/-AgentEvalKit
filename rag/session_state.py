"""
会话状态管理模块。
负责 Streamlit session_state 的初始化、持久化和会话 CRUD 操作。
"""

import json
import logging
import time
from pathlib import Path

import streamlit as st

import config

logger = logging.getLogger(__name__)


def load_persisted_sessions(store_path: Path) -> dict:
    """从本地 JSON 文件加载会话。"""
    if not store_path.exists():
        return {"sessions": {}, "current_session_id": None, "input_history": []}
    try:
        with open(store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sessions = data.get("sessions") if isinstance(data, dict) else {}
        if not isinstance(sessions, dict):
            sessions = {}
        return {
            "sessions": sessions,
            "current_session_id": data.get("current_session_id") if isinstance(data, dict) else None,
            "input_history": data.get("input_history", []) if isinstance(data, dict) else [],
        }
    except Exception as e:
        logger.warning(f"加载会话持久化文件失败：{e}")
        return {"sessions": {}, "current_session_id": None, "input_history": []}


def persist_sessions(store_path: Path):
    """保存会话到本地 JSON 文件。"""
    try:
        store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "current_session_id": st.session_state.get("current_session_id"),
            "sessions": dict(st.session_state.get("sessions", {})),
            "input_history": list(st.session_state.get("input_history", []))[-20:],
            "updated_at": time.time(),
        }
        with open(store_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存会话持久化文件失败：{e}")


def init_session_state(store_path: Path):
    """初始化会话状态。"""
    persisted = load_persisted_sessions(store_path) if "sessions_loaded_from_disk" not in st.session_state else None
    if "sessions" not in st.session_state:
        st.session_state.sessions = persisted["sessions"] if persisted else {}
    if "current_session_id" not in st.session_state:
        current_id = persisted["current_session_id"] if persisted else None
        st.session_state.current_session_id = current_id if current_id in st.session_state.sessions else None
    if "chat_history" not in st.session_state:
        current_id = st.session_state.current_session_id
        if current_id and current_id in st.session_state.sessions:
            st.session_state.chat_history = st.session_state.sessions[current_id].get("messages", [])
        else:
            st.session_state.chat_history = []
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "show_clear_confirm" not in st.session_state:
        st.session_state.show_clear_confirm = False
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "input_counter" not in st.session_state:
        st.session_state.input_counter = 0
    if "scroll_to_bottom" not in st.session_state:
        st.session_state.scroll_to_bottom = False
    if "answer_scroll_pending" not in st.session_state:
        st.session_state.answer_scroll_pending = False
    if "scroll_request_id" not in st.session_state:
        st.session_state.scroll_request_id = 0
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "input_history" not in st.session_state:
        st.session_state.input_history = persisted["input_history"] if persisted else []
    if "sessions_loaded_from_disk" not in st.session_state:
        st.session_state.sessions_loaded_from_disk = True
    if "rename_session_id" not in st.session_state:
        st.session_state.rename_session_id = None
    if "delete_session_id" not in st.session_state:
        st.session_state.delete_session_id = None
    if "delete_document_source" not in st.session_state:
        st.session_state.delete_document_source = None
    if "selected_documents" not in st.session_state:
        st.session_state.selected_documents = set()
    if "batch_delete_confirm" not in st.session_state:
        st.session_state.batch_delete_confirm = False
    if "rename_collection_name" not in st.session_state:
        st.session_state.rename_collection_name = None
    if "delete_collection_name" not in st.session_state:
        st.session_state.delete_collection_name = None
    if "settings_top_k" not in st.session_state:
        st.session_state.settings_top_k = config.RETRIEVER_TOP_K
    if "settings_chunk_size" not in st.session_state:
        st.session_state.settings_chunk_size = config.CHUNK_SIZE
    if "settings_chunk_overlap" not in st.session_state:
        st.session_state.settings_chunk_overlap = config.CHUNK_OVERLAP
    if "settings_temperature" not in st.session_state:
        st.session_state.settings_temperature = config.LLM_TEMPERATURE
    if "settings_show_thinking" not in st.session_state:
        st.session_state.settings_show_thinking = True
    if "settings_query_rewrite" not in st.session_state:
        st.session_state.settings_query_rewrite = config.ENABLE_QUERY_REWRITE
    if "settings_contextual_compression" not in st.session_state:
        st.session_state.settings_contextual_compression = config.ENABLE_CONTEXTUAL_COMPRESSION
    if "settings_multimodal_parsing" not in st.session_state:
        st.session_state.settings_multimodal_parsing = config.ENABLE_MULTIMODAL_PARSING
    if "settings_agent_mode" not in st.session_state:
        st.session_state.settings_agent_mode = False
    if "settings_agent_debug" not in st.session_state:
        st.session_state.settings_agent_debug = config.AGENT_DEBUG


def create_new_session(store_path: Path) -> str:
    """创建新会话。"""
    import uuid
    session_id = str(uuid.uuid4())[:8]
    st.session_state.sessions[session_id] = {
        "id": session_id,
        "name": "新会话",
        "user_named": False,
        "messages": [],
        "created_at": time.time(),
    }
    persist_sessions(store_path)
    return session_id


def get_session_name(session_id: str) -> str:
    """获取会话显示名称。"""
    session = st.session_state.sessions.get(session_id, {})
    if session.get("user_named") and session.get("name"):
        return str(session["name"])

    messages = session.get("messages", [])

    # 如果有用户消息，使用第一条用户消息的前15个字
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"].strip()
            if content:
                return content[:15] + "..." if len(content) > 15 else content

    return "新会话"


def switch_session(session_id: str, store_path: Path):
    """切换到指定会话。"""
    if session_id in st.session_state.sessions:
        st.session_state.current_session_id = session_id
        st.session_state.chat_history = st.session_state.sessions[session_id]["messages"]
        persist_sessions(store_path)


def delete_current_session(store_path: Path):
    """删除当前会话。"""
    delete_session(st.session_state.current_session_id, store_path)


def delete_session(session_id: str, store_path: Path):
    """删除指定会话，并切换到相邻可用会话。"""
    if session_id and session_id in st.session_state.sessions:
        del st.session_state.sessions[session_id]

        # 切换到其他会话或创建新会话
        if st.session_state.sessions:
            new_session_id = list(st.session_state.sessions.keys())[0]
            switch_session(new_session_id, store_path)
        else:
            new_session_id = create_new_session(store_path)
            switch_session(new_session_id, store_path)
        persist_sessions(store_path)


def save_current_session(store_path: Path):
    """保存当前会话到 sessions。"""
    current_id = st.session_state.current_session_id
    if current_id and current_id in st.session_state.sessions:
        st.session_state.sessions[current_id]["messages"] = st.session_state.chat_history.copy()
        if not st.session_state.sessions[current_id].get("user_named"):
            st.session_state.sessions[current_id]["name"] = get_session_name(current_id)
        persist_sessions(store_path)


def rename_session(session_id: str, new_name: str, store_path: Path):
    """重命名指定会话。"""
    name = (new_name or "").strip()
    if session_id in st.session_state.sessions and name:
        st.session_state.sessions[session_id]["name"] = name[:40]
        st.session_state.sessions[session_id]["user_named"] = True
        persist_sessions(store_path)
