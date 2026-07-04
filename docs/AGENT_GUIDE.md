# Agent 能力说明与使用示例

本项目的 Agent 不是用来替代普通 RAG 主链路，而是作为增强层：在需要时调用本地知识库、Web 搜索或受限 Python 工具，并把工具选择、证据来源和失败降级过程完整记录到 debug 信息中。

## 当前能力

- **本地知识库检索**：通过 `search_knowledge_base` 查询当前知识库，适合回答上传资料、项目文档、学习笔记和论文资料相关问题。
- **Web 搜索补充**：通过 Tavily 搜索实时信息；Tavily 未配置或失败时，可降级到 DuckDuckGo。
- **受限 Python 工具**：用于轻量计算、格式转换和标准库级别的数据整理；危险文件、网络、系统命令类输入会被拦截。
- **本地优先兜底**：本地资料类问题如果 Agent 没有调用本地检索，会自动补一次 `search_knowledge_base`。
- **执行路由约束**：`routing_decision` 会根据问题类型生成 `allowed_tools`、`preferred_tool` 和 `strong`，减少本地问题误用 Web 或代码工具。
- **失败降级**：本地资料类 Agent 执行失败时，`/agent` 会 fallback 到普通 RAG 问答，并在 `debug_info` 中记录 `fallback_reason`、`fallback_used=rag_qa` 和 `fallback_sources`。
- **统一证据摘要**：`evidence_summary` 汇总本地/Web/代码证据使用情况；`evidence_items` 统一表示本地片段、网页结果和代码输出。

## Debug 字段

调试开启后，`/agent` 响应中的 `debug_info` 重点关注这些字段：

- `tool_policy`：问题分类、是否本地优先、是否允许 Web。
- `routing_decision`：允许工具、首选工具、是否强约束。
- `tool_sequence`：实际工具调用顺序。
- `tool_calls`：工具调用输入、输出摘要和耗时。
- `tool_budget`：工具调用次数和策略违规提醒。
- `source_layers`：本地、Web、代码来源组合模式。
- `search_trace`：Web provider、attempts、fallback 和结果数。
- `evidence_summary`：统一证据摘要，适合前端调试面板优先展示。
- `evidence_items`：统一证据列表，可用于后续证据抽屉。
- `fallback_reason` / `fallback_used`：Agent 失败或策略兜底原因。

## 使用示例

建议用脱敏示例知识库，先上传：

- `zhishiku/demo_rag_workbench.md`
- `zhishiku/demo_agent_debug.md`

然后按下面顺序体验：

1. **本地资料问题**
   - 问：`Agent 为什么应该优先检索本地知识库？`
   - 预期：优先调用 `search_knowledge_base`，debug 中 `routing_decision.category=local_knowledge`。

2. **实时 Web 问题**
   - 问：`2026 年 Python 最新版本是什么？`
   - 预期：允许 `search_web`，debug 中展示 `search_trace.provider`、`attempts` 和 `fallback_used`。

3. **本地 + Web 混合**
   - 问：`结合本项目资料和最新版本信息，说明 LangChain Agent 的变化。`
   - 预期：回答按“本地资料 / 外部搜索补充 / 来源提示”分层，避免 Web 内容覆盖本地资料。

4. **失败降级**
   - 模拟 Agent 执行失败或 Web 失败。
   - 预期：本地资料类问题 fallback 到普通 RAG；实时类问题给出友好失败并保留 request id 与 trace。

5. **安全边界**
   - 说明代码工具只适合标准库级轻量任务，不执行文件读取、网络请求、系统命令或安装新依赖。

## 评测与测试

Agent 相关护栏分三层：

- `eval/agent_eval_cases.json`：记录本地优先、实时 Web、混合来源、Web fallback 和标准库代码回答等评测场景。
- `eval/agent_eval.py`：读取 Agent eval cases，调用 `/agent`，输出路由、工具调用、debug 字段和失败原因报告。
- `tests/test_agent_debug.py`：验证路由、工具预算、evidence summary、evidence_items、fallback reason 和 Agent eval case schema。
- `tests/test_tools_tavily.py`：验证 Tavily/DuckDuckGo trace、Web fallback 和 Python 工具安全拦截。

当前 Agent eval case：

- `local_question_must_start_with_kb`
- `realtime_question_allows_web`
- `mixed_local_web_requires_layered_answer`
- `web_failure_keeps_search_trace`
- `code_task_no_new_dependency`

推荐发布前运行：

```powershell
D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_tools_tavily.py tests\test_main_endpoints.py -q
```

如需生成真实 Agent 评测报告：

```powershell
D:\anaconda3\envs\ai_project\python.exe eval\agent_eval.py --api-base http://127.0.0.1:8000 --collection-name 示例知识库 --output-json eval\agent_eval_report.json
```

`eval/agent_eval_report.json` 属于本地评测产物，公开仓库中不应提交。

## 当前边界

- Agent 不做复杂多智能体编排，优先保证本地 RAG 主链路稳定。
- 工具选择采用 prompt、启发式分类和 allowlist 约束组合，而不是让模型任意调用工具。
- Web 搜索结果作为补充证据，不覆盖本地知识库已有结论。
- `evidence_summary` 和 `evidence_items` 属于 debug 信息，普通回答正文不依赖这些字段。
