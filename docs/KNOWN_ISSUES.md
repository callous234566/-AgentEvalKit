# KNOWN_ISSUES

本文件记录 Codex 维护本项目时最容易踩的长期坑。内容来自当前仓库文档、`AGENTS.md`、`BUG_LOG.md` 和近期任务经验。

## 高风险交互

- 侧边栏三点菜单：知识库菜单项为“置顶 / 重命名 / 删除”，会话菜单项为“分享 / 置顶 / 重命名 / 删除”。不要恢复 `st.popover` 或让三点菜单变成独立旧样式。
- 上传队列删除：必须以 Streamlit `session_state` 为准，不能依赖隐藏原生上传器 DOM。新增文件时要保留已移除记录和已完成任务状态，成功文件不得重复入库。
- 固定输入框：用户滚动查看历史时，输入框应固定在底部；生成期间只在用户靠近底部时自动跟随。用户离开底部后必须提供“查看最新回答”入口。
- 文档管理：全选、删除、禁用、启用都涉及后端状态同步。不要只改前端展示。
- 深浅色切换：新增组件必须检查 `_dark_refinement.py`，避免亮白/亮红硬编码在深色模式下冒出。

## 已知历史问题与规则

- Chroma collection 内部名称不适合直接使用中文，用户可见名称与内部名称通过 `collection_name_mapping.json` 持久化映射。
- 不得在真实 `chroma_db/collection_name_mapping.json` 上做临时测试；名称映射测试必须用临时目录。
- Chroma 备份应完整复制整个 `chroma_db/` 目录，包含 sqlite、collection 子目录和 `collection_name_mapping.json`；不要只备份映射文件。
- SiliconFlow Embedding 兼容接口要求 `OpenAIEmbeddings(check_embedding_ctx_length=False)`，避免 LangChain 将中文转换成接口不接受的 token-id 数组。
- 文档解析为空的 PDF 可能是扫描版/图片型 PDF；需要提示 OCR、多模态权限或上传可复制文本版本。
- 多模态、reranker、Web 搜索等增强能力失败时，应降级而不是中断主流程。
- Agent 工具曾出现误建议安装 `nltk` 的问题；代码工具应优先使用标准库或项目已有依赖。具体根因细节见 `BUG_LOG.md`，当前状态：待确认。
- Agent 曾因 LangChain `verbose` API 不兼容出现 500；涉及 AgentExecutor 或 LangChain 版本变化时要先看相关测试。当前状态：待确认。
- 后端响应头会带 `X-Request-ID` 和 `X-Process-Time-Ms`；排查前端报错时优先用 request id 搜索 `logs/app.log`。

## 前端反馈与 CSS

- 页面级反馈不得直接使用 `st.info`、`st.warning`、`st.success`、`st.error`、`st.progress`、`st.spinner`、`st.balloons`。使用 `render_status_notice()` 或 `st.toast()`。
- `tests/test_frontend_ui_contracts.py` 防止默认大色块、默认进度条、旧上传列表、旧侧边栏菜单回潮。
- CSS 体积较大，组合 CSS 当前量级约 200 KB。只清理确认无调用的孤儿规则或明确重复覆盖，不要大拆结构。
- 样式加载顺序是功能的一部分：变量先行，深色最终覆盖靠后，移动端最终覆盖最后。
- SVG/Material 图标在部分 Streamlit 组合中会空白；稳定做法是 CSS mask 或纯 CSS 图形。

## 编码与 Windows 环境

- PowerShell `Get-Content` 可能把中文显示成乱码。判断文件真实内容时，使用 Python `Path(...).read_text(encoding="utf-8")`。
- `py_compile` 可能遇到锁定的 `__pycache__`，优先设置临时 `PYTHONPYCACHEPREFIX`。
- 不要跨 shell 拼接破坏性文件操作；Windows 删除/移动必须谨慎使用 PowerShell 原生命令。

## 运行与密钥

- 长期运行后端优先使用 `start_backend_stable.ps1`，不要在生产或长时间使用时启用 `--reload`。
- 不要在日志、截图、测试输出或提交记录中暴露 `LLM_API_KEY`、`TAVILY_API_KEY`、`API_TOKEN`。
- 启用 `API_TOKEN` 后，前端、curl、评测脚本都必须携带同一个 token；评测脚本可使用 `--api-token` 或环境变量 `API_TOKEN`。
- Tavily 未配置或失败时应降级 DuckDuckGo；调试时看 Agent debug 中的 provider、attempts 和 fallback 状态。

## 待确认

- `vector_store.restore.tmp` 的用途和是否可删除。
- `chroma_db_backup_*`、`chroma_db_dim384_*`、`chroma_export_*.json` 是否仍需要长期保留。
- `.runtime_logs/`、`.runlogs/`、`logs/` 中哪些日志属于当前运行必需，哪些只是历史排障产物。
