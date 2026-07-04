# 个人 RAG 知识库助手

一个面向个人资料管理的本地 RAG 知识库助手，使用 **FastAPI + Streamlit + LangChain + Chroma + SiliconFlow + Tavily** 构建。项目重点不是简单 demo，而是把“上传入库、混合检索、引用追踪、Agent 工具调用、评测与日志排障”做成一条可维护的完整闭环。

## 项目亮点

- **完整 RAG 闭环**：支持 PDF、TXT、DOCX、Markdown 上传，经过解析、标题感知分块、embedding、Chroma 持久化、检索、生成和引用展示。
- **可解释检索质量**：向量检索 + BM25 + 关键词兜底 + rerank + contextual compression，并输出 `source`、`score`、`candidate_source`、trace 与 eval 诊断。
- **中文个人知识库体验**：支持中文知识库名称、多知识库切换、文档启用/禁用、批量管理、多会话和导出。
- **Agent + Web 搜索融合**：Agent 可调用本地知识库、Tavily/DuckDuckGo Web 搜索和受限 Python 工具；本地资料问题有 local-first 兜底和 evidence summary 调试信息。
- **工程化护栏**：API token、上传校验、request id 全链路日志、前端排障 ID、RAG eval 基线、后端/前端契约测试和真实 UI 回归巡检。

## 快速演示路径

1. 复制 `.env.example` 为 `.env`，填写 SiliconFlow 兼容接口密钥。
2. 运行 `.\start_backend_stable.ps1` 和 `.\start_frontend.ps1`。
3. 打开 `http://127.0.0.1:8501`，创建或选择知识库，上传一份 Markdown/PDF/DOCX/TXT。
4. 在“知识库问答”中提问，查看回答、引用来源、检索 trace 或 Agent debug。

> 公开仓库不提交本地 `chroma_db/`、日志、session、缓存、真实向量库备份或评测报告；这些都由 `.gitignore` 排除。首次运行会在本地自动生成数据目录。

## 界面预览

| 工作台首屏 | 问答与引用 | Agent 调试 |
| --- | --- | --- |
| ![工作台首屏](docs/images/workbench.png) | ![问答与引用](docs/images/rag-answer-sources.png) | ![Agent 调试](docs/images/agent-debug.png) |

截图只展示脱敏演示内容，不包含 `.env`、密钥、本地 Chroma、日志或私有文档正文。

## 前端体验亮点

- **打开即是工作台**：首屏直接展示知识库状态、文档状态和会话状态，不做单独营销落地页。
- **面试演示快捷问题**：内置 BM25 正常问答、域外拒答和引用总结三个高价值入口，方便快速展示 RAG 能力边界。
- **引用证据面板**：回答下方展示来源编号、文件名、相似度、证据片段和复制按钮，便于解释“答案从哪里来”。
- **Agent debug 可解释**：调试面板优先显示 evidence summary，本地/外部来源、Web 降级和策略提醒一眼可见。
- **失败可排障**：前端失败提示会展示排障 ID，可用同一个 request id 搜索 `logs/app.log`。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端服务 | FastAPI, Uvicorn |
| 前端界面 | Streamlit |
| RAG 框架 | LangChain, LangChain Community, LangChain Classic, langchain-chroma |
| 向量数据库 | Chroma 本地持久化 |
| 对话模型 | SiliconFlow OpenAI-compatible Chat API |
| Embedding | `BAAI/bge-large-zh-v1.5` |
| Reranker | `BAAI/bge-reranker-v2-m3` |
| Web 搜索 | Tavily，失败时可降级 DuckDuckGo |
| 多模态 | Qwen VL 类视觉模型 |
| 文档解析 | pypdf, docx2txt, python-docx, markdown, Pillow |

## 项目结构

```text
personal-rag-assistant/
├── .env.example
├── requirements.txt
├── config.py
├── main.py
├── streamlit_app.py
├── start_backend_stable.ps1
├── start_frontend.ps1
├── eval/
│   ├── eval_cases.json
│   └── rag_eval.py
├── rag/
│   ├── agent.py
│   ├── tools.py
│   ├── document_loader.py
│   ├── multimodal.py
│   ├── qa_chain.py
│   ├── reranker.py
│   ├── text_splitter.py
│   └── vector_store.py
├── ui/
│   ├── chat.py
│   ├── sidebar.py
│   ├── upload.py
│   ├── pages.py
│   └── styles/
├── tests/
├── docs/
├── README.md
├── RAG技术详解.md
├── 项目维护手册.md
├── BUG_LOG.md
└── AGENTS.md
```

## 快速开始

### 1. 创建环境

推荐 Python 3.11：

```powershell
conda create -n ai_project python=3.11
conda activate ai_project
```

或使用 venv：

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

如果安装新依赖，必须先做兼容性分析，并同步更新 `requirements.txt`。

### 3. 配置环境变量

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，至少填写：

```env
LLM_API_KEY=sk-your-api-key-here
LLM_API_BASE=https://api.siliconflow.cn/v1
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
EMBEDDING_MODEL=BAAI/bge-large-zh-v1.5
```

## 启动服务

推荐使用稳定脚本：

```powershell
.\start_backend_stable.ps1
.\start_frontend.ps1
```

稳定运行建议：

- 长期运行后端优先使用 `start_backend_stable.ps1`，该脚本使用 `uvicorn main:app --workers 1 --timeout-keep-alive 120`，不启用 `--reload`。
- 开发调试可以手动启动，但生产或长时间使用时不要开启 `--reload`。
- 后端启动后先检查 `http://127.0.0.1:8000/health`，前端启动后再访问 `http://127.0.0.1:8501`。
- 如果启用 `API_TOKEN`，前端 `.env` 和评测命令都需要使用同一个 token。

也可以手动启动：

```powershell
python main.py
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

默认访问地址：

- 前端：`http://127.0.0.1:8501`
- 后端：`http://127.0.0.1:8000`
- API 文档：`http://127.0.0.1:8000/docs`

## 常用 API

### 健康检查

```bash
curl http://127.0.0.1:8000/health
```

### 上传文档

```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@example.pdf" \
  -F "collection_name=默认知识库" \
  -F "chunk_size=500" \
  -F "chunk_overlap=100" \
  -F "enable_multimodal=true"
```

### 问答

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "这份资料的核心观点是什么？",
    "collection_name": "默认知识库",
    "chat_history": [],
    "top_k": 3,
    "temperature": 0.1,
    "enable_query_rewrite": true,
    "enable_contextual_compression": true
  }'
```

### 分步检索与生成

前端的“思考过程”使用这两个接口：

- `/retrieve`：返回检索、重排后的真实片段，并在兼容原字段的基础上追加 `trace`。`sources` 中会包含 `source`、`section`、`score`、`vector_score`、`keyword_score`、`rerank_score`、`candidate_source` 等字段；`trace.final_documents` 用于排查片段为什么被选中。
- `/generate`：基于已检索片段生成最终答案。

所有 HTTP 响应都会带 `X-Request-ID` 和 `X-Process-Time-Ms` 响应头。客户端也可以传入 `X-Request-ID`，后端会保留该值，便于把前端报错和后端日志对应起来。

## 关键配置

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `LLM_API_KEY` | 模型 API 密钥 | 必填 |
| `LLM_MODEL` | 对话模型 | `Qwen/Qwen2.5-72B-Instruct` |
| `LLM_API_BASE` | OpenAI-compatible API 地址 | `https://api.siliconflow.cn/v1` |
| `EMBEDDING_MODEL` | Embedding 模型 | `BAAI/bge-large-zh-v1.5` |
| `CHROMA_DB_PATH` | Chroma 存储目录 | `./chroma_db` |
| `CHUNK_SIZE` | 分块大小 | `500` |
| `CHUNK_OVERLAP` | 分块重叠 | `200` |
| `RETRIEVER_TOP_K` | 返回片段数量 | `3` |
| `RETRIEVER_MIN_SCORE` | 最低检索分数 | `0.35` |
| `RETRIEVER_INITIAL_K_MULTIPLIER` | 初始候选数量倍数 | `6` |
| `RETRIEVER_INITIAL_K_MIN` | 初始候选数量下限 | `20` |
| `RETRIEVER_RERANK_K_MULTIPLIER` | 重排候选数量倍数 | `4` |
| `HYBRID_VECTOR_WEIGHT` | 向量与 BM25 混合时的向量权重 | `0.65` |
| `HYBRID_BM25_WEIGHT` | 向量与 BM25 混合时的 BM25 权重 | `0.35` |
| `RERANK_VECTOR_WEIGHT` | 最终重排向量分权重 | `0.65` |
| `RERANK_KEYWORD_WEIGHT` | 最终重排关键词分权重 | `0.25` |
| `RERANK_PHRASE_WEIGHT` | 最终重排短语命中权重 | `0.10` |
| `ENABLE_QUERY_REWRITE` | 是否启用查询改写 | `true` |
| `ENABLE_QUERY_REWRITE_FALLBACK` | 改写查询无命中时是否回退原上下文查询 | `true` |
| `ENABLE_CONTEXTUAL_COMPRESSION` | 是否启用上下文压缩 | `true` |
| `ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION` | 压缩丢失高置信片段时是否补回基础片段 | `true` |
| `CONTEXTUAL_COMPRESSION_PROTECT_TOP_N` | 最多保护的基础片段数量 | `1` |
| `CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE` | 触发保护的最低基础片段分数 | `0.7` |
| `AGENT_MAX_TOOL_CALLS` | Agent 单次回答最大工具调用次数 | `4` |
| `AGENT_MAX_WEB_SEARCHES` | Agent 单次回答最大网页搜索次数 | `1` |
| `AGENT_MAX_CODE_EXECUTIONS` | Agent 单次回答最大代码执行次数 | `1` |
| `ENABLE_MULTIMODAL_PARSING` | 是否解析文档图片 | `true` |
| `CORS_ALLOW_ORIGINS` | 允许访问后端的前端来源 | `http://127.0.0.1:8501,http://localhost:8501` |

## RAG 评估

项目提供轻量评估脚本：

```powershell
python eval\rag_eval.py --api-base http://127.0.0.1:8000
```

如果后端配置了 `API_TOKEN`：

```powershell
python eval\rag_eval.py --api-base http://127.0.0.1:8000 --api-token your-token
```

评估用例在 `eval/eval_cases.json` 中。修改检索、分块、重排、生成逻辑后，应补充或运行评估用例。
评估输出会显示每个用例的候选数、最终片段数、top source/section/score、缺失关键词和禁用关键词，便于判断是检索未命中还是生成答案缺失。
如需保存结构化报告：

```powershell
python eval\rag_eval.py --api-base http://127.0.0.1:8000 --output-json eval\rag_eval_report.json
```

Agent evaluation checks tool routing, first tool choice, Web fallback, debug fields, and code-tool safety boundaries:

```powershell
python eval\agent_eval.py --api-base http://127.0.0.1:8000 --collection-name default
```

To save a structured Agent eval report:

```powershell
python eval\agent_eval.py --api-base http://127.0.0.1:8000 --output-json eval\agent_eval_report.json
```

`eval/rag_eval_report.json` and `eval/agent_eval_report.json` are local evaluation artifacts and should not be committed to the public repository.

### Backend release gate

Before publishing the repository or doing an interview demo, run the read-only
backend release check:

```powershell
python scripts\check_backend_release.py --api-base http://127.0.0.1:8000
```

The script does not write to Chroma or change configuration. It checks whether
Git tracks local artifacts such as `.env`, `chroma_db/`, logs, caches, and eval
reports; scans tracked text files for real secret-like values; validates
`collection_name_mapping.json`; compares mapping entries with Chroma collection
names; and verifies `/health` with request id diagnostics.

If the backend is not running yet, skip only the health probe:

```powershell
python scripts\check_backend_release.py --no-health
```

### GitHub Actions CI

The repository includes `.github/workflows/ci.yml` for public GitHub checks.
It installs `requirements.txt`, compiles key modules, validates eval JSON, runs
mock/static lightweight tests, and executes `scripts/check_backend_release.py --no-health`.
The CI does not require real LLM keys, Tavily keys, Chroma data, or a running backend.

报告 JSON 会包含通过率、失败 case、错误原因、top sources、关键词检查结果和各阶段耗时。

## 自动化测试

维护 smoke test 使用标准库 `unittest`：

```powershell
python -m unittest tests.test_maintenance_smoke
```

当前覆盖上传内容校验、评估用例校验、API client 兜底和父子块索引缓存。

## 维护状态

已完成的维护项：

- 补齐 LangChain 拆分包、docx2txt、Pillow、chardet 等依赖。
- CORS 环境变量化。
- 可选 `API_TOKEN` 访问保护。
- 上传文件名清理和流式大小限制。
- 上传文件 MIME/文件头校验。
- 滚动文件日志，默认写入 `logs/app.log`。
- Streamlit 会话持久化到 `data/sessions.json`。
- `streamlit_app.py` 的后端请求已抽离到 `rag/api_client.py`。
- `QAChain` 按配置缓存复用。
- 维护 smoke test：上传校验、评估用例校验、API client、父子块索引缓存。
- collection 文档快照缓存和 BM25 缓存。
- 关键词兜底、相邻子块扩展、文档列表复用 collection 快照。
- 父子块索引缓存，减少相邻子块扩展的线性扫描。
- 修复 `rag/vector_store.py` 中历史乱码导致的代码粘连和不可打印字符。
- 清理 `rag/vector_store.py` 中主要日志、异常提示和注释乱码。
- 前端已拆分为 `ui/` 模块，覆盖侧边栏、上传、聊天、文档管理、设置、导出和样式系统。
- 已建立临时 Chroma 后端闭环测试、RAG eval 基线、Agent/Tavily debug 契约和前端 UI 契约测试。
- 真实 RAG eval 已清洗到有文档知识库，当前基线为 14/14 通过。

仍待维护：

- 持续更新公开演示截图或短视频，确保只包含脱敏内容。
- 持续扩充脱敏 eval case，覆盖更多文档类型和 Agent 混合来源场景。

## 故障排查

### 1. API 密钥未配置

确认 `.env` 中存在：

```env
LLM_API_KEY=sk-...
```

不要把 `LLM_API_KEY`、`TAVILY_API_KEY`、`API_TOKEN` 写入日志、截图或提交记录。

### 2. 导入缺包

先确认当前解释器是项目环境：

```powershell
where python
python -m pip install -r requirements.txt
```

### 3. 中文知识库名称显示异常

检查：

```text
chroma_db/collection_name_mapping.json
```

该文件应保存用户可见名称到 Chroma 内部 collection 名称的映射。

### 4. 检索为空

检查：

- 文档是否上传成功。
- 当前选择的知识库是否正确。
- Embedding 模型是否和已有 Chroma 数据维度一致。
- `RETRIEVER_MIN_SCORE` 是否过高。

### 5. 前端报错如何定位后端日志

检查浏览器或 API 响应头中的 `X-Request-ID`，然后在 `logs/app.log` 中搜索同一个 request id：

```powershell
Select-String -Path logs\app.log -Pattern "request_id=<复制的ID>"
```

日志中的 `path`、`status` 和 `elapsed_ms` 可以帮助判断是接口错误、认证错误还是模型/检索耗时过长。

### 6. Tavily 搜索异常

检查：

- `.env` 中是否配置 `TAVILY_API_KEY`。
- `WEB_SEARCH_TIMEOUT` 是否过低。
- `TOOL_RETRY_MAX_ATTEMPTS` 是否符合当前网络环境。

Tavily 未配置或失败时会降级 DuckDuckGo；Agent 调试面板会显示 provider、重试次数和是否降级。

### 7. Chroma 备份与恢复

默认向量库目录是 `chroma_db/`。备份前建议先停止后端服务，完整复制整个目录，包括：

- `chroma.sqlite3`
- collection 子目录
- `collection_name_mapping.json`

不要只复制 `collection_name_mapping.json`，也不要在真实 `chroma_db/collection_name_mapping.json` 上做临时测试。

## 文档索引

- `AGENTS.md`：项目开发规则。
- `RAG技术详解.md`：RAG 链路与模块说明。
- `项目维护手册.md`：维护路线、已完成项和待办项。
- `BUG_LOG.md`：问题记录、修复记录和后续规则。
- `PROJECT_MAP.md`：后端、前端、RAG、测试和数据目录地图。
- `docs/INTERVIEW_GUIDE.md`：面试讲解稿、架构图、RAG 流程图和演示清单。
- `docs/KNOWN_ISSUES.md`：历史坑、待确认风险和安全注意事项。
- `docs/GLOSSARY.md`：项目术语表。

## Agent 与联网搜索

- Agent 模式可调用知识库检索、网页搜索和 Python 代码执行工具。
- Agent 工具策略默认本地知识库优先；只有最新新闻、当前版本、价格、天气等实时外部问题才优先使用网页搜索。
- 同时使用本地知识库和网页搜索时，回答会按“本地资料 / 外部搜索补充 / 来源提示”分层，避免外部搜索覆盖本地资料结论。
- `AGENT_DEBUG=true` 时，`/agent` 会返回 `debug_info`，前端展示工具策略、工具预算、工具调用、搜索服务、重试次数、降级状态和耗时。
- 网页搜索优先使用 Tavily；未配置 `TAVILY_API_KEY` 或 Tavily 失败时自动降级到 DuckDuckGo。
- 外部搜索调用受 `AGENT_MAX_WEB_SEARCHES`、`TOOL_RETRY_MAX_ATTEMPTS`、`TOOL_RETRY_BACKOFF_SECONDS`、`WEB_SEARCH_MAX_RESULTS`、`WEB_SEARCH_TIMEOUT` 控制。
- Agent guide: see `docs/AGENT_GUIDE.md` for capabilities, boundaries, debug fields, and interview demo script.
