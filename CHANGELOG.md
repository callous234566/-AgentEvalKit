# Changelog

All notable changes for this project are recorded here.

## v0.1.0 - 2026-07-04

Initial public release of **Personal RAG Assistant**, a local-first personal RAG knowledge base assistant.

### Included

- End-to-end RAG workflow: upload, parse, split, embed, persist to Chroma, retrieve, generate, and cite sources.
- Hybrid retrieval with vector search, BM25, keyword candidates, rerank, contextual compression, and source score traces.
- Streamlit workspace for knowledge bases, uploads, chat, sources, document management, settings, and Agent debug.
- Agent layer with local knowledge search, Tavily/DuckDuckGo Web fallback, restricted Python tool, routing diagnostics, and evidence summaries.
- Request-id diagnostics across backend responses, logs, frontend error messages, and eval reports.
- RAG eval and Agent eval baselines with structured failure reasons.
- GitHub Actions lightweight CI, issue templates, PR template, security policy, contribution guide, and release hygiene check.

### Not Included

- Real `.env` files, API keys, bearer tokens, private settings, local `chroma_db/`, logs, sessions, caches, backups, or eval reports.
- Private knowledge base documents or private source text.
