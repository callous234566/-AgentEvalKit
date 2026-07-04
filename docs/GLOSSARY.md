# GLOSSARY

## 核心术语

- RAG：Retrieval-Augmented Generation，先检索知识库片段，再让大模型基于片段回答。
- 知识库 / collection：用户可见的资料集合。内部由 Chroma collection 存储，中文显示名通过映射文件持久化。
- Chroma：本地向量数据库，默认目录为 `chroma_db/`。
- `collection_name_mapping.json`：用户可见知识库名称与 Chroma 内部名称的映射文件。
- Embedding：文本向量化。当前配置使用 SiliconFlow OpenAI-compatible Embedding API。
- `check_embedding_ctx_length=False`：LangChain OpenAIEmbeddings 兼容 SiliconFlow 中文输入的关键参数，避免把中文文本变成 token-id 数组。
- BM25：词法检索方法，用于混合检索和关键词兜底。
- Hybrid Search / 混合检索：向量检索、BM25、关键词检索等结果合并。
- Reranker：重排序模型，用于对召回片段重新排序。
- Contextual Compression / 上下文压缩：从召回片段中压缩出更相关的上下文，降低噪声。
- Query Rewrite / 查询改写：根据问题和历史对话生成更适合检索的查询。
- 多模态解析：提取 PDF/DOCX 图片并用视觉模型生成中文说明后入库。
- Agent 模式：通过工具调用执行知识库搜索、Web 搜索或代码执行等步骤，再生成回答。

## 前端术语

- 三点菜单：侧边栏知识库/会话行的操作入口，高回归风险。
- 固定输入框：问答页底部固定的输入区域，不应要求用户滚到最新消息才能输入。
- 最新回答入口：用户离开底部时出现的“查看最新回答”按钮。
- 上传任务队列：上传页中合并“已选择文件”和“处理状态”的单一队列。
- `upload_removed_keys`：上传队列中记录已移除文件的 Streamlit session state key。
- `upload_task_queue`：上传任务队列状态，包含等待、处理中、成功、失败等状态。
- `render_status_notice()`：统一页面级状态提示组件，替代默认 Streamlit 大色块。
- CSS final refinement：后加载的最终覆盖层，如 `_dark_refinement.py` 和 `_mobile_refinement.py`。

## 重要文件与目录

- `main.py`：FastAPI 后端入口。
- `streamlit_app.py`：Streamlit 前端入口。
- `rag/`：RAG 后端核心模块。
- `ui/`：Streamlit 前端拆分模块。
- `ui/styles/`：CSS 变量、基础样式、组件样式和最终覆盖层。
- `tests/`：pytest 测试。
- `eval/`：RAG 评估脚本和用例。
- `data/sessions.json`：会话持久化文件。
- `.agents/skills/`：项目级 Codex skills。
- `$HOME/.agents/skills/`：全局通用 Codex skills。

## 命令术语

- `py_compile`：Python 语法编译检查，不运行完整业务流程。
- `pytest -q`：安静模式运行 pytest。
- `git diff --check`：检查 diff 中的尾随空格等格式问题。
- `rg`：ripgrep，用于快速搜索文本或文件。
