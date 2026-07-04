# Codex Prompt: frontend-fix

用于让 Codex 修复或优化当前项目 Streamlit 前端。复制时按需删改括号内容。

```text
请修复当前项目的前端问题：[描述现象，最好附截图或页面位置]。

要求：
- 先读取 `AGENTS.md`、`PROJECT_MAP.md`、`docs/KNOWN_ISSUES.md`，不要凭记忆改。
- 只做最小必要改动，不要大范围重构 UI。
- 不要破坏侧边栏三点菜单、上传队列删除、固定输入框、最新回答入口、深浅色切换。
- 页面级反馈不要使用 `st.info/warning/success/error/progress/spinner/balloons`，使用 `render_status_notice()` 或 `st.toast()`。
- 如果问题可能是 session state 或后端 API 状态导致，不要只改 CSS，要定位真实原因。
- 前端小改后不用重启服务；我会刷新验证。
- 不要新增依赖，不要 reset/revert，不要清理未追踪文件。
- 修改后更新 `BUG_LOG.md`。

建议验证：
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q`
- `$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-ui-pycache'; D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\components.py ui\styles\__init__.py`
- `git diff --check -- <touched-files>`
```

## 适用场景

- UI 对齐、按钮、三点菜单、上传队列、聊天输入区、深浅色、状态提示、引用卡片等问题。

## 不适用场景

- 后端检索质量问题。
- Chroma 数据损坏。
- 模型 API 失败。
- 依赖升级。
