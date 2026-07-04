# PROJECT_MAP

本文件帮助 Codex 快速建立当前仓库的真实结构认知。内容基于当前仓库文件、启动脚本、测试和近期任务记录；不确定内容标为“待确认”。

## 项目定位

- 项目名：`personal-rag-assistant`
- 类型：本地个人 RAG 知识库助手
- 技术栈：SiliconFlow OpenAI-compatible API、LangChain、Chroma、FastAPI、Streamlit
- 目标：多知识库、本地持久化、中文知识库名称、文档上传、检索问答、引用来源、会话管理和可视化前端

## 顶层入口

- `main.py`：FastAPI 后端入口，提供上传、问答、检索、生成、Agent、知识库和文档管理 API。
- `streamlit_app.py`：Streamlit 前端入口，负责页面配置、样式注入、侧边栏、上传、问答、文档管理、系统设置。
- `config.py`：环境变量、模型、Chroma、分块、检索、多模态、Agent、搜索、日志和 API 配置。
- `requirements.txt` / `pyproject.toml`：依赖声明。新增依赖必须先做兼容性分析并同步维护。
- `start_backend_stable.ps1`：推荐后端稳定启动脚本。
- `start_frontend.ps1`：前端启动脚本。

## 后端模块地图

- `rag/vector_store.py`：Chroma 管理、中文名称映射、Embedding、混合检索、BM25、缓存、重排、上下文压缩、文档启用/禁用、文档删除、知识库重命名/删除。
- `rag/qa_chain.py`：问答链、检索查询改写、上下文组织、基于检索片段生成回答、多轮对话指代处理、兜底回答。
- `rag/document_loader.py`：PDF、TXT、DOCX、Markdown 文档加载，并可接入多模态解析。
- `rag/text_splitter.py`：Markdown 标题感知分块和普通文本递归分块。
- `rag/multimodal.py`：文档图片解析相关能力；多模态权限失败应降级或返回友好提示。
- `rag/reranker.py`：BGE reranker 与降级逻辑。
- `rag/agent.py`：Agent 执行逻辑、RAG 评估类问题特殊处理、调试信息。
- `rag/tools.py`：知识库搜索、Web 搜索、Python 执行等 Agent 工具；Tavily 失败可降级到 DuckDuckGo。
- `rag/api_client.py`：前端调用 FastAPI 的客户端封装。
- `rag/session_state.py`：Streamlit 会话状态、会话持久化、会话命名与删除。
- `rag/upload_validation.py`：上传文件扩展名、MIME、文件头和内容校验。
- `rag/logging_utils.py`：日志配置。

## FastAPI 路由地图

来自 `main.py`：

- `GET /`：根信息。
- `GET /health`：健康检查。
- `POST /upload`：上传文档并写入知识库。
- `POST /ask`：端到端问答。
- `POST /retrieve`：只检索并返回片段、source 和 trace。
- `POST /generate`：基于已检索片段生成回答。
- `POST /agent`：Agent 模式问答。
- `GET /collections`：列出知识库。
- `GET /collections/{collection_name}/info`：知识库信息。
- `GET /collections/{collection_name}/documents`：列出知识库源文档。
- `DELETE /collections/{collection_name}/documents`：删除单个源文档。
- `POST /collections/{collection_name}/documents/batch_delete`：批量删除源文档。
- `PATCH /collections/{collection_name}/documents/enabled`：启用或禁用源文档。
- `POST /collections/{collection_name}`：创建知识库。
- `POST /collections/{collection_name}/rename`：重命名知识库。
- `DELETE /collections/{collection_name}`：删除知识库。

## 前端模块地图

- `ui/assets.py`：导出组合 CSS 和图标辅助。
- `ui/components.py`：共享组件，例如 Hero、概览卡、统一状态提示、AI 消息 HTML、引用证据卡。
- `ui/sidebar.py`：知识库管理、会话历史、三点菜单、删除确认、重命名和分享入口。
- `ui/upload.py`：上传选择、任务队列、删除、状态实时更新、失败提示、处理按钮。
- `ui/chat.py`：聊天页、固定输入框、快捷提问、检索/生成流程、Agent 调试、导出、清空确认、最新回答滚动。
- `ui/marketing.py`：AI Marketing Intelligence Copilot 工作台，提供 Campaign Angle Finder、Landing Page Critique、Creative Brief Generator 和 Test Plan Builder 四类营销工作流提示。
- `ui/pages.py`：文档管理、搜索筛选排序、全选/删除/启用/禁用、系统设置。
- `ui/api_wrappers.py`：前端 API 包装和缓存失效。
- `ui/session_ui.py`：会话分享和导出面板。
- `ui/js_injection.py`：前端增强脚本，包括复制、快捷键、即时加载反馈、固定输入框、滚动跟随、按钮可访问标签。
- `ui/icons.py`：线性 SVG 图标。
- `ui/export.py`：Markdown、纯文本和 PDF 导出。
- `ui/text_utils.py`：文本清理，兼容历史 HTML 泄漏问题。

## 样式系统地图

样式由 `ui/styles/__init__.py` 组合，加载顺序很重要：

1. `_variables.py`：CSS 变量，必须最先加载。
2. `_global.py`、`_chat.py`、`_dark.py`、`_responsive.py`、`_sidebar.py`、`_workspace.py`、`_documents.py`、`_upload.py`、`_widgets.py`、`_buttons.py`：基础和组件样式。
3. `_sidebar_refinement.py`、`_empty_states.py`：后加载的专项修正。
4. `_dark_refinement.py`：最终深色覆盖层。
5. `_mobile_refinement.py`：最终移动端覆盖层。

不要随意调整顺序。三点菜单、上传删除、固定输入框、深色模式、移动端侧边栏属于高回归风险区域。

## 数据与持久化

- `chroma_db/`：当前 Chroma 持久化目录，包含向量数据和 `collection_name_mapping.json`。不要在真实 mapping 文件上做临时测试。
- `data/sessions.json`：Streamlit 多会话持久化。
- `logs/`、`.runtime_logs/`、`.runlogs/`：运行日志。
- `zhishiku/`：示例或本地知识资料。
- `samples/marketing/`：公开参赛/演示用的虚构营销样例资料，包含 offer brief、customer notes、landing page copy、ad performance CSV 和 competitor notes。
- `chroma_db_backup_*`、`chroma_db_dim384_*`、`chroma_export_*.json`：备份/导出数据。用途和是否仍需保留：待确认。
- `vector_store.restore.tmp`：空临时文件。用途：待确认。

## 公开文档入口

- `README.md`：公开仓库首页，说明定位、快速启动、RAG/Agent 能力、评测和发布检查。
- `CHANGELOG.md`：公开版本变更记录。
- `docs/PROJECT_WALKTHROUGH.md`：项目架构、RAG 流程、可展开技术点和讲解清单。
- `docs/SAMPLE_DATA.md`：脱敏示例资料和快速体验路线。
- `docs/AGENT_GUIDE.md`：Agent 能力、debug 字段、使用示例和评测入口。
- `docs/OPEN_SOURCE_CHECKLIST.md`：公开仓库发布检查清单。

## 测试与验证

- Pytest 配置：`pytest.ini`，`testpaths = tests`。
- 前端契约测试：`tests/test_frontend_ui_contracts.py`。
- 维护 smoke：`tests/test_maintenance_smoke.py`。
- 关键后端/RAG 测试包括：`tests/test_vector_store.py`、`tests/test_api_client.py`、`tests/test_main_endpoints.py`、`tests/test_qa_chain.py`、`tests/test_document_loader.py`、`tests/test_text_splitter.py`、`tests/test_tools_tavily.py`。
- RAG 评估：`eval/rag_eval.py` 和 `eval/eval_cases.json`。

常用命令：

```powershell
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-pycache'
D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py main.py
```

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q
```

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_api_client.py -q
```

```powershell
git diff --check -- <touched-files>
```

## Codex 工作约定

- 修改后更新 `BUG_LOG.md`。
- 重复出现的问题上升到 `AGENTS.md`。
- 接口变更同步更新 `README.md`。
- 技术实现细节同步更新 `RAG技术详解.md`。
- 维护路线或未完成项同步更新 `项目维护手册.md`。
- PowerShell 读取中文可能显示乱码；判断真实内容时使用 Python UTF-8 读取。
- 当前工作区可能很脏，不要 reset/revert/清理未追踪文件。
