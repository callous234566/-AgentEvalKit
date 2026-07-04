# Codex Prompt: rag-debug

用于让 Codex 排查 RAG 检索、分块、Embedding、重排、生成和 Agent 问答问题。

```text
请排查当前项目 RAG 问答问题：[描述问题、知识库、问题文本、期望答案、实际答案/错误]。

要求：
- 先读取 `AGENTS.md`、`PROJECT_MAP.md`、`docs/KNOWN_ISSUES.md`、`RAG技术详解.md`。
- 先判断问题在上传解析、分块、向量入库、检索召回、重排压缩、生成提示词、Agent 工具调用中的哪一段。
- 不要直接改 prompt 或阈值掩盖问题，要先定位根因。
- SiliconFlow Embedding 使用 `OpenAIEmbeddings(check_embedding_ctx_length=False)`；不要让中文输入变 token-id 数组。
- 文档解析模块变更后，要考虑 PDF、TXT、DOCX、Markdown。
- 多模态、reranker、Web 搜索失败时应降级并给友好提示。
- 不要在真实 `chroma_db/collection_name_mapping.json` 上做临时测试。
- 不要新增依赖，除非先做兼容性分析并同步 `requirements.txt`。
- 修改后更新 `BUG_LOG.md`，必要时同步 `RAG技术详解.md`。

建议验证：
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_qa_chain.py tests\test_text_splitter.py -q`
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_document_loader.py tests\test_reranker.py tests\test_tools_tavily.py -q`
- `python eval\rag_eval.py --api-base http://127.0.0.1:8000`（后端运行且适合评估时）
- `git diff --check -- <touched-files>`
```

## 适用场景

- 检索不到相关文档。
- 中文知识库、中文问题、指代问题表现差。
- 上传成功但问答没有引用。
- Reranker、多模态、Agent 工具调用异常。

## 不适用场景

- 纯前端对齐、按钮、颜色问题。
- 纯服务启动或 CORS 问题。
- 需要破坏性重建向量库但未明确授权。
