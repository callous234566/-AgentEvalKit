"""
Streamlit 前端界面
提供用户友好的文档上传、知识库管理和问答界面
优化版本：支持多会话、流式输出、美观的聊天界面
"""

import logging
from pathlib import Path

import streamlit as st

import config
from rag.api_client import RagApiClient
from rag.logging_utils import setup_logging
from rag.session_state import init_session_state

from ui.api_wrappers import init as init_api_wrappers
from ui.assets import CSS_STYLES
from ui.chat import init_chat, render_chat_section
from ui.components import render_app_hero, render_workspace_overview
from ui.marketing import render_marketing_copilot
from ui.pages import render_document_management, render_settings_panel
from ui.sidebar import init_sidebar, render_sidebar
from ui.upload import render_upload_section

# 配置日志
setup_logging()
logger = logging.getLogger(__name__)

# FastAPI 服务地址
API_BASE_URL = f"http://{config.API_HOST}:{config.API_PORT}"
SESSION_STORE_PATH = config.BASE_DIR / "data" / "sessions.json"
api_client = RagApiClient(API_BASE_URL, config.API_TOKEN)

# 初始化 UI 子模块（注入共享实例，避免循环导入）
init_api_wrappers(api_client)
init_chat(SESSION_STORE_PATH)
init_sidebar(API_BASE_URL, SESSION_STORE_PATH)

# ============== 页面配置 ==============
st.set_page_config(
    page_title="个人 RAG 知识库助手",
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============== 样式注入 ==============
st.markdown(CSS_STYLES, unsafe_allow_html=True)


# ============== 主程序 ==============

def main():
    """主函数"""
    # 初始化会话状态（必须在最前面）
    init_session_state(SESSION_STORE_PATH)

    # 页面标题与主题切换
    title_col, theme_col = st.columns([8, 1], vertical_alignment="top")
    with title_col:
        render_app_hero()
    with theme_col:
        theme_label = "浅色" if st.session_state.dark_mode else "深色"
        if st.button(theme_label, key="theme_toggle_btn", help="切换深色/浅色模式", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # 渲染侧边栏并获取当前知识库
    current_collection = render_sidebar()

    if current_collection is None:
        return

    # 主内容区
    render_workspace_overview(current_collection)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "文档上传",
        "营销工作台",
        "知识库问答",
        "文档管理",
        "系统设置",
    ])

    with tab1:
        render_upload_section(current_collection)

    with tab2:
        render_marketing_copilot(current_collection)

    with tab3:
        render_chat_section(current_collection)

    with tab4:
        render_document_management(current_collection)

    with tab5:
        render_settings_panel()


if __name__ == "__main__":
    main()
