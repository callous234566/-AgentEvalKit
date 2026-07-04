# 脱敏演示包

本目录记录公开 GitHub 版本推荐使用的演示资料和演示路线。演示包不包含真实 Chroma、日志、缓存、密钥、私有知识库正文或真实 eval report。

Agent 能力、边界和调试字段说明见 `docs/AGENT_GUIDE.md`。

## 示例资料

建议在全新知识库中上传以下脱敏文档：

- `zhishiku/demo_rag_workbench.md`
- `zhishiku/demo_agent_debug.md`

这两份文档覆盖本地 RAG、混合检索、BM25、引用来源、未知问题拒答、Agent 本地优先、Tavily fallback 和 evidence summary。

## 推荐演示路线

1. 创建知识库，例如 `公开演示知识库`。
2. 上传两份 `zhishiku/demo_*.md` 示例文档。
3. 提问：`BM25 在 RAG 检索中有什么作用？`
4. 展示回答下方的引用来源、分数和片段证据。
5. 提问：`这些资料是否说明了火星基地厨房的虚构配置项？`
6. 展示未知问题拒答能力。
7. 打开 Agent debug，提问：`Agent 为什么应该优先检索本地知识库？`
8. 展示 evidence summary、tool sequence、source layers 和 request id 排障链路。

## 发布前注意

- 不提交 `.env`、`logs/`、`.cache/`、`chroma_db/`、`eval/rag_eval_report.json`。
- 不把本地真实知识库截图放进 README。
- 如果要展示 eval 结果，只写脱敏摘要，不提交私有 report 原文。
