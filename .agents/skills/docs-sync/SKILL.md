---
name: docs-sync
description: Use in this personal-rag-assistant repo when synchronizing durable project documentation after code, API, RAG, frontend, dependency, or workflow changes. Trigger for updating AGENTS.md, BUG_LOG.md, README.md, PROJECT_MAP.md, docs/KNOWN_ISSUES.md, docs/GLOSSARY.md, docs/codex-prompts/*.md, RAG技术详解.md, or 项目维护手册.md based on real repository changes. Do not use for business-code implementation itself, short-lived notes, speculative roadmap content, or documentation that would require inventing unverified project behavior.
---

# Docs Sync

Keep long-lived project understanding accurate without inventing details.

## Workflow

1. Read current repository files before writing. Prefer `rg --files` and targeted reads.
2. Choose the right document:

- Durable Codex/project rules: `AGENTS.md`.
- Change history and user-visible fixes: `BUG_LOG.md`.
- Architecture and entry points: `PROJECT_MAP.md`.
- Repeated pitfalls and pending risks: `docs/KNOWN_ISSUES.md`.
- Terminology: `docs/GLOSSARY.md`.
- Reusable task prompts: `docs/codex-prompts/*.md`.
- Public usage/API changes: `README.md`.
- RAG internals: `RAG技术详解.md`.
- Maintenance backlog/route: `项目维护手册.md`.

3. Mark uncertain facts as `待确认`; do not guess.
4. Keep short-term UI snapshots out of long-term docs unless they became stable rules.
5. Verify Chinese files with UTF-8 reads when PowerShell display looks garbled:

```powershell
D:\anaconda3\envs\ai_project\python.exe -c "from pathlib import Path; [Path(p).read_text(encoding='utf-8') for p in ['AGENTS.md','BUG_LOG.md']]"
```

6. Run diff whitespace checks on touched docs:

```powershell
git diff --check -- AGENTS.md BUG_LOG.md PROJECT_MAP.md docs
```

## Guardrails

- Do not modify business code while doing docs sync.
- Do not add dependencies.
- Do not reset, revert, or clean untracked files.
- Prefer concise durable rules over long narrative recaps.
