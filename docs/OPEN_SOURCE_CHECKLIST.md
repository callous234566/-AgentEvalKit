# Open Source Release Checklist / 开源发布检查清单

Use this checklist before publishing or refreshing the GitHub repository.

发布或刷新 GitHub 仓库前，建议按这份清单检查一次。

## Repository Hygiene / 仓库卫生

- [ ] `README.md` renders correctly on GitHub.
- [ ] Screenshots do not contain secrets, private paths, private documents, or `.env` values.
- [ ] `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` exist.
- [ ] Issue templates and PR template are visible in `.github/`.
- [ ] GitHub Actions CI is present and scoped to lightweight checks.

## Secret and Data Safety / 密钥与数据安全

- [ ] `.env` is not tracked.
- [ ] `chroma_db/` is not tracked.
- [ ] `logs/`, `data/`, caches, and sessions are not tracked.
- [ ] `eval/rag_eval_report.json` and `eval/agent_eval_report.json` are not tracked.
- [ ] Private knowledge base documents are not tracked.
- [ ] Only sanitized demo docs under `zhishiku/demo_*.md` are included.

## Commands / 检查命令

```powershell
python scripts\check_backend_release.py --api-base http://127.0.0.1:8000
git ls-files | rg "(^\.env$|^chroma_db/|^logs/|^data/|eval/(rag|agent)_eval_report\.json|产品需求与功能灵感)"
```

The second command should produce no output.

## Eval and Tests / 评测与测试

```powershell
python -m json.tool eval\eval_cases.json
python -m json.tool eval\agent_eval_cases.json
python -m pytest tests\test_maintenance_smoke.py tests\test_agent_eval.py tests\test_frontend_ui_contracts.py -q
```

Optional real local eval:

```powershell
python eval\rag_eval.py --api-base http://127.0.0.1:8000 --output-json eval\rag_eval_report.json
python eval\agent_eval.py --api-base http://127.0.0.1:8000 --output-json eval\agent_eval_report.json
```

Do not commit generated eval reports.
