# 公开演示资料：Agent 与证据摘要

这是一份可公开上传到本项目的脱敏 Markdown 示例文档，用于演示 Agent 调试面板和证据摘要。

## Agent 本地优先

当问题属于当前知识库内容时，Agent 应优先调用本地知识库检索工具。只有当问题需要实时信息、网页资料或外部补充时，才应该使用 Web 搜索。

本地优先可以减少不必要的联网搜索，也能让回答更贴近用户上传的资料。

## Web 搜索降级

项目接入 Tavily 搜索工具，并保留 DuckDuckGo 作为 fallback。调试信息会记录 provider、attempts、fallback_used 和 result_count。

如果 Web 搜索失败，系统应该给出友好说明，并保留 request id，方便在日志中定位问题。

## Evidence Summary

Agent debug 中的 evidence summary 用来统一说明本次回答使用了哪些证据：

- local_used：是否使用本地知识库。
- web_used：是否使用外部搜索。
- code_used：是否使用 Python 工具。
- local_fallback_used：是否触发本地优先兜底。
- policy_violations：是否出现策略提醒。

这个摘要适合面试演示，因为它能快速解释 Agent 为什么调用某个工具，以及最终答案依赖哪些证据。

## 演示问题

- Agent 为什么应该优先检索本地知识库？
- Tavily 搜索失败时系统应该如何降级？
- evidence summary 可以帮助排查哪些问题？
