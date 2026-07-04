# Codex Prompt: backend-debug

用于让 Codex 排查当前项目 FastAPI 后端、API、服务稳定性和状态同步问题。

```text
请排查当前项目后端问题：[描述 API、日志、错误码、复现步骤]。

要求：
- 先读取 `AGENTS.md`、`PROJECT_MAP.md`、`docs/KNOWN_ISSUES.md`，不要猜。
- 先复现或找到最接近的失败信号，再定位根因。
- 只做最小必要改动，不要重构无关代码。
- 不要吞异常、跳过校验或删除核心逻辑来伪装修复。
- 涉及创建、删除、重命名、启用禁用等数据状态时，前端状态必须与后端 API 同步。
- 不要在真实 `chroma_db/collection_name_mapping.json` 上做临时测试。
- 不要新增依赖，除非先做兼容性分析并同步 `requirements.txt`。
- 不要 reset/revert，不要清理未追踪文件。
- 修改后更新 `BUG_LOG.md`。

建议验证：
- `Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health`
- `$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'personal-rag-backend-pycache'; D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py config.py rag\api_client.py`
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_api_client.py tests\test_main_endpoints.py -q`
- `git diff --check -- <touched-files>`
```

## 适用场景

- API 500/401/404。
- 上传、删除、重命名、启用禁用没有同步。
- 服务启动、日志、CORS、API token、请求超时问题。

## 不适用场景

- 纯 UI 视觉问题。
- 只需要写文档或提示词。
- 需要真实删除用户数据但未明确授权。
