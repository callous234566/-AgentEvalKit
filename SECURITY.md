# Security Policy / 安全政策

Personal RAG Assistant is a local personal RAG assistant. Most security risks come from accidentally publishing local data, API keys, logs, or evaluation artifacts.

Personal RAG Assistant 是一个本地个人 RAG 助手，主要安全风险来自误提交本地数据、API key、日志或评测产物。

## Do Not Publish / 请勿公开提交

- `.env`
- `LLM_API_KEY`, `TAVILY_API_KEY`, `API_TOKEN`, Bearer tokens
- `chroma_db/`
- `logs/`
- `data/`
- `.cache/`, `.pytest_cache/`, `__pycache__/`
- `eval/rag_eval_report.json`
- `eval/agent_eval_report.json`
- private documents or screenshots containing private content

## Release Safety Checks / 发布前安全检查

```powershell
python scripts\check_backend_release.py --api-base http://127.0.0.1:8000
git ls-files | rg "(^\.env$|^chroma_db/|^logs/|^data/|eval/(rag|agent)_eval_report\.json)"
```

The release check scans tracked files for unsafe local artifacts and secret-like values.

## Reporting Security Issues / 报告安全问题

If you find a security issue, please do not open a public issue with secrets or private data. Use a private channel if available, or open a minimal public issue without sensitive details and ask for a private follow-up path.

如果发现安全问题，请不要在公开 issue 中粘贴密钥、日志、私有文档或真实向量库内容。可以先提交不含敏感细节的最小 issue，再约定私下沟通方式。
