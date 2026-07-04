# Contributing / 贡献指南

Thanks for your interest in AgentEvalKit. This repository is primarily an interview-ready open-source demo, so contributions should keep the project easy to run, explain, and verify.

感谢你关注 AgentEvalKit。本仓库定位为面试展示型开源项目，贡献应优先保持项目易运行、易理解、易验证。

## Local Setup / 本地启动

```powershell
conda create -n ai_project python=3.11
conda activate ai_project
pip install -r requirements.txt
Copy-Item .env.example .env
```

Then fill in `.env` with your own model credentials and start:

```powershell
.\start_backend_stable.ps1
.\start_frontend.ps1
```

## Development Rules / 开发规则

- Do not commit `.env`, API keys, Chroma data, logs, sessions, caches, private documents, or eval reports.
- Do not change public API shapes without updating README and tests.
- Keep RAG and Agent changes small, observable, and covered by tests.
- Use existing modules and patterns before adding new abstractions.
- New dependencies must be justified and added to `requirements.txt`.

## Recommended Checks / 推荐检查

```powershell
python scripts\check_backend_release.py --api-base http://127.0.0.1:8000
python -m pytest tests\test_maintenance_smoke.py tests\test_agent_eval.py tests\test_frontend_ui_contracts.py -q
python -m json.tool eval\eval_cases.json
python -m json.tool eval\agent_eval_cases.json
```

For larger backend or Agent changes, also run focused tests:

```powershell
python -m pytest tests\test_main_endpoints.py tests\test_vector_store.py tests\test_qa_chain.py -q
python -m pytest tests\test_agent_debug.py tests\test_tools_tavily.py tests\test_eval.py -q
```

## Pull Requests / PR 要求

Before opening a PR:

- Describe what changed and why.
- List the tests you ran.
- Confirm no secrets or local data are committed.
- Include screenshots for UI changes.
- Mention whether the change affects API, RAG, Agent, eval, or dependencies.
