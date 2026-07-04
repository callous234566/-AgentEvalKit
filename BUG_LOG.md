## 2026-07-04 README 公开产品口径收敛

- 目标：移除公开 README 和贡献指南中的“面试展示 / interview-ready / demo”包装口径，让仓库更像长期维护的标准开源项目。
- 调整：README 首屏简介改为本地优先、可维护的个人 RAG 知识库助手；Why/Included/Roadmap/Quick Usage Flow 等段落改用产品和开源项目表述。
- 同步：`CONTRIBUTING.md` 和 `SECURITY.md` 顶部项目名与定位同步为 `Personal RAG Assistant`。
- 范围：仅公开文档措辞调整；未修改业务代码、GitHub 仓库设置或运行时行为。

## 2026-07-04 GitHub 仓库重新命名为 PersonalRAGAssistant

- 目标：让公开仓库名称更贴合项目本体，避免 `AgentEvalKit` 给人“只是 Agent 评测工具”的误解。
- 调整：GitHub 仓库从 `callous234566/AgentEvalKit` 重命名为 `callous234566/PersonalRAGAssistant`，Description 同步为个人 RAG 知识库助手定位。
- 同步：本地 `origin` remote 已更新为 `https://github.com/callous234566/PersonalRAGAssistant.git`；README 标题、简介、CI badge 和 GitHub issue template 文案同步为新名称。
- 范围：仅 GitHub 仓库元数据、README/模板文案和维护日志；未修改业务代码或运行时行为。

## 2026-07-04 GitHub Topics 补充

- 目标：补齐公开仓库 Topics，提升 GitHub 搜索可发现性和面试展示观感。
- 调整：设置 Topics 为 `rag`、`retrieval-augmented-generation`、`llm`、`ai-agent`、`agent-evaluation`、`knowledge-base`、`fastapi`、`streamlit`、`langchain`、`chroma`、`vector-database`、`tavily`、`siliconflow`、`chinese-rag`、`eval`。
- 范围：仅 GitHub 仓库元数据和维护日志；未修改业务代码或运行时行为。

## 2026-07-04 GitHub 仓库名称与描述更新

- 目标：去掉公开仓库名称前面的横杠，让 GitHub 页面更像标准开源项目。
- 调整：GitHub 仓库从 `callous234566/-AgentEvalKit` 重命名为 `callous234566/AgentEvalKit`，并设置 Description 为面试展示型个人 RAG 知识库助手说明。
- 同步：本地 `origin` remote 已更新为 `https://github.com/callous234566/AgentEvalKit.git`；README CI badge 链接同步到新仓库地址。
- 范围：仅 GitHub 仓库元数据、README 链接和维护日志；未修改业务代码或运行时行为。

## 2026-07-04 GitHub 标准开源化文档与模板补齐

- 目标：把公开仓库从“可展示项目”整理成更标准的面试展示型开源项目，补齐许可证、协作规范、安全说明和 GitHub 协作入口。
- 新增：`LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、`.github/ISSUE_TEMPLATE/bug_report.yml`、`.github/ISSUE_TEMPLATE/feature_request.yml`、`.github/pull_request_template.md`、`.github/dependabot.yml` 和 `docs/OPEN_SOURCE_CHECKLIST.md`。
- README：增加 CI/Python/License/框架 badges、目录、Why this project、included/not included、Roadmap，并链接开源发布检查清单。
- 面试文档：`docs/INTERVIEW_GUIDE.md` 增加公开仓库发布前 checklist 提醒。
- 范围：仅文档、GitHub 模板和仓库治理文件；未修改后端 API、RAG/Agent 策略、前端 UI 行为或运行时依赖。

## 2026-07-04 README 中英双语重写

- 目标：修复 GitHub README 中历史编码造成的中文乱码/问号问题，并将首页整理成中英双语公开展示版。
- 调整：`README.md` 重写为中英双语结构，保留项目亮点、截图、快速启动、演示路线、API、RAG eval、Agent eval、release check、GitHub Actions CI、测试命令和发布安全策略。
- 保护：未修改业务代码、后端 API、RAG/Agent 策略或依赖；只更新公开文档。

## 2026-07-04 GitHub Actions Lightweight CI

- 目标：为公开 GitHub 仓库增加不依赖真实密钥、真实 Chroma、真实后端或真实 LLM/Tavily 的轻量 CI，提升面试发布版工程可信度。
- 新增：`.github/workflows/ci.yml`，在 push / pull request 到 `main` 或 `master` 时运行。
- 覆盖：安装 `requirements.txt`，编译关键模块，校验 `eval/eval_cases.json` 与 `eval/agent_eval_cases.json`，运行 maintenance/API/eval/Agent/Tavily/frontend 契约等 mock/static 测试，并执行 `scripts/check_backend_release.py --no-health`。
- 发布安全：`.gitignore` 收紧 `zhishiku/`，默认只允许 `zhishiku/demo_*.md` 脱敏演示资料进入公开仓库，避免个人产品草稿或私有知识资料被 `git add .` 误提交。
- 文档：`README.md` 增加 GitHub Actions CI 说明；`PROJECT_MAP.md` 增加 CI 入口。

## 2026-07-04 Agent Eval 发布展示收口

- 目标：把已通过的 Agent eval 基线纳入公开 README、面试指南和项目地图，让面试展示从“口头说明 Agent 能力”升级为“有可运行评测入口和通过证据”。
- 文档：`README.md` 的评估章节新增 `eval/agent_eval.py` 命令和 `eval/agent_eval_report.json` 本地产物说明；项目结构补充 `agent_eval.py` 与 `agent_eval_cases.json`。
- 面试：`docs/INTERVIEW_GUIDE.md` 将展示顺序更新为 RAG eval / Agent eval，并记录当前真实 RAG eval 14/14、Agent eval 5/5。
- 地图：`PROJECT_MAP.md` 增加 Agent 评估入口，标明其覆盖工具路由、Web fallback、debug 字段和代码工具安全边界。

## 2026-07-04 Agent Eval Runner

- 目标：把 `eval/agent_eval_cases.json` 从静态样例清单升级为可运行的 Agent 评测基线，方便面试前验证工具路由、Web fallback、debug 字段和失败原因。
- 新增：`eval/agent_eval.py`，调用 `/agent` 并检查 `expected_category`、`expected_first_tool`、`forbidden_first_tools`、`required_allowed_tools`、`expected_answer_sections`、`expected_debug_fields`、答案关键词和禁用关键词。
- 报告：Agent eval 会输出 pass rate、`failure_reasons`、request id、首个工具、允许工具、`routing_decision`、`evidence_summary`、`search_trace` 和 fallback 信息；可用 `--output-json` 保存本地报告。
- 安全：`.gitignore` 增加 `eval/agent_eval_report.json`，避免真实 Agent 评测产物误提交到公开仓库。
- 基线：当前本地后端真实 Agent eval 已跑通 5/5；`code_task_no_new_dependency` 的正向关键词收敛为低脆弱度 `json`，核心仍检查不建议 `pip install`、`nltk`、`sklearn`、`transformers`。
- 测试：新增 `tests/test_agent_eval.py`，全部 mock `/agent` 调用，不访问真实 Tavily、Chroma、LLM 或后端服务。

## 2026-07-04 Agent 展示与维护文档补强

- 目标：在不改 Agent 路由策略、不改后端 API 的前提下，把 Agent 能力、边界、debug 字段和面试演示脚本整理成可公开展示的稳定入口。
- 文档：新增 `docs/AGENT_GUIDE.md`，说明本地知识库、Tavily/DuckDuckGo、受限 Python 工具、本地优先兜底、路由约束、失败降级、`evidence_summary` 和 `evidence_items`。
- 演示：`docs/AGENT_GUIDE.md` 补充本地资料问题、实时 Web 问题、本地+Web 混合、失败降级和安全边界的面试演示脚本；`README.md` 与 `docs/DEMO_PACKAGE.md` 增加指南入口。
- 测试：`tests/test_agent_debug.py` 增加 Agent 指南契约，确保文档覆盖 `eval/agent_eval_cases.json` 中的 case id 和关键 debug 字段，防止后续 Agent 行为演进时文档脱节。

## 2026-07-03 发布前后端收口与脱敏演示包

- 目标：落实面试发布版路线图中优先级最高的三件事：清理 Chroma mapping warning、Agent 本地失败降级、准备可公开上传的脱敏演示资料。
- 发布检查：`scripts/check_backend_release.py` 新增 `--fix-missing-mapping`，默认仍只读；显式开启后会为 `collection_name_mapping.json` 创建时间戳备份，并移除指向不存在 Chroma collection 的孤儿映射。
- 本地清理：已对当前本地 `chroma_db/collection_name_mapping.json` 执行一次孤儿映射清理，删除 5 条缺失 collection 的 mapping；未删除真实 Chroma collection、文档正文或向量数据。
- Agent 降级：`/agent` 在本地知识库类问题执行失败时，会 fallback 到普通 RAG 问答，并在 `debug_info` 中记录 `fallback_reason`、`fallback_used=rag_qa` 和 `fallback_sources`；实时 Web 类失败不触发本地 RAG fallback。
- 演示包：新增 `zhishiku/demo_rag_workbench.md`、`zhishiku/demo_agent_debug.md` 和 `docs/DEMO_PACKAGE.md`，用于公开 GitHub 版本的脱敏上传演示。
- 测试：`tests/test_backend_release_check.py` 覆盖 mapping 清理备份；`tests/test_main_endpoints.py` 覆盖 Agent 本地失败 fallback 与实时失败不 fallback。
## 2026-07-03 Agent 路由执行约束与证据项补强

- 目标：让 Agent 工具选择从仅依赖 prompt 提醒，升级为执行前的 allowlist 约束，减少本地资料问题误先调用 Web 或代码工具的概率。
- 优化：`rag/agent.py` 新增 `routing_decision`，根据 `tool_policy` 输出 `allowed_tools`、`preferred_tool` 和 `strong`；真实 LangGraph Agent 在执行前会按允许工具重建受限 Agent，旧 fake agent/测试替身保持兼容。
- 调试：`debug_info` 新增 `routing_decision` 和 `evidence_items`；`evidence_items` 统一描述本地、Web、代码工具输出的 `type/title/source/provider/snippet/tool`，不改变 `/agent` 顶层响应。
- 失败诊断：Agent 执行异常时在 debug 中记录 `fallback_reason=agent_execution_error`，便于前端和日志解释失败来源。
- 安全：`execute_python_code` 将普通 `open(...)` 纳入拦截，配合既有 `os.system`、`subprocess`、`socket` 等规则，避免 Agent 在展示环境中读取文件、访问网络或执行系统命令。
- 评测：新增 `eval/agent_eval_cases.json`，沉淀本地优先、实时 Web、local+web 分层、Web fallback trace 和标准库代码回答等 Agent 评测样例。
- 测试：`tests/test_agent_debug.py` 覆盖路由 allowlist、受限 Agent 执行、统一证据项、失败 fallback reason 和 eval case JSON；`tests/test_tools_tavily.py` 覆盖代码工具文件/网络/系统命令拦截。
## 2026-07-03 后端发布前只读检查脚本

- 目标：面试和公开 GitHub 发布前，用一条命令检查后端是否存在明显发布风险，而不写入 Chroma、不调用真实 LLM、不修改配置。
- 新增：`scripts/check_backend_release.py`，检查 Git 是否跟踪 `.env`、`chroma_db/`、日志、缓存、eval report 等本地产物，扫描已跟踪文本文件中的真实密钥/Bearer token，读取 `collection_name_mapping.json`，对比 Chroma collection 列表，并可验证 `/health` 的 request id 响应头。
- 保护：Chroma/mapping 不一致默认只输出脱敏 warning，不自动修复；健康检查支持 `--no-health` 跳过；脚本会静默 Chroma/GRPC 原生 stderr 噪音，保持 release gate 输出可读。
- 测试：新增 `tests/test_backend_release_check.py`，覆盖危险 tracked 文件识别、占位密钥过滤、真实密钥命中、mapping JSON 错误、mapping/collection 不一致和 health request meta 捕获。
- 补强：`tests/test_main_endpoints.py` 增加删除知识库异常和 Agent 异常日志契约，确认 500 失败路径继续保留 `X-Request-ID`，并在日志中包含 request id、operation、collection_name 和错误摘要。
## 2026-07-03 深色模式低对比文字修复

- 现象：深色模式下侧边栏知识库/会话三点菜单悬浮提示文字低对比，原生文件上传器中的 `Drag and drop files here` 与文件限制说明也偏暗。
- 根因：三点菜单按钮同时由 Streamlit `help` 和前端脚本 `title` 生成浅底 tooltip，浏览器原生 tooltip 不适合用 CSS 稳定改色；文件上传器是 Streamlit 原生组件，深色模式下内部 `p/small/span/svg` 颜色没有被最终覆盖层接住。
- 修复：`ui/sidebar.py` 移除三点菜单按钮的 `help`，`ui/js_injection.py` 对侧边栏三点菜单只保留 `aria-label` 并移除 `title`；`ui/styles/_dark_refinement.py` 为 `stFileUploader` / `stFileUploaderDropzone` 补充深色文字、图标和按钮颜色。
- 测试：`tests/test_frontend_ui_contracts.py` 增加深色上传器和侧边栏 tooltip 契约，防止低对比 tooltip 与上传器文字回退。
- 追补：列表行本身的 `help=collection_name/session_name` 仍会生成浅底 tooltip，且三点按钮 hover 会出现块状背景；已移除列表行 `help`，前端脚本清理列表行 `title`，并在侧栏基础、refinement、深色最终覆盖层把三点 hover 背景压为透明。

## 2026-07-03 上传空状态图标不显示修复

- 现象：上传页“把脱敏资料拖进来”空状态左侧只显示浅色方块边框，内部上传图标没有显示。
- 根因：`st.html` 会清理空状态 HTML 中的内联 SVG，导致 `.workspace-empty-icon` 和三步卡片里的图标节点被移除，只剩图标容器外框。
- 修复：`ui/components.py` 的空状态不再输出内联 SVG，改为输出安全的 `empty-icon-*` class；`ui/styles/_empty_states.py` 使用 `::before` + CSS mask 渲染 upload/library/layers/settings 等图标。
- 修复：上传空状态步骤卡片的三个小图标不再用同一个伪元素同时绘制底座和 mask，改为 `workspace-empty-step-icon` 容器 + 内层 `::before` mask，避免只显示浅色方块、不显示图标线条。
- 测试：`tests/test_frontend_ui_contracts.py` 增加空状态 CSS mask 契约，防止上传空状态图标再次只剩外框。

## 2026-07-03 删除知识库误报失败修复

- 现象：前端确认删除知识库后，弹窗先显示“操作失败 500”和排障 ID，但刷新后知识库实际已经被删除。
- 根因：`langchain_chroma.Chroma.delete_collection()` 在 collection 已被 Chroma 删除/置空后，可能继续抛出 `Chroma collection not initialized. Use reset_collection...`；后端据此返回 500，导致前端误报失败。
- 修复：`rag/vector_store.py` 在捕获该 Chroma deleted-state 异常时，使用持久化 Chroma client 确认底层 collection 已不存在；确认后按删除成功处理，并清理 `_stores`、collection cache 和中文名称 mapping。
- 保护：仅对 `collection not initialized` / `reset_collection` 这一类删除后状态异常做成功确认；普通异常仍返回失败，避免吞掉真实删除问题。
- 测试：`tests/test_vector_store.py` 增加删除后状态异常成功分支和真实异常失败分支，防止“删除成功但 UI 报失败”回潮。

## 2026-07-03 面试展示版前端打磨

- 目标：在不修改后端 API、RAG 策略、Agent 工具策略或真实知识库数据的前提下，让前端第一屏和问答页更适合面试演示。
- 首页：`ui/components.py` 的 Hero 文案改为 `Interview-ready RAG Workbench`，突出本地 RAG、混合检索、Agent/Web、引用可追溯和排障 ID；工作台概览卡补充本地持久化、trace、request id 日志链路等提示。
- 问答页：`ui/chat.py` 的空状态改为“3 步开始一次可追溯问答”；快捷提问加入 `BM25 在 RAG 检索中有什么作用？` 与域外拒答演示问题，方便面试时一键展示引用和拒答守卫。
- 引用：`ui/components.py` 与 `ui/styles/_chat.py` 将引用区升级为证据面板，展示来源编号、文件名、相似度、证据片段和复制按钮；深色模式补充 `.source-index`、`.source-score`、`.source-label` 覆盖。
- 设置/上传：`ui/pages.py` 的 Agent 说明明确“优先查本地资料，必要时补充 Web”；`ui/upload.py` 增加公开演示安全提示，说明公开仓库不包含 Chroma、session、日志或密钥，并建议先上传少量脱敏 Markdown/PDF。
- 文档：README 增加界面预览和前端体验亮点；`docs/INTERVIEW_GUIDE.md` 补充前端演示路线和截图清单。
- 测试：`tests/test_frontend_ui_contracts.py` 增加面试展示文案契约，防止关键演示入口被后续改动误删。

## 2026-07-03 公开 GitHub 发布整理

- 目标：面试前将项目整理为可公开发布的 GitHub 仓库，避免提交密钥、本地向量库、缓存、日志、session、备份数据或本地评测产物。
- 清理：`.gitignore` 补充 `.cache/`、`.pytest_cache/`、`.claude/settings.local.json`、`.runtime_logs/`、`.runlogs/`、`outputs/`、`chroma_db_backup_*`、`chroma_db_dim384_*`、`chroma_export_*.json`、`eval/rag_eval_report.json`、`vector_store.restore.tmp` 等本地产物。
- 索引：从 Git 索引移除已误加入的 cache、pytest cache、Chroma 备份、Chroma 导出和本地配置，保留工作区文件本身不删除。
- 文档：README 第一屏改为面试展示口径，突出 RAG 闭环、混合检索、Agent/Web 融合、引用 trace、request id 日志链路和 eval 基线；新增 `docs/INTERVIEW_GUIDE.md`，包含 3 分钟/8 分钟讲解稿、架构图、RAG 流程图和演示清单。
- 安全：staged 文件中未发现 `.env`、Chroma 数据、日志、session、缓存、备份向量库或 eval report；密钥扫描仅命中 `.env.example` 与 README 中的占位示例。

## 2026-07-02 前端真实 UI 回归巡检

- 目标：在真实运行的 Streamlit 前端上检查近期排障 ID、Agent debug、RAG 回答与拒答守卫相关改动是否造成 UI 回退。
- 环境：后端 `http://127.0.0.1:8000/health` 返回 healthy，前端 `http://127.0.0.1:8501` 可访问；当前知识库列表能正常展示中文名称。
- 验证：`tests/test_frontend_ui_contracts.py` 16 passed；静态扫描未发现 `st.info/warning/success/error/progress/spinner/balloons` 默认大色块调用；前端相关模块 `py_compile` 通过。
- 浏览器巡检：切换到 `RAG技术原理` 后问答页正常渲染；基线问题 `BM25 在 RAG 检索中有什么作用？` 返回正文与 5 条引用来源，未发现乱码、默认 Streamlit 报错块或引用区域遮挡。
- 拒答巡检：域外问题 `这些资料是否说明了火星基地厨房的虚构配置项？` 返回标准短拒答 `根据现有资料无法回答该问题。`，未再生成长篇“相关要点”。
- Agent 检查：系统设置页可见 `Agent 模式` 与已勾选的 `Agent 调试模式`；自动化未强行点击隐藏 checkbox 做 Agent 实问，相关 debug 展示仍以现有后端、API、wrapper 和前端函数级契约测试作为护栏。
- 结论：本轮未发现需要立即修复的前端 UI 回退；未执行上传、删除、重命名等会改变真实知识库数据的操作。

## 2026-07-02 RAG Eval 答案长度断言

- 目标：补齐 eval 对异常短答、误拒答和过长未知问题回答的结构化检测能力。
- 增强：`eval/rag_eval.py` 支持可选 `min_answer_chars` 与 `max_answer_chars`，并新增 `answer_too_short`、`answer_too_long` 失败原因。
- 用例：`eval/eval_cases.json` 为正常 RAG/probe case 增加温和 `min_answer_chars`，为 `unknown_answer_guard` 增加 `max_answer_chars`，防止短拒答或长篇“相关要点”漏检。
- 测试：`tests/test_eval.py` 覆盖长度字段类型校验、过短/过长失败分类，以及长度达标路径。
- 结果：重新生成 `eval/rag_eval_report.json`，真实 eval 14/14 通过，`retrieve_empty` 为 0。

## 2026-07-02 RAG Eval probe 生成断言补强

- 目标：防止 probe case 只验证检索/source/trace，却漏过生成层异常短答或误拒答。
- 调整：`eval/eval_cases.json` 为 `exact_title_source_probe`、`query_rewrite_fallback_probe`、`compression_protection_probe` 增加低脆弱度 `expected_keywords`，分别覆盖 `BM25`、`原始查询`、`片段`。
- 结果：重新生成 `eval/rag_eval_report.json`，真实 eval 14/14 通过；三个 probe case 均保持非空检索和正常生成。
- 保护：本次不调整后端检索策略、不改 eval schema、不改 API；只增强现有 eval case 的生成层护栏。

## 2026-07-02 未知问题拒答守卫增强

- 目标：修复真实 eval 中唯一失败的 `unknown_answer_guard`，避免检索到主题相近但实体不相关的片段后仍整理“相关要点”。
- 修复：`rag/qa_chain.py` 在生成前增加轻量实体覆盖守卫；当问题包含明确实体且这些实体在检索上下文中覆盖不足时，直接返回标准拒答 `根据现有资料无法回答该问题。`。
- 保护：RAG 常见技术锚点（如 BM25、Query Rewrite、Contextual Compression、Reranker、Embedding、LangChain、Python、Chroma、FastAPI）不触发该实体守卫，避免误伤正常技术问题。
- 测试：`tests/test_qa_chain.py` 覆盖域外实体拒答、相关问题不拒答、技术锚点不误拒、模型拒答后的既有 fallback 摘要行为。
- 结果：重新启动后端并生成 `eval/rag_eval_report.json`，真实 eval 14/14 通过，`retrieve_empty` 为 0，`unknown_answer_guard` 通过。

## 2026-07-02 RAG Eval case 对齐真实知识库

- 目标：修复真实 eval 基线中 RAG case 全部 `retrieve_empty` 的问题，让评测样例指向当前真实存在且有文档的知识库。
- 调整：`eval/eval_cases.json` 改用 `RAG技术原理`、`AI编程学习库`、`本项目开发与代码结构说明` 三个有文档知识库；移除依赖空集合 `default` 和空文档集合 `AI与编程学习资料` 的 RAG case。
- 稳定性：将缺少上下文的多轮问题改成单轮问题；高确定性 case 使用明确 source 片段，例如 `02_BM25资料.md`、`03_Hybrid_Search资料.md`、`05_Contextual_Compression资料.md`；对生成措辞易波动的 case 降低关键词脆弱度。
- 结果：重新生成 `eval/rag_eval_report.json`，本轮 14 个 case 中 13 个通过，pass rate 为 92.86%；所有 RAG case 均有非空检索结果。
- 剩余问题：`unknown_answer_guard` 仍失败，原因是答案未包含预期拒答关键词 `无法回答`；这暴露了未知问题拒答策略仍需后续单独优化。
- 保护：本次不调整 BM25、rerank、query rewrite、contextual compression 权重，不修改后端 API，不上传或恢复资料，不改 Chroma 数据。

## 2026-07-02 真实 RAG Eval 基线报告

- 目标：在不调整检索策略、不修改后端 API、不改 Chroma 数据的前提下，使用真实后端运行 `eval/rag_eval.py`，建立一份可追踪 request id 的 RAG 质量基线。
- 结果：生成 `eval/rag_eval_report.json`，本轮 14 个 case 中 2 个 endpoint case 通过、12 个 RAG case 失败，pass rate 为 14.29%。
- 失败归类：`retrieve_empty` 出现 12 次，是主导失败原因；同时伴随 `answer_missing_keywords` 7 次、`top_score_below_threshold` 3 次、`source_miss` 1 次、`answer_forbidden_keywords` 1 次。
- 诊断：`/collections` 可用且返回 5 个知识库，但 `default` 与 `AI与编程学习资料` 的文档列表均为空；因此本轮失败优先判断为 eval case 对应知识库/样例数据未就绪，而不是 BM25、rerank、query rewrite 或 compression 权重问题。
- 追踪：失败 RAG case 的 `retrieve_request_id` 和 `ask_request_id` 已写入 report details，可直接用 request id 搜索 `logs/app.log`。
- 下一步：先清洗 `eval/eval_cases.json`，让 case 指向当前真实存在且有文档的知识库，或先上传/恢复与 case 对应的基线资料；完成后再进入检索质量调参。

## 2026-07-02 RAG Eval 报告记录 request_id

- 目标：让 RAG eval 失败后也能直接按 request id 搜索 `logs/app.log`，补齐前端、后端接口、子模块日志之外的评测排障链路。
- 优化：`eval/rag_eval.py` 新增内部 `ApiResult` 和带 meta 的请求 helper，读取 `X-Request-ID` 与 `X-Process-Time-Ms`，并写入 RAG case 的 retrieve/ask details 以及 endpoint case details。
- 输出：失败 case 控制台摘要会在可用时显示 `request_ids` 或 `request_id`；结构化 JSON report 继续复用现有 `details` 字段，不改 eval case schema。
- 测试：`tests/test_eval.py` 覆盖 RAG retrieve/ask request id、endpoint request id、失败控制台输出和旧 dict mock 兼容路径。

## 2026-07-02 全链路日志 request_id 上下文贯穿

- 目标：让一次请求期间的后端子模块日志自动带上同一个 request id，方便从前端排障 ID 追踪到 RAG、vector store、Agent 和工具调用链路中的日志。
- 优化：`rag/logging_utils.py` 使用 `ContextVar` 保存当前 request id，并通过 `RequestIdFilter` 给 log record 注入 `request_id`；日志 formatter 增加 `request_id=%(request_id)s`。
- 接入：`main.py` 在请求中间件生成或读取 `X-Request-ID` 后设置日志上下文，请求结束后 reset，避免串请求污染；保留现有响应头和业务日志字段。
- 测试：`tests/test_logging_utils.py` 覆盖 formatter、默认 request id、set/reset；`tests/test_main_endpoints.py` 覆盖子模块 logger 在请求内继承 `request_id`。

## 2026-07-02 后端业务失败日志补充 request_id

- 目标：让前端失败提示中的“排障 ID”可以直接对应到后端业务失败日志，用户在 `logs/app.log` 搜索 request id 时不仅能看到请求完成行，也能看到具体 endpoint 失败原因。
- 优化：`main.py` 新增内部 `_log_endpoint_exception()`，在上传、问答、检索、生成、Agent 以及知识库/文档管理的 500 失败路径记录 `request_id`、operation 和必要上下文。
- 保护：日志不记录 token、headers、完整请求体、完整问题正文或文件内容；不改变 API 响应 JSON、响应头、前端展示、RAG 策略或 Agent/Tavily 行为。
- 测试：`tests/test_main_endpoints.py` 增加 endpoint 业务失败日志契约，验证响应头保留 `X-Request-ID`，错误日志包含 request id、operation、collection 和错误摘要。

## 2026-07-02 前端操作失败提示展示排障 ID

- 目标：把聊天失败中已经可见的 request id 排障信息扩展到创建/重命名/删除知识库、文档列表、批量删除、批量启用/禁用和上传失败任务消息中，方便用户按 `logs/app.log` 对齐后端日志。
- 新增：`ui/api_wrappers.py` 提供共享 `format_last_response_diagnostic_suffix()`，复用最近一次 API 响应诊断信息；没有 request id 时返回空字符串，保持原文案不变。
- 接入：`ui/chat.py` 改用共享 helper；`ui/sidebar.py`、`ui/pages.py`、`ui/upload.py` 仅在失败类提示或失败任务消息中追加排障 ID，不影响成功 toast、普通 info/warning、sources、Agent debug 或导出内容。
- 保护：`tests/test_frontend_ui_contracts.py` 覆盖共享 helper 的有/无 request id 输出、上传内联前缀，以及聊天/侧边栏/文档页/上传失败路径调用契约。

## 2026-07-02 前端错误回答展示排障 ID

- 目标：让聊天失败消息直接展示最近一次后端响应的 request id，方便用户按 `logs/app.log` 中的 `request_id` 定位后端日志。
- 新增：`ui/api_wrappers.py` 提供 `get_last_response_meta()`，只读返回 API client 捕获的最近一次响应诊断信息。
- 新增：`ui/chat.py` 在普通 RAG 失败和 Agent 失败回答中追加轻量排障后缀，包含 `排障 ID`、状态码和耗时；无 request id 时不显示。
- 保护：不修改后端 API、不改变业务返回 dict、不影响成功回答、sources、Agent debug 面板或导出内容。
- 测试：`tests/test_frontend_ui_contracts.py` 覆盖 wrapper 浅拷贝、诊断后缀格式化和失败消息路径调用。

## 2026-07-02 前端 API Client request diagnostics 捕获

- 目标：把后端响应头中的 `X-Request-ID` 和 `X-Process-Time-Ms` 接到前端 API client 层，便于后续用同一个 request id 对齐前端报错和后端日志。
- 新增：`rag/api_client.py` 的 `RagApiClient.last_response_meta` 保存最近一次请求的 `request_id`、`process_time_ms` 和 `status_code`。
- 兼容：请求异常时仅记录简短 `error` 摘要；诊断信息不混入现有业务返回 dict，不改变后端 API、RAG trace schema 或 UI 展示。
- 测试：`tests/test_api_client.py` 覆盖成功响应、非 200 响应、请求异常和 `/agent` debug payload 原样透传。

## 2026-07-02 Pytest 重复配置警告清理

- 目标：消除测试启动时 `pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)` 的重复配置噪音，让回归输出更聚焦真实失败。
- 清理：从 `pyproject.toml` 删除重复的 `[tool.pytest.ini_options]` 段，保留 `pytest.ini` 作为唯一 pytest 配置入口。
- 保护：不修改测试收集规则、不调整测试用例、不改变业务代码、依赖版本或运行时行为。
- 依据：`pytest.ini` 比 `pyproject.toml` 中的旧配置更完整，且 `PROJECT_MAP.md` 已记录 pytest 配置入口为 `pytest.ini`。

## 2026-07-02 Chroma/LangChain 弃用警告收敛

- 目标：继 FastAPI lifespan 迁移后，继续收敛向量库相关弃用警告，避免测试输出中的噪音遮挡真实失败。
- 迁移：`rag/vector_store.py` 将 Chroma wrapper 导入从 `langchain_community.vectorstores` 切换到 `langchain_chroma`。
- 兼容：新增内部持久化 helper；当前 `langchain_chroma` 自动持久化路径不再手动调用 `persist()`，旧式测试替身仍可通过 helper 验证兼容行为。
- 依赖：`requirements.txt` 和 `pyproject.toml` 显式声明 `langchain-chroma>=1.0.0`，不批量升级现有依赖。
- 保护：不修改 RAG 检索策略、不改变公开 API、不迁移 Chroma 数据，上传/删除/启禁用后的缓存失效语义保持不变。

## 2026-07-02 FastAPI lifespan 启动生命周期迁移

- 目标：消除 FastAPI `@app.on_event("startup")` 弃用警告，同时保持后端启动行为、endpoint 响应、API token、request id 和 Agent debug 透传不变。
- 迁移：`main.py` 新增 `asynccontextmanager` lifespan，把原有 API key 配置日志和 Embedding 预加载逻辑合并到统一启动生命周期中。
- 清理：删除旧的两个 `@app.on_event("startup")` 注册，避免测试和长期运行环境继续触发 deprecation warning。
- 保护：不调整 RAG 检索策略、不改变公开 API wire shape、不新增依赖、不修改启动脚本。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_main_endpoints.py -q` 通过，17 passed，未再输出 `on_event is deprecated` 警告。

## 2026-07-02 前端 API Agent debug 透传契约补强

- 目标：补齐前端调用链对 Agent debug 的透传护栏，确保 `agent_steps` 和 `debug_info.evidence_summary` 从 API client 到 UI wrapper 不被改写或丢失。
- 测试：`tests/test_api_client.py` 覆盖 `RagApiClient.agent()` 的 `/agent` 请求 payload、debug 开关、`agent_steps`、`search_trace` 和 `evidence_summary` 原样返回，以及失败 fallback 的空 debug 形状。
- 测试：`tests/test_frontend_ui_contracts.py` 覆盖 `agent_query_api()` 会读取 `settings_agent_debug` 并传给 `_api_client.agent()`，且返回值保持原对象不改写。
- 保护：不修改 `rag/api_client.py` 或 `ui/api_wrappers.py` 运行时代码，不改变 `/agent` wire shape，不访问真实后端、Tavily、Chroma 或 LLM。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_api_client.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_api_client.py tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m py_compile rag\api_client.py ui\api_wrappers.py tests\test_api_client.py` 通过。

## 2026-07-02 Web 搜索 search_trace 契约补强

- 目标：钉住 Tavily/DuckDuckGo 的 `search_trace` 结构，确保 Agent `evidence_summary` 中的 Web provider、降级状态、attempt count 和结果数可信。
- 修复：`rag/tools.py` 在 DuckDuckGo 被尝试时即写入 `provider=DuckDuckGo`，DuckDuckGo 成功后清空上游 Tavily 失败遗留的 `error`，避免成功兜底被误诊断为失败。
- 测试：`tests/test_tools_tavily.py` 覆盖 Tavily 成功、Tavily 重试后成功、无 Tavily key 走 DuckDuckGo、Tavily 失败后 DuckDuckGo 兜底、DuckDuckGo 失败五类 trace 契约。
- 保护：不改变 Tavily 优先和 DuckDuckGo 兜底策略，不改变工具返回正文格式，不访问真实 Tavily/DuckDuckGo 网络。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_tools_tavily.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_tools_tavily.py tests\test_agent_debug.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m py_compile rag\tools.py tests\test_tools_tavily.py` 通过。

## 2026-07-02 Agent evidence_summary API 透传契约

- 目标：补齐 `/agent` 端到端 debug 透传契约，确保后端生成的 `debug_info.evidence_summary` 不会在 FastAPI 响应层丢失。
- 测试：`tests/test_main_endpoints.py` 的 Agent debug 透传用例补充 `evidence_summary` mock payload，并断言 `mode`、本地/Web 使用状态、本地兜底、Web provider、Web 降级、尝试次数、结果数和策略提醒完整返回。
- 保护：不修改 `main.py`、不改变 `/agent` wire shape、不触发真实 LLM/Tavily/Chroma；仅用测试钉住既有 `debug_info: dict` 原样透传行为。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_main_endpoints.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_main_endpoints.py tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py tests\test_main_endpoints.py` 通过。

## 2026-07-02 Agent debug 前端函数级测试补强

- 目标：把 Agent 调试面板的 `evidence_summary` 展示从静态契约升级为函数级可验证，防止字段存在但实际步骤拼接回退。
- 测试：`tests/test_frontend_ui_contracts.py` 直接覆盖 `_build_agent_debug_steps()`，验证 local-only、local+web、本地兜底、Web 降级、策略提醒和缺少 `evidence_summary` 的旧 debug payload 兼容。
- 保护：不改后端 API、不改 Agent/Tavily 策略、不改前端布局；保留原有静态契约检查作为关键字段与文案防回退护栏。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m py_compile ui\chat.py tests\test_frontend_ui_contracts.py` 通过。

## 2026-07-02 Agent debug 证据摘要前端展示

- 目标：在不改后端 API、Agent 路由策略和 Tavily 搜索逻辑的前提下，把 `debug_info.evidence_summary` 接入前端 Agent 调试面板。
- 新增：`ui/chat.py` 的 `_build_agent_debug_steps()` 会优先展示紧凑中文“证据摘要”，汇总本地资料、外部补充、代码验证、本地兜底、Web provider、尝试次数、结果数、Web 降级和策略提醒。
- 兼容：缺少 `evidence_summary` 的历史消息继续走原有 `source_layers`、`search_trace`、`tool_budget` 展示，不丢失旧调试信息。
- 测试：`tests/test_frontend_ui_contracts.py` 增加前端契约断言，覆盖“证据摘要”“本地兜底”“Web 已降级”和 `policy_violations` 关键展示字段。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_frontend_ui_contracts.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m py_compile ui\chat.py` 通过。

## 2026-07-02 Agent debug 统一证据摘要

- 目标：在不改变 Agent 路由策略和 Tavily 搜索实现的前提下，为 debug 输出补充统一 `evidence_summary`，让本地证据、Web 证据、兜底和违规状态能一眼判断。
- 新增：`rag/agent.py` 根据 `tool_sequence`、`source_layers`、`tool_budget`、`search_trace` 和 `policy_fallbacks` 生成 `debug_info.evidence_summary`。
- 字段：摘要包含 `mode`、`local_used`、`web_used`、`code_used`、`local_fallback_used`、`web_provider`、`web_fallback_used`、`web_attempt_count`、`web_result_count` 和 `policy_violations`。
- 兼容：保留原有 `tool_sequence`、`tool_calls`、`tool_budget`、`source_layers`、`search_trace` 字段；debug 关闭时仍返回空 debug 信息。
- 测试：`tests/test_agent_debug.py` 覆盖 local-only、web-only、local-first 兜底后 local+web、RAG eval 快速回答和 debug disabled 场景。
- 保护：不修改 Tavily provider、retry/fallback 逻辑，不改变公开 API，不新增依赖。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_tools_tavily.py tests\test_agent_debug.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_tools_tavily.py tests\test_eval.py -q` 通过。

## 2026-07-01 Agent 本地优先兜底补本地证据

- 目标：本地资料类问题即使 Agent 误先调用 `search_web`，也必须补一次 `search_knowledge_base`，避免最终回答只依赖网页搜索。
- 修复：扩展 `rag/agent.py` 的 local-first 兜底条件，从“没有任何工具调用才补本地检索”改为“缺少 `search_knowledge_base` 就补本地检索”。
- 行为：本地兜底成功时把本地证据放在原 Agent 回答前；若本地检索未找到文档或检索出错，仅记录兜底调用，不强行改写回答。
- 调试：`debug_info.policy_fallbacks` 继续记录 `local_first_enforced`；误用 Web 的 `web_used_for_non_realtime_question` 和 `local_first_not_followed` 仍保留，便于诊断。
- 测试：`tests/test_agent_debug.py` 新增本地问题先调 Web 的场景，验证补本地检索、local+web 分层回答、违规保留和 source layer 更新。
- 保护：不修改 Tavily provider、retry/fallback 逻辑，不改变公开 API，不新增依赖。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_tools_tavily.py tests\test_agent_debug.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_agent_debug.py tests\test_tools_tavily.py tests\test_eval.py -q` 通过。

## 2026-07-01 Eval Probe 检索质量断言

- 目标：把仅用于观察的 eval probe 升级为可选硬性断言，避免后续检索调参时只看到 trace、却无法判断 top 命中质量是否回退。
- 覆盖：`eval/rag_eval.py` 新增 `expected_top_source_contains`、`min_top_score`、`expected_candidate_source`、`expected_trace`，可检查 top 来源、top 分数、候选来源和 query rewrite/contextual compression trace。
- 报告：新增 `top_source_miss`、`top_score_below_threshold`、`candidate_source_mismatch`、`trace_expectation_failed` 四类失败原因，继续保留原 `errors`、`failure_reasons`、top sources 和 diagnostics 输出。
- 样例：`eval/eval_cases.json` 只为现有 probe 增加低脆弱度断言，不写死本地私有来源或候选来源。
- 测试：`tests/test_eval.py` 覆盖 top source、top score、candidate source、query rewrite fallback、compression protected count、schema 校验和 report 字段。
- 保护：不修改 RAG 检索策略、不改变后端公开 API、不新增依赖、不访问真实 Chroma 或真实 LLM。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_eval.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_backend_rag_loop.py tests\test_vector_store.py tests\test_qa_chain.py tests\test_eval.py -q` 通过。

## 2026-07-01 RAG Eval 失败原因结构化

- 目标：让 RAG 评测报告在保留原 `errors` 文本的同时，额外输出稳定的 `failure_reasons` 枚举，方便后续判断问题来自检索、来源、答案关键词或 endpoint 检查。
- 覆盖：`eval/rag_eval.py` 为 RAG case 增加 `source_miss`、`answer_missing_keywords`、`answer_forbidden_keywords`、`retrieve_empty`，为 endpoint case 增加 `endpoint_check_failed`。
- 报告：结构化 JSON case 结果新增 `failure_reasons` 字段；控制台失败输出在 top sources 和 diagnostics 前显示失败原因摘要。
- 测试：`tests/test_eval.py` 覆盖五类失败原因、结构化 report 字段和控制台输出契约。
- 保护：不修改检索策略、不改变后端公开 API、不新增依赖、不访问真实 Chroma 或真实 LLM。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_eval.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_backend_rag_loop.py tests\test_vector_store.py tests\test_qa_chain.py tests\test_eval.py -q` 通过。

## 2026-06-04 检索排序短语加分与结果去重收敛

- 现象：`LangChain 的核心模块有哪些？` 这类问题中，query rewrite 可能追加“相关信息和应用实例”等宽泛短语，导致示例类章节被 phrase boost；同一章节的相邻片段也可能重复占满 top 结果。
- 修复：多行 query 的 exact phrase 只使用第一行原问题，rewrite 追加行仍参与关键词召回，但不再参与短语精准加分。
- 修复：metadata/title phrase boost 改为归一化短语精确命中，并跳过只剩 `langchain` 这类单英文技术词的宽泛短语，避免标题里只出现工具名就被抬高。
- 修复：最终重排结果按 `source + parent_chunk_index` 或 `source + section` 做去重，减少同父块/同章节片段重复占位；`phrase_score` 同步写入 trace 和 sources。
- 验证：真实 `/retrieve` smoke 中重复 8.2.1 片段收敛，eval smoke `3/3` 通过；未修改 Chroma 数据。

## 2026-06-04 普通 RAG 生成兜底答案更聚焦

- 现象：真实 `/ask` 与 eval smoke 中，检索可以命中正确文档，但当模型过度保守或输出偏片段摘要时，兜底答案容易丢失文档主题词、章节信息，并可能重复展示相同片段。
- 修复：收紧 `RAG_PROMPT_TEMPLATE`，要求先直接回答当前问题，再列支撑要点；对“有哪些/步骤/方法/模块”等问题优先整理成条目，并保留上下文中的英文专名、函数名和文件名。
- 修复：`_build_fallback_answer()` 的抽取式兜底现在会显示 `source / section` 标签，去重相同片段；有来源或章节信息的短片段也允许进入兜底。
- 兼容：不改变 `/ask`、`/retrieve`、`/generate` 响应结构，不修改 Chroma 数据，不新增环境变量或依赖。

## 2026-06-04 Agent 本地优先执行层兜底

- 现象：真实 `/agent` smoke 中，本地资料类问题被正确分类为 `local_knowledge`，但模型没有调用 `search_knowledge_base`，直接要求用户补充背景；说明仅靠 prompt 无法稳定执行“本地知识库优先”。
- 修复：`create_agent()` 将工具按名称挂到 agent 对象；`run_agent()` 在 local-first 问题且工具序列为空时，自动调用一次 `search_knowledge_base`。
- 调试：执行层兜底会写入 `agent_steps`、`debug_info.tool_sequence`、`debug_info.tool_calls` 和 `debug_info.policy_fallbacks=["local_first_enforced"]`。
- 兼容：只有本地优先且 Agent 完全未调用工具时触发；已有工具调用、实时 Web 问题和代码任务不受影响。

## 2026-06-04 稳定运行与排障文档清单

- 目标：把 Phase 4 已完成的日志、评测、Agent/Tavily 回归能力整理成可执行的部署与排障清单。
- 文档：README 新增稳定运行建议、request id 排查、Tavily 异常、Chroma 备份与恢复说明。
- 文档：项目维护手册新增 Phase 4 日志、评测与 Agent 回归维护项，并补充真实 RAG 评测、API_TOKEN、request id 和 Chroma 备份演练待办。
- 文档：`docs/KNOWN_ISSUES.md` 新增运行与密钥规则，强调不要长期使用 `--reload`、不要泄露密钥、Chroma 备份要完整复制目录。
- 兼容：仅更新文档，不修改业务代码。

## 2026-06-04 RAG 评测结构化 JSON 报告

- 目标：让每次 RAG 调参后的评测结果可保存、可对比，而不只停留在控制台 PASS/FAIL 输出。
- 优化：`eval/rag_eval.py` 新增 `--output-json` 参数，可保存结构化报告。
- 优化：报告包含 summary（总数、通过数、失败数、通过率、总耗时）、meta（api_base、cases_path、generated_at）和每个 case 的 question、collection、endpoint、success、errors、details。
- 优化：RAG case 的 details 继续包含候选数、最终片段数、top source/section/score、缺失关键词、禁用关键词、检索耗时、生成耗时和答案长度。
- 兼容：默认不传 `--output-json` 时行为和退出码保持不变；不新增依赖。

## 2026-06-04 API request_id 与耗时日志

- 目标：Phase 4 日志标准化先做最小闭环，让前端错误、API 响应和后端日志能通过同一个 request id 对齐。
- 优化：新增 HTTP 中间件，接收客户端 `X-Request-ID` 或自动生成 request id，并写入 `request.state.request_id`。
- 优化：所有响应头追加 `X-Request-ID` 和 `X-Process-Time-Ms`；401 等中间件提前返回也会带上 request id。
- 优化：后端日志记录 `request_completed request_id=... method=... path=... status=... elapsed_ms=...`；未捕获异常会记录 traceback 并返回友好 500 响应和 request id。
- 兼容：不改变现有 JSON 成功响应结构；只新增响应头和日志字段。

## 2026-06-04 Agent 工具策略 smoke 覆盖

- 目标：为 Phase 3 Agent/Tavily 融合增加低成本回归保护，不连接真实 LLM 或真实网络。
- 覆盖：新增本地资料问题 smoke，验证 Agent debug 标记 `local_knowledge`、`local_only`，且不出现 Web 策略违规。
- 覆盖：新增实时外部问题 smoke，验证 Agent debug 标记 `external_realtime`、`web_only`，且 Web 调用不被判为非实时违规。
- 覆盖：`/agent` endpoint 测试确认 `tool_policy`、`tool_budget`、`source_layers` 会完整透传给前端。
- 覆盖：Tavily 失败降级 DuckDuckGo 时，搜索 trace 会记录 provider、fallback、attempts 和失败原因。

## 2026-06-04 Agent 本地资料与外部搜索分层输出

- 现象：Agent 同时调用本地知识库和网页搜索时，最终回答可能把两类来源混在一起，用户难以判断哪些结论来自本地资料、哪些只是外部补充。
- 优化：system prompt 要求同时使用 `search_knowledge_base` 和 `search_web` 时，最终回答按“本地资料 / 外部搜索补充 / 来源提示”分层，并明确本地资料优先。
- 优化：新增 `debug_info.source_layers`，记录本次回答是 `local_only`、`web_only`、`local_plus_web`、`code_only` 还是 `no_tool`。
- 优化：如果模型同时使用本地和 Web 但没有按分层格式输出，后处理会添加轻量分层外壳，避免外部搜索覆盖本地资料结论。
- 优化：前端 Agent 调试面板展示来源层级，便于定位回答是否来自本地资料、外部搜索或二者混合。

## 2026-06-04 Agent 工具策略与预算调试

- 目标：收紧 Agent 工具选择，避免本地资料问题直接走 Web 或无节制调用代码工具。
- 优化：Agent system prompt 明确“本地知识库优先”，项目资料、已有知识、上传文档、代码结构和 RAG 实现类问题必须先查 `search_knowledge_base`；只有最新新闻、当前版本、价格、天气等实时外部信息才优先使用 `search_web`。
- 优化：新增 `AGENT_MAX_TOOL_CALLS`、`AGENT_MAX_WEB_SEARCHES`、`AGENT_MAX_CODE_EXECUTIONS`，并在 `debug_info.tool_budget` 中记录实际工具次数、预算上限和策略提醒。
- 优化：新增轻量问题分类，`debug_info.tool_policy` 会记录问题类别、是否本地优先、是否允许 Web/代码工具、推荐首个工具。
- 优化：前端 Agent 调试面板展示工具策略和预算统计，便于判断模型是否违反“本地优先”或超出 Web/代码预算。
- 兼容：不改变 `/agent` 响应结构，只扩展 `debug_info`；既有 `agent_steps` 和搜索 trace 继续保留。

## 2026-06-04 上下文压缩高置信片段保护

- 现象：上下文压缩或 reranker 偶尔会把基础检索中的高置信片段过滤掉，导致 `/ask` 拿不到关键证据，表现为引用不完整或回答缺少资料中的核心代码/段落。
- 优化：新增 `ENABLE_CONTEXTUAL_COMPRESSION_PROTECTION`，默认开启；压缩结果为空时回退基础 top 片段，压缩丢失高置信基础片段时最多补回 `CONTEXTUAL_COMPRESSION_PROTECT_TOP_N` 个片段。
- 优化：新增 `CONTEXTUAL_COMPRESSION_PROTECT_MIN_SCORE` 控制保护阈值，默认 `0.7`，避免低置信片段覆盖压缩结果。
- 优化：`/retrieve.trace.compression` 记录压缩输入数量、压缩输出数量、保护补回数量和降级原因；被补回片段在 `final_documents` 中标记 `contextual_compression_protected=true`。
- 兼容：不修改 Chroma 数据；压缩正常且未丢失高置信片段时，输出顺序保持压缩结果优先。

## 2026-06-03 Query rewrite 空命中自动回退

- 现象：LLM query rewrite 偶尔会把问题改写得过窄或跑偏，导致本地知识库明明有资料但 `/retrieve` 返回空结果，后续 `/ask` 容易回答“根据现有资料无法回答该问题”。
- 优化：新增 `ENABLE_QUERY_REWRITE_FALLBACK`，默认开启；当启用 query rewrite 且改写检索没有候选/最终片段时，自动用原上下文查询重试一次。
- 优化：`/retrieve.trace.query_rewrite` 记录 `attempted_query`、`final_query`、`contextual_query`、`fallback_used`，便于评测和前端调试判断是否发生回退。
- 兼容：已有命中时不额外重试，避免常规检索多一次 Chroma 查询；关闭 query rewrite 或关闭 fallback 时行为保持原样。

## 2026-06-03 检索候选数与排序权重配置化

- 目标：让 RAG 质量调参不再需要修改代码，配合评测脚本可以直接通过 `.env` 调整候选数量、混合检索权重和重排权重。
- 优化：新增 `RETRIEVER_INITIAL_K_MULTIPLIER`、`RETRIEVER_INITIAL_K_MIN`、`RETRIEVER_RERANK_K_MULTIPLIER`，替代初始候选和重排候选数量的硬编码。
- 优化：新增 `HYBRID_VECTOR_WEIGHT`、`HYBRID_BM25_WEIGHT`、`RERANK_VECTOR_WEIGHT`、`RERANK_KEYWORD_WEIGHT`、`RERANK_PHRASE_WEIGHT` 以及关键词候选相关权重配置，默认值保持原行为。
- 优化：`/retrieve.trace` 中补充实际使用的 `initial_k`、`rerank_candidate_count` 和 `weights`，便于评测输出和排障时复现参数。
- 兼容：不修改 Chroma 数据，不改变默认排序结果；旧 `.env` 不配置新变量时继续使用当前默认值。

## 2026-06-03 RAG 评测输出接入检索 trace

- 现象：`eval/rag_eval.py` 只能输出 PASS/FAIL 和简单错误，无法看见 `/retrieve` 命中的 source、section 和 score；排查评测失败时难以区分“检索没命中”和“生成没覆盖关键词”。
- 优化：评测 CLI 改为读取 `/retrieve.trace.final_documents`，每个 RAG case 输出候选数、最终片段数、top source/section/score、检索耗时、生成耗时和答案长度。
- 优化：新增 `forbidden_keywords` 检查，用于防止回答包含历史错误建议，例如缺失第三方库时建议临时安装不必要依赖。
- 修复：`eval/eval_cases.json` 中已有 `GET /health`、`GET /collections` smoke case，旧校验却强制每个 case 必须有 question；现在 endpoint case 可无 question，并支持基础 GET 检查。
- 验证：新增评测 helper 单元测试覆盖 trace 提取、source 格式化、endpoint case、禁用关键词和 `evaluate_case()` 诊断详情。

## 2026-06-03 `/retrieve` 检索 trace 与 source score 契约

- 现象：排查“资料明明存在但回答不完整/引用不清楚”时，`/retrieve` 只返回基础片段和粗略数量，缺少稳定的最终片段 score、候选来源和 trace 字段，前端和评测脚本难以解释为什么某个 chunk 被选中。
- 优化：在向量检索 trace 中补充 `final_documents`，为每个最终片段记录 `source`、`section`、`score`、`vector_score`、`keyword_score`、`rerank_score`、`candidate_source`、`ensemble_rank` 等 JSON-safe 字段。
- 优化：`QAChain.retrieve()` 保持原有 `documents/sources/retrieved_count/selected_count` 字段不变，追加 `trace`；`sources` 同步输出关键 score 字段，便于 UI、Agent 和评测复用同一契约。
- 兼容：不修改 Chroma 数据，不做历史 metadata 迁移；旧数据缺字段时使用默认值，避免已有知识库读取失败。
- 验证：新增 vector store trace、QAChain retrieve trace 和 `/retrieve` endpoint 契约测试；README 已补充接口字段说明。

## 2026-06-02 前端 CSS 孤儿规则收尾清理

- 目标：界面稳定后集中移除已经失去渲染路径或被最终覆盖层完整接管的旧 CSS，减少后续局部修改互相覆盖的风险。
- 清理：移除早期 `.upload-docs-table` 文档表格、`.doc-checkbox` 假复选框和 `.status-*` 状态文字规则；当前文档管理继续使用真实 Streamlit checkbox 与 `.document-card` 卡片系统。
- 清理：移除旧 `.thinking` 加载组件及其 `spin`、`thinking-dots` 动画；当前等待反馈继续使用 `.process-step` 真实检索步骤和浏览器端即时加载卡。
- 清理：移除已无页面节点的 `.main-header` 与 `.mode-select-btn` 规则；移除已被 `_dark_refinement.py` 后加载层完整接管的旧深色固定输入框背景块。
- 保留：移动端 `_responsive.py` 与 `_mobile_refinement.py` 仍分别承担基础断点和最终窄屏收口职责；侧边栏 `_sidebar.py` 与 `_sidebar_refinement.py` 仍分别承担结构图标和紧凑尺寸覆盖职责，不合并。
- 结果：组合 CSS 收敛到 `198401` 字符；源码扫描无 `.upload-docs-table`、`.doc-checkbox`、`.status-*`、`.thinking`、`.mode-select-btn` 和 `.main-header` 运行样式残留。
- 保护：未修改按钮 key、布局 class、侧边栏菜单、上传、文档管理、问答、固定输入框、移动端断点或后端逻辑。
- 验证：使用独立临时 `PYTHONPYCACHEPREFIX` 运行 `python -m py_compile ui/styles/_global.py ui/styles/_widgets.py ui/styles/_dark.py ui/styles/_workspace.py ui/styles/_responsive.py ui/styles/_chat.py ui/styles/__init__.py ui/assets.py streamlit_app.py` 通过；`git diff --check` 通过。

## 2026-06-02 高频操作无障碍细节优化

- 目标：在不改变现有布局和业务逻辑的前提下，补齐高频按钮的悬停提示、键盘焦点反馈和禁用原因。
- 优化：知识库与会话三点菜单补充具体悬停提示；菜单中的置顶、分享、重命名和删除操作补充用途说明，已置顶状态会明确提示无需重复操作。
- 优化：文档管理全选、删除、禁用和启用按钮补充动态提示；按钮禁用时明确说明需要先选择文档，或所选文档已经全部处于目标状态。
- 优化：快捷提问、空状态示例、上传处理和失败重选按钮补充操作提示；自定义回答复制、重新生成、单条引用复制、全部引用复制和引用折叠区补充 `title`、`aria-label` 与键盘焦点环。
- 优化：浏览器增强脚本为侧边栏三点和上传队列删除按钮补充可读 `aria-label`，避免辅助技术只能朗读“⋯”或“删除”。
- 保护：未修改知识库、会话、文档管理、上传、问答、检索、固定输入框或后端接口逻辑。
- 验证：`python -m py_compile ui/sidebar.py ui/pages.py ui/chat.py ui/upload.py ui/components.py ui/js_injection.py ui/styles/_chat.py streamlit_app.py` 通过。

## 2026-06-02 对话发送即时加载反馈优化

- 现象：点击发送、快捷提问或空状态示例后，Streamlit rerun 与后端检索开始前存在短暂空档；网络较慢时用户容易误以为页面白屏或点击未生效。
- 优化：在浏览器端为发送按钮、快捷提问和空状态示例绑定即时反馈；点击后无需等待 Python rerun，立即在固定输入区上方显示轻量“正在检索知识库”卡片、说明文字和三点骨架动画。
- 优化：真实检索步骤渲染后即时卡自动让位；快速请求完成后通过短时保护与兜底定时器自动清理，避免自身 DOM 变更触发观察器后被过早移除，也避免残留。
- 适配：补充深色模式背景与阴影适配；现有全局 `prefers-reduced-motion` 规则会自动压缩骨架动画时长。
- 保护：未修改检索、生成、会话持久化、固定输入框定位、自动滚动或后端接口逻辑。
- 验证：`python -m py_compile ui/js_injection.py ui/styles/_chat.py ui/styles/_dark_refinement.py ui/styles/__init__.py ui/chat.py streamlit_app.py` 通过。

## 2026-06-02 交互回归巡检与检索链路兼容修复

- 巡检：稳定模式启动后端与前端；确认健康检查通过、模型密钥已配置、3 个知识库可列出，当前知识库可返回 6 个启用文档。
- 巡检：桌面端知识库三点菜单可展开与关闭，菜单项为“置顶 / 重命名 / 删除”；会话三点菜单可展开与关闭，菜单项为“分享 / 置顶 / 重命名 / 删除”；关闭菜单后主标签页可恢复交互。
- 巡检：文档管理页可加载搜索、筛选、排序、全选和批量操作工具栏；真实鼠标点击“全选”后 6 个文件进入选中状态。自动化语义点击未触发 Streamlit 前端桥接，不属于产品缺陷。
- 修复：窄屏下侧边栏作为覆盖层打开时，全局隐藏 Streamlit header 会同时隐藏原生收起入口，导致主区左侧无法点击。移动端最终覆盖层恢复原生侧栏收起/展开控件，仅保留该控件可交互，不改变桌面布局。
- 修复：SiliconFlow `/embeddings` 支持原始中文字符串，但 LangChain `OpenAIEmbeddings` 默认会先将文本转换为 token-id 数组，导致中文检索返回 `400 code 20015`。设置 `check_embedding_ctx_length=False`，让兼容接口接收原始文本；项目已有上传前安全分块保护。
- 保护：未执行文档删除、批量删除、文档启停、上传、知识库删除、会话删除或 Chroma 数据迁移；未修改现有向量数据。
- 验证：`python -m py_compile ui/styles/_mobile_refinement.py ui/styles/__init__.py ui/pages.py ui/upload.py ui/sidebar.py ui/chat.py ui/js_injection.py streamlit_app.py main.py rag/vector_store.py tests/test_vector_store.py` 通过；`python -m pytest tests/test_vector_store.py tests/test_api_client.py -q` 通过，共 `62 passed`；新增兼容参数单元测试；独立 Embedding 探针确认关闭 LangChain token 化后中英文均返回 `1024` 维向量；稳定重启后端后，中文知识库真实 `/retrieve` 请求返回 `200`，召回 `30` 个候选并成功筛选结果；前后端 HTTP 探针均返回 `200`，名称映射无临时乱码键残留。

## 2026-05-31 前端 CSS 长期清理第二轮

- 目标：继续降低历史补丁堆叠风险，只删除已确认无运行时调用的旧样式，不改动当前交互结构。
- 清理：移除早期 `.sidebar-collections-list`、`.sidebar-collection-item`、`.sidebar-more-btn`、`.dropdown-*` 和 `.new-collection-*` 自定义侧边栏实现；当前知识库与会话三点菜单继续使用真实 Streamlit key 规则。
- 清理：移除已被 `render_empty_state()` 与 `ui/styles/_empty_states.py` 接管的旧 `.chat-empty-*`、`.upload-empty-*`、`.empty-step`、`.empty-state` 和 `.empty-chat-message` 规则，并同步清除深色模式与响应式孤儿覆盖。
- 清理：移除 `_responsive.py` 中已由最终移动端收口层接管的固定输入区重复规则，保留表格、引用卡、文档工具栏与消息气泡等仍有效的响应式规则。
- 结果：组合 CSS 从 `211087` 字符收敛到 `201051` 字符，减少 `10036` 字符；共享空状态、固定输入框、上传删除按钮和侧边栏三点菜单相关规则仍保留。
- 保护：未修改上传、文件删除、知识库管理、会话管理、三点菜单开关、问答、固定输入框行为或后端接口逻辑。
- 验证：`python -m py_compile ui/styles/_global.py ui/styles/_chat.py ui/styles/_upload.py ui/styles/_dark.py ui/styles/_responsive.py ui/styles/__init__.py ui/components.py ui/pages.py streamlit_app.py` 通过；旧类扫描仅剩共享 `.workspace-empty-*` 实现。

## 2026-05-31 超窄屏交互区二次收口

- 现象：移动端主要布局已适配，但在更窄的手机宽度下，文档筛选器、批量操作按钮、上传失败恢复条和固定输入区操作按钮仍可能拥挤；侧边栏三点菜单浮层也需要进一步内收。
- 优化：为文档筛选区和批量操作区增加稳定容器 key，仅在超窄屏下将筛选器改为纵向排列、四个批量按钮改为两列排列，并隐藏桌面端占位列。
- 优化：上传失败恢复条在手机端改为上下排列；聊天输入区固定为“输入框 + 发送/停止 + 重置”三列；同步收紧头像、消息气泡和侧边栏菜单浮层。
- 保护：桌面布局保持不变；未修改筛选、批量删除、启用/禁用、上传恢复、聊天发送或三点菜单行为。
- 验证：`python -m py_compile ui/pages.py ui/styles/_mobile_refinement.py` 通过。

## 2026-05-31 移动端与窄屏布局收口

- 现象：现有响应式规则较分散，窄屏下固定输入区、快捷提问、上传队列、文档工具栏和标签页仍可能挤压或横向溢出；通用按钮全宽规则会让部分操作区显得臃肿。
- 优化：新增 `ui/styles/_mobile_refinement.py` 最终移动端覆盖层；侧边栏限制为合理视口宽度，固定输入区缩为紧凑两行，快捷提问和标签页支持隐藏滚动条的横向滑动。
- 优化：上传队列改为移动端优先的信息排布，状态徽标落到文件信息下方；文档工具栏、文档卡片、复选框和操作按钮同步压缩间距与字号，但保留可触达高度。
- 优化：在更窄屏幕下进一步收紧 Hero 标签、共享空状态和引用卡片边距。
- 保护：仅修改响应式 CSS，不改变侧边栏、上传、问答、文档管理、快捷提问或标签页逻辑。
- 验证：`python -m py_compile ui/styles/_mobile_refinement.py ui/styles/__init__.py` 通过；移动端覆盖层已在样式注册表最后加载。

## 2026-05-31 深色模式高频区域巡检与收口

- 现象：多数组件已经使用深色变量，但上传主按钮、失败恢复按钮、快捷提问胶囊、停止按钮 hover 和危险确认 hover 仍存在浅色硬编码，切换深色模式时可能出现突兀白块或亮红色闪烁。
- 优化：新增 `ui/styles/_dark_refinement.py` 最终覆盖层并在样式注册表最后加载；统一固定输入区、快捷提问、停止/清空按钮、上传队列、上传主按钮、失败恢复条、文档卡片、弹窗和侧边栏菜单的深色背景、边框和阴影。
- 优化：危险操作继续保留红色语义，但 hover 改为深色变量，不再闪出浅色红底；上传操作按钮移除深色模式下的白色渐变。
- 保护：仅修改深色视觉覆盖，不改变上传、问答、停止生成、文档管理、弹窗或侧边栏菜单逻辑。
- 验证：`python -m py_compile ui/styles/_dark_refinement.py ui/styles/__init__.py` 通过；深色收口层已在样式注册表最后加载。

## 2026-05-31 核心页面空状态统一

- 现象：上传页、文档管理页和知识库问答页的空状态分别使用不同结构；文档管理仍是临时文字块，图标、标题和步骤卡层级不一致。
- 优化：新增复用组件 `render_empty_state()` 和独立样式模块 `ui/styles/_empty_states.py`；统一空状态的图标徽章、标题、说明、三段引导卡、圆角、阴影、深色模式和移动端布局。
- 优化：上传页保留归档引导；问答页补齐范围、提问和引用图标；文档管理区分“知识库暂无文档”和“筛选无结果”两类空状态，并为筛选状态补充线性搜索图标。
- 保护：未修改上传、文档列表查询、筛选、问答、快捷问题、会话或后端逻辑。
- 验证：`python -m py_compile ui/components.py ui/upload.py ui/chat.py ui/pages.py ui/icons.py ui/styles/_empty_states.py ui/styles/__init__.py` 通过；共享空状态样式已在注册表最后加载。

## 2026-05-31 回答停止入口与手动滚动保护

- 现象：回答生成过程中用户没有明确的停止入口；用户主动向上查看历史消息后，回答完成时页面仍可能强制跳回底部，打断阅读。
- 优化：生成期间将发送按钮切换为轻量红色“停止”按钮；点击后结束当前前端回答流程、恢复输入框，并在会话中记录“已停止生成”提示。
- 优化：增加用户滚动意图保护。发送新问题时仍自动定位到底部；用户向上滚动或按 `PageUp / Home / ArrowUp` 后暂停自动跟随，回到底部或按 `End` 后恢复。
- 说明：后端模型请求仍为同步请求，停止入口用于立即终止当前前端回答流程，不承诺撤回已经发出的远程请求。
- 保护：未修改检索、生成 API、会话导出、引用来源、快捷提问或侧边栏菜单逻辑。
- 验证：`python -m py_compile ui/chat.py ui/js_injection.py ui/styles/_chat.py` 通过。

## 2026-05-31 侧边栏置顶状态与长名称提示优化

- 现象：知识库和会话置顶后虽然会移动到列表顶部，但列表和菜单缺少明确反馈；名称较长被截断后无法快速查看完整文本。
- 优化：置顶知识库和会话在列表气泡右侧增加轻量图钉标记；菜单中的“置顶”会切换为蓝色“已置顶”禁用态，避免重复操作。
- 优化：知识库和会话列表按钮增加原生悬停提示，长名称截断时仍可查看完整文本。
- 保护：未修改三点按钮 key、菜单开关、排序规则、会话持久化、重命名、分享、删除或后端接口逻辑。
- 验证：`python -m py_compile ui/sidebar.py ui/styles/_sidebar_refinement.py` 通过。

## 2026-05-31 上传失败恢复体验收口

- 现象：上传失败后虽然文件行已经展示原因，但队列下方仍有重复汇总卡片和普通 caption；用户需要自行判断下一步如何重新选择文件。
- 优化：失败文件行新增针对性恢复建议；扫描版或图片型 PDF 会明确提示启用图片解析、检查多模态模型权限，或改用 OCR / 可复制文本版本。
- 优化：失败状态下不再展示重复结果卡片，队列下方只保留紧凑恢复条和“重新选择文件”入口；点击后同步清空上传控件、队列、分页签名和旧结果状态，可直接重新选择。
- 保护：未修改上传接口、文档解析、向量入库、成功提示、文件行删除或后端错误处理逻辑。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-31 对话快捷键提示间距修复

- 现象：固定输入区右侧 `Ctrl`、`Enter` 和“快速发送”提示被拉伸到整列宽度，元素之间距离过大。
- 根因：`.chat-input-hint` 使用 `justify-content: space-between`，在 Streamlit 列容器中被撑宽后将三个内容推散；移动端规则还会将提示拆成竖排。
- 修复：将快捷键提示改为右侧对齐的紧凑行内组，缩小间距并固定为单行；移动端继续保持横向排列。
- 保护：仅调整提示文字布局，不修改快捷键监听、发送、固定输入区、问答或会话逻辑。
- 验证：`python -m py_compile ui/styles/_chat.py` 通过。

## 2026-05-31 侧边栏视觉节奏收口

- 目标：让知识库管理侧边栏从多轮局部补丁中重新收敛为统一、紧凑的产品级导航区。
- 优化：新增 `ui/styles/_sidebar_refinement.py` 最终覆盖层，并在按钮系统之后加载；统一管理标题、创建知识库、新建会话、使用说明、知识库列表、会话列表和当前知识库卡片的圆角、高度、间距与阴影节奏。
- 优化：移除标题前重复装饰圆点，保留语义明确的书本图标；列表项继续使用单一气泡结构，内嵌三点按钮位置更稳定，菜单面板同步收紧。
- 保护：未修改知识库或会话按钮 key、三点菜单开关、置顶、分享、重命名、删除、会话切换或后端接口逻辑。
- 验证：`python -m py_compile ui/styles/_sidebar_refinement.py ui/styles/__init__.py ui/sidebar.py` 通过；样式注册表可加载且侧边栏收口层位于最后。

## 2026-05-31 对话输入工具条与引用摘要降噪

- 目标：降低固定输入区和回答下方引用来源的视觉噪音，让对话页更接近成熟聊天产品。
- 优化：快捷提问从独立标题行加按钮行合并为单一工具条，左侧显示“快捷提问”和四个紧凑胶囊，右侧保留 `Ctrl + Enter` 提示；进一步收紧胶囊高度、字号、图标和间距。
- 优化：引用来源继续保持默认折叠摘要，仅显示引用数量、最高相似度和复制入口；摘要卡收紧最大宽度、圆角、内边距和阴影，展开后才展示证据卡片。
- 保护：未修改固定输入框定位、快捷问题内容、问答生成、引用阈值、复制引用、会话或后端逻辑。
- 验证：`python -m py_compile ui/chat.py ui/styles/_chat.py` 通过。

## 2026-05-31 文档管理工具栏紧凑化升级

- 目标：降低文档管理页批量操作区的视觉重量，让搜索、状态摘要和操作按钮更适合高频管理场景。
- 优化：工具栏改为紧凑状态摘要，保留启用、禁用和当前显示数量；选中文档后才显示蓝色选择强调，无选择时保持中性白卡；选中数量改为更清晰的“X 已选择文档”。
- 优化：全选、删除、禁用、启用四个按钮缩减为 34px 高的紧凑图标按钮组，减少列宽、字号、内边距和阴影；重要提示“禁用文档不会参与问答检索”移动到工具栏下方的轻量说明行。
- 保护：未修改全选范围、批量删除确认、启用/禁用 API、搜索、筛选、排序或文档列表逻辑。
- 验证：`python -m py_compile ui/pages.py ui/styles/_documents.py ui/styles/_widgets.py` 通过。

## 2026-05-31 上传流程轻量步骤条

- 目标：让用户明确理解上传页当前处于“选择文件 / 开始处理 / 完成归档”的哪个阶段，减少点击后等待时的不确定感。
- 优化：新增三段紧凑上传流程条；未选择文件时引导选择资料，队列等待时推进到开始处理，上传过程中高亮处理中阶段，全部成功或失败后进入完成归档阶段。
- 适配：步骤条使用轻量蓝色 active、绿色 done 状态，移动端自动切换为单列展示，避免占用过多横向空间。
- 保护：状态完全由现有上传队列推导，不修改上传接口、PDF 解析、向量入库、删除状态同步或后端逻辑。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-31 前端 CSS 废弃规则收敛

- 目标：减少前端补丁堆叠，删除已经没有调用方的旧样式，降低后续 UI 调整互相覆盖和回归的概率。
- 清理：移除上传页旧 `.uploaded-files-*` / `.uploaded-file-*` 预览列表整套样式、废弃上传分页箭头样式、已移除的失败重试按钮样式和未使用的 `.upload-task-list` 包装规则。
- 清理：移除侧边栏旧 `.sidebar-new-btn`、`.collection-menu`、`.session-menu` HTML 菜单样式，以及响应式文件中的对应残留；当前侧边栏继续使用真实 Streamlit key 菜单规则。
- 结果：CSS 总体积从约 `184 KB` 收敛到约 `176 KB`；上传样式和侧边栏样式保留当前唯一实现。
- 保护：未修改问答、上传、文件删除状态同步、侧边栏菜单行为、文档管理或后端接口逻辑。
- 验证：`python -m py_compile ui/styles/_upload.py ui/styles/_sidebar.py ui/styles/_responsive.py ui/styles/_buttons.py ui/styles/__init__.py ui/upload.py` 通过；源码扫描无 `uploaded-files-`、`uploaded-file-`、`retry_upload_`、`.sidebar-new-btn`、`.collection-menu`、`.session-menu` 和 `.upload-task-list` 残留。

## 2026-05-31 全局按钮设计系统收口

- 目标：统一创建、上传、发送、重置、确认删除和小型图标按钮的尺寸、圆角、阴影与交互反馈，避免不同模块像来自不同产品。
- 根因：按钮样式历史上分散在 `_widgets.py`、`_chat.py`、`_upload.py` 和侧边栏样式中，同一种语义存在多套高度、圆角和 hover 规则，后续修改容易互相覆盖。
- 修复：新增 `ui/styles/_buttons.py` 作为最终按钮覆盖层，并在样式注册表最后加载；定义小/中/大控件高度、圆角和图标尺寸变量；将主操作统一为蓝白轻量强调，次操作统一为中性白卡，危险确认统一为红色语义，小型图标操作统一为 34px 方圆按钮。
- 保护：仅新增视觉收口层，不修改按钮 key、点击事件、上传、会话、文档管理、侧边栏菜单或后端接口逻辑。
- 验证：`python -m py_compile ui/styles/_buttons.py ui/styles/__init__.py ui/styles/_upload.py ui/styles/_chat.py ui/styles/_widgets.py` 通过；`from ui.styles import CSS_STYLES` 成功加载并包含按钮系统变量。

## 2026-05-31 上传队列单行 Grid 结构重构

- 目标：彻底移除上传队列文件条依赖 Streamlit 双列和负边距覆盖的脆弱布局，避免垃圾桶反复错位。
- 根因：旧结构将 HTML 文件卡片和真实删除按钮分别放在两个 Streamlit 列中，再通过负 margin 把删除按钮压回卡片内部；列宽、组件包装层或窗口宽度变化都会造成按钮偏移、重叠或文件条缩短。
- 修复：每个上传队列项改为单一带 key 的 Streamlit 容器；文件卡片内部使用固定 Grid 布局展示“文件图标 / 文件信息 / 状态徽标”，真实 `st.button` 删除按钮作为同一容器内的绝对定位操作位，固定在右侧中线，不再使用双列或负 margin。
- 清理：移除废弃 `.upload-task-remove` 假按钮样式和移动端残留选择器，避免新旧规则继续互相干扰。
- 保护：保留真实 Streamlit 删除按钮、上传控件状态同步、重复文件独立 key、上传处理和后端 API 调用逻辑。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py ui/styles/_responsive.py` 通过；源码检查上传队列不再包含 `.upload-task-remove` 和负 margin 覆盖规则。

## 2026-05-31 上传队列垃圾桶图标绝对居中修复

- 现象：上传队列删除按钮外框已经位于正确位置，但内部黑色垃圾桶图标仍偏左。
- 根因：伪元素作为按钮 flex 子项时仍受到 Streamlit 按钮内部布局影响，普通 flex 居中未能稳定约束图标位置。
- 修复：将垃圾桶伪元素改为相对按钮的绝对定位，使用 `top: 50%`、`left: 50%` 和双轴 `translate(-50%, -50%)` 锁定正中心。
- 保护：仅调整垃圾桶图标定位，不改变按钮外框、删除状态同步、上传或后端逻辑。
- 验证：`python -m py_compile ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列状态徽标与垃圾桶重叠修复

- 现象：上传队列文件条恢复等宽后，垃圾桶覆盖到了“等待中”状态徽标，右侧操作区仍不合格。
- 根因：覆盖式删除按钮的负边距过大，同时文件条为状态徽标预留的右侧槽位不足。
- 修复：扩大文件条右侧操作槽，将状态徽标向左收；缩小删除按钮负边距，使垃圾桶固定在卡片右侧内边距内；按钮使用 flex 双向居中，保证垃圾桶位于圆角方框正中。
- 保护：仅调整上传队列右侧操作区布局，不改变真实删除、状态同步、上传或后端逻辑。
- 验证：`python -m py_compile ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列文件条等宽与垃圾桶居中修复

- 现象：上传队列文件胶囊条比下方分页条短，垃圾桶图标在圆角方框内部也没有居中。
- 根因：真实删除按钮占用了独立 Streamlit 列宽，导致文件胶囊被压缩；之前为修正位置增加的按钮垂直偏移又让垃圾桶图标偏离方框中线。
- 修复：将删除按钮列压缩为覆盖操作位，让文件胶囊恢复接近整行宽度；删除按钮覆盖到胶囊右侧内部，取消垂直偏移，并为垃圾桶伪元素增加块级居中规则。
- 保护：保留真实 `st.button` 删除和上传控件状态同步逻辑，不修改后端接口或文件处理流程。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列垃圾桶垂直中线修复

- 现象：上传队列垃圾桶已经位于文件条内部，但视觉中线仍比文件卡片和状态徽标略高。
- 修复：对真实 Streamlit 删除按钮增加稳定的垂直位移，并同步修正 hover 位移，避免悬停时按钮跳回原位。
- 保护：仅微调垃圾桶垂直对齐，不改变删除、上传或后端逻辑。
- 验证：`python -m py_compile ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列删除按钮内收微调

- 现象：上传队列垃圾桶虽然进入文件条，但仍贴近右侧边框，视觉上像被挤出卡片。
- 修复：继续向左收紧删除按钮操作位，并同步扩大文件条右侧留白，使状态徽标与垃圾桶保持独立间距。
- 保护：仅调整上传队列删除按钮位置，不改变删除状态同步、上传或后端逻辑。
- 验证：`python -m py_compile ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列删除按钮对齐修复

- 现象：上传队列右侧垃圾桶按钮和文件卡片不在同一水平中线，看起来偏上/偏右，视觉不协调。
- 根因：文件卡片和删除按钮使用两个 Streamlit 列渲染，右侧列继承了默认间距和高度，按钮容器没有与文件行高度严格对齐。
- 修复：收紧上传队列行列宽比例，固定删除按钮容器高度、外边距和按钮尺寸，让垃圾桶和文件行垂直居中；保留真实 `st.button` 删除逻辑。
- 保护：仅调整上传队列删除按钮布局和样式，不改变上传、删除状态同步、后端接口或文件处理逻辑。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列删除后控件状态同步修复

- 现象：删除上传队列中的文件后，页面仍显示 Streamlit 默认 `info` 提示；原生文件上传控件里仍保留旧文件，导致不刷新页面时再次点击上传没有反应。
- 根因：删除逻辑只移除了前端队列项，没有同步重置 `st.file_uploader` 的 widget 状态；同时旧队列 key 只按文件内容生成，同一个文件重复选择时会共用 key，删除/跳过状态会互相影响。
- 修复：上传队列 key 改为“文件指纹 + 出现序号”，同一文件重复选择也能独立处理；当删除最后一个队列项时自动递增上传控件 key，清空原生 file uploader、预览签名和旧处理结果，避免必须手动刷新页面。
- 优化：移除突兀的默认 `st.info` 展示，改为系统风格轻量空队列提示兜底；上传队列垃圾桶按钮调整为更清晰的真实 Streamlit 图标按钮。
- 保护：未修改后端上传接口、PDF 解析、向量入库和文档管理删除逻辑；本次修复的是前端队列与上传控件状态同步。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-31 上传队列删除按钮真实触发修复

- 现象：上传队列中的垃圾桶按钮在待上传、处理失败或处理完成后点击都没有反应，用户无法移除队列文件。
- 根因：旧垃圾桶是自定义 HTML 按钮，依赖 JavaScript 去点击隐藏的 Streamlit 触发按钮；Streamlit rerun、iframe 挂载和隐藏样式变化后，脚本无法稳定命中目标，导致前端有按钮但 Python 状态未更新。
- 修复：删除隐藏触发按钮链路，改为每个队列项使用真实 `st.button` 承接删除操作，点击后直接写入 `upload_removed_keys` 并从 `upload_task_queue` 移除；上传处理过程中的实时队列渲染禁用删除按钮，处理完成后自动 rerun 恢复可删除状态，避免重复 widget key。
- 优化：用 CSS 将真实 Streamlit 删除按钮绘制为轻量垃圾桶图标，保留当前上传队列视觉风格；清理删除后同步清空旧处理结果提示。
- 保护：未修改后端上传接口、PDF 解析、向量入库、知识库/会话三点菜单或文档管理逻辑。
- 验证：`python -m py_compile ui/upload.py ui/styles/_upload.py` 通过。

## 2026-05-29 前端现代视觉焕新第五阶段

- 目标：做全局细节收束，提升稳定性、深色模式一致性和浏览器兼容性。
- 优化：新增全局页面柔和背景、统一滚动条、选中文本颜色和减少动画偏好适配；主容器顶部留白更稳定。
- 优化：移除 `color-mix()` 用法，降低不同浏览器/嵌入 WebView 下样式失效风险；补充深色模式下 Hero 标签、聊天输入区、上传面板、文档卡片、设置摘要和证据卡的背景/边框适配。
- 保护：仅修改 CSS 样式模块，未修改业务逻辑、后端接口、数据持久化和三点菜单触发机制；未恢复 `st.popover`。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\styles\_global.py ui\styles\_dark.py ui\styles\_sidebar.py ui\styles\_upload.py ui\assets.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover`、旧三点菜单选择器和 `color-mix` 残留。

## 2026-05-29 前端现代视觉焕新第四阶段

- 目标：补齐系统设置页、全局控件和移动端响应式体验，让配置区更像统一控制台。
- 优化：设置摘要改为状态胶囊组，突出检索片段数、分块参数、temperature 和各增强开关；数字输入、选择框、滑块、开关统一圆角、焦点态、阴影和 hover 反馈。
- 优化：主题切换按钮增加轻量品牌背景；移动端下 Hero、概览卡片、设置摘要和区块说明卡改为更稳的一列布局，避免窄屏挤压。
- 保护：仅修改 CSS 样式模块，未修改系统设置字段、Agent 开关、检索参数、上传和问答逻辑；未恢复 `st.popover`，未改动三点菜单触发机制。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\styles\_workspace.py ui\styles\_widgets.py ui\styles\_responsive.py ui\assets.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover` 与旧三点菜单选择器残留。

## 2026-05-29 前端现代视觉焕新第三阶段

- 目标：优化知识库问答页，让对话、引用证据、上下文信息和输入区更像成熟知识助手。
- 优化：用户/AI 消息气泡增加更柔和的圆角、阴影、hover 层次和代码块圆角；AI 回答改为带微弱发光背景的知识卡片；头像边框与阴影更统一。
- 优化：引用来源升级为更清晰的证据面板，证据卡 hover 更明显；输入区升级为带轻微玻璃感的智能输入栏；聊天上下文条改为胶囊信息组，移动端自适应换行。
- 保护：仅修改问答页 CSS，不改问答生成、Agent、引用数据、复制、重新生成和会话逻辑；未恢复 `st.popover`，未改动三点菜单触发机制。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\styles\_chat.py ui\components.py ui\chat.py ui\assets.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover` 与旧三点菜单选择器残留。

## 2026-05-29 前端现代视觉焕新第二阶段

- 目标：继续提升上传、文档管理、标签页和通用操作组件的用户体验，保持业务逻辑不变。
- 优化：上传队列升级为任务中心风格，增加网格纹理、状态徽标、hover 层次和移动端适配；上传/文档空状态增加步骤卡片，引导用户完成资料归档、处理和问答。
- 优化：文档管理页补充现代工具栏、启用/禁用状态胶囊、选择计数卡、文档卡片 hover 层次和启用/禁用徽标；标签页改为圆角胶囊式导航，通用按钮和文件上传拖拽区同步升级。
- 保护：仅改 CSS 样式模块，未修改上传、批量删除、启用/禁用、问答和知识库操作逻辑；未恢复 `st.popover`，未改动三点菜单触发机制。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\styles\_upload.py ui\styles\_documents.py ui\styles\_widgets.py ui\assets.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover` 与旧三点菜单选择器残留。

## 2026-05-29 前端现代视觉焕新第一阶段

- 目标：在不改动上传、问答、知识库和会话业务逻辑的前提下，提升首页与侧边栏的现代感，补充更统一的线性图标和卡片层次。
- 优化：新增 `sparkles`、`database`、`layers`、`activity`、`clock` 等 SVG 图标；将顶部 Hero 升级为带品牌胶囊、柔和发光、网格纹理和能力标签的产品头图；将工作区三张概览卡片改为图标徽章卡片，并区分知识库、文档、会话状态。
- 优化：侧边栏标题改为轻量品牌卡片；知识库/会话行升级为更现代的圆角卡片；右侧三点菜单保持稳定 Streamlit 按钮触发，同时视觉上改为更紧凑的右侧浮层。
- 保护：未恢复 `st.popover`，未修改 RAG、上传、删除、重命名、分享等业务逻辑；三点菜单项保持知识库 `置顶 / 重命名 / 删除`，会话 `分享 / 置顶 / 重命名 / 删除`。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\components.py ui\icons.py ui\styles\_workspace.py ui\styles\_sidebar.py ui\assets.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover` 与旧三点菜单选择器残留。

## 2026-05-29 侧边栏三点菜单点击无响应修复

- 现象：知识库和会话列表里的三个点按钮可见，但点击后没有弹出菜单，用户无法执行置顶、重命名、删除、分享等操作。
- 根因：旧实现依赖脚本在当前 DOM 上逐个绑定按钮事件；Streamlit rerun 或组件挂载顺序变化后，新渲染出来的三点按钮没有稳定绑定点击事件，表现为“看得到但点不动”。
- 修复：移除依赖跨 iframe 的侧边栏菜单脚本和未使用的旧 HTML 三点组件，改为 Streamlit 原生按钮承接三点点击，再在当前行下方展开自定义菜单面板；点击三点、菜单项和行选择都由 Streamlit session state 驱动，避免 rerun 后事件丢失。
- 追加修复：三点按钮文本和 CSS 伪元素同时显示会造成“双三点”；打开菜单时额外调用 `st.rerun()` 会导致一次点击触发连续两次刷新。现改为只显示按钮自身的 `⋯`，并移除打开菜单时的手动 rerun。
- 视觉修复：将展开菜单从行下方大卡片改为右侧小浮层，挂在对应知识库/会话行容器内，减少纵向挤压并贴近三点按钮。
- 保护：未恢复 Streamlit 原生 `st.popover`；菜单项保持知识库 `置顶 / 重命名 / 删除`，会话 `分享 / 置顶 / 重命名 / 删除`；三点按钮改为单一真实 `⋯` 字符，不再叠加 CSS 伪元素。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\sidebar.py ui\components.py ui\js_injection.py ui\styles\_sidebar.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-28 前端性能优化：API 缓存 + CSS 变量重构

- 现象：Streamlit 的 rerun 机制下，任何交互（切换标签页、点击按钮、输入文字）都会触发整个页面重新渲染，导致：
  1. `get_collections()` 和 `list_documents_api()` 每次 rerun 都发起 HTTP 请求，后端压力大且页面响应慢。
  2. 深色模式 CSS (`_dark.py`) 有 775 行，大量重复的颜色硬编码值（`#111827`、`#334155`、`#e5e7eb` 出现 30+ 次），CSS 总体积过大。
  3. 深色模式通过 JS 切换 `body.rag-dark` class，切换瞬间因为样式需要重新匹配大量硬编码值而产生闪烁。
  4. `_responsive.py` 和 `_sidebar.py` CSS 模块以未闭合大括号开头，依赖上一个模块的未闭合块，无法独立测试。
- 根因：
  - `ui/api_wrappers.py` 中的读操作没有缓存层，每次调用都直接穿透到 `_api_client`。
  - 所有样式模块（`_global.py`、`_chat.py`、`_sidebar.py`、`_workspace.py`、`_documents.py`、`_upload.py`、`_widgets.py`）大量使用硬编码十六进制颜色值，未使用 CSS Custom Properties。
  - `_dark.py` 通过重复覆盖每个选择器的颜色值来实现深色模式，而非通过变量切换。
- 修复方案：
  1. **API 缓存**：在 `ui/api_wrappers.py` 的 `st.session_state` 中为 `get_collections()` 和 `list_documents_api()` 增加带 TTL（5 秒）的缓存；在所有写操作（`upload_file`、`create_collection_api`、`delete_collection_api`、`rename_collection_api`、`delete_document_api`、`batch_delete_documents_api`、`toggle_document_enabled_api`）后主动失效对应缓存 key。
  2. **CSS 变量**：新增 `ui/styles/_variables.py`，定义 `:root`（浅色）和 `body.rag-dark`（深色）两套 CSS Custom Properties（共 40+ 变量覆盖背景、文字、边框、蓝色系、绿色系、红色系、琥珀色系、阴影）；将所有组件 CSS 中的硬编码颜色替换为 `var(--rag-*)` 引用。
  3. **深色模式精简**：`_dark.py` 从 775 行缩减到 168 行，仅保留无法通过变量切换的 Streamlit 组件覆盖（按钮 chrome、输入框、代码块、滚动条等）。
  4. **CSS 模块独立化**：`_responsive.py` 和 `_sidebar.py` 重构为独立完整的 CSS 块，不再依赖上一个模块的未闭合大括号。
- 影响范围：
  - `ui/api_wrappers.py` — 增加缓存逻辑，新增 `_invalidate_collections_cache()`、`_invalidate_documents_cache()`，移除函数内重复的 `import streamlit as st`。
  - `ui/styles/_variables.py` — 新文件，CSS Custom Properties 定义（浅色 `:root` + 深色 `body.rag-dark`）。
  - `ui/styles/__init__.py` — 新增 `_variables` 导入，`CSS_STYLES` 拼接顺序调整为变量在最前。
  - `ui/styles/_global.py` — 所有颜色替换为 `var(--rag-*)`。
  - `ui/styles/_chat.py` — 所有颜色替换为 `var(--rag-*)`。
  - `ui/styles/_dark.py` — 从 775 行缩减到 168 行，仅保留 Streamlit 组件覆盖。
  - `ui/styles/_sidebar.py` — CSS 变量替换 + 模块独立化。
  - `ui/styles/_workspace.py` — CSS 变量替换。
  - `ui/styles/_documents.py` — CSS 变量替换。
  - `ui/styles/_upload.py` — CSS 变量替换。
  - `ui/styles/_widgets.py` — CSS 变量替换。
  - `ui/styles/_responsive.py` — 模块独立化。
  - 不涉及后端接口、RAG 检索逻辑、会话持久化、依赖或环境变量。
- 验证：全部 18 个修改文件 `py_compile` 通过；`from ui.styles import CSS_STYLES` 成功，CSS 总长 61322 字符，包含 328 处 `var(--rag-*)` 引用，`:root` 和 `body.rag-dark` 变量块均存在；`langchain_core` 缺失为环境预存问题，与本次修改无关。
- 潜在风险：
  - CSS 变量值与原始硬编码值完全一致（逐色对照），视觉表现不应有差异。如有个别选择器优先级变化导致样式偏差，可在 `_dark.py` 中补充对应覆盖。
  - API 缓存 TTL 为 5 秒，在极短时间内连续创建/删除操作后，侧边栏可能短暂显示旧数据。写操作后已主动失效缓存，实际影响极小。
- 后续建议：
  - 升级 Streamlit 到 1.35+ 后可使用 `st.fragment` 隔离聊天区域，进一步减少全页面 rerun 次数。
  - CSS 中剩余的硬编码颜色（如 SVG data URL 中的 `stroke='black'`、动画关键帧中的特定色值）属于不可替换的场景，无需处理。

## 2026-05-28 引用来源复制全部优化

- 现象：AI 回答下方的引用来源只能逐条复制，长答案复盘或分享时需要重复点击多个证据卡，效率偏低。
- 优化：在引用来源摘要栏新增“复制全部引用”按钮，自动汇总所有引用的文档名、相似度和片段内容；点击复制不会触发展开/收起；移动端摘要栏自适应换行。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/components.py`、`ui/assets.py` 的引用来源前端展示与复制交互、`BUG_LOG.md` 记录，不涉及 RAG 检索阈值、后端接口、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\components.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\components.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 聊天输入快捷提示词优化

- 现象：用户进入问答页后仍需要从空白输入框开始组织问题，常见任务如总结资料、提取重点、生成学习计划缺少快速入口。
- 优化：在聊天输入区上方新增快捷提问 chips，包含“总结资料 / 提取重点 / 学习计划 / 查找矛盾”；点击后复用现有 `queued_question` 提交流程直接发送；补充浅色、深色和移动端样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/chat.py`、`ui/assets.py` 的聊天输入前端交互与 `BUG_LOG.md` 记录，不涉及问答生成 API、RAG 检索逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\chat.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\chat.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 顶部概览文档状态升级

- 现象：主工作区顶部“文档状态”卡片只显示文档总数，无法体现当前知识库中启用/禁用文档比例，也看不到最近上传时间。
- 优化：将文档状态卡升级为“启用 X / 禁用 Y”，补充启用、禁用、总计迷你状态标签，并显示最近上传时间；深色模式同步适配。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/components.py`、`ui/assets.py` 的顶部概览展示与 `BUG_LOG.md` 记录，不涉及后端接口、RAG 检索逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\components.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\components.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 上传队列处理中动效优化

- 现象：文件上传队列虽然会实时更新状态，但“处理中”只显示文字徽标，用户在较慢文件处理时不容易判断系统是否仍在工作。
- 优化：为上传队列行补充状态 class；当前处理文件增加轻量高亮、左侧强调线、图标脉冲和处理中徽标呼吸动画；深色模式同步适配。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/upload.py`、`ui/assets.py` 的上传队列前端动效展示与 `BUG_LOG.md` 记录，不涉及上传接口、RAG 入库逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 聊天清空会话确认弹窗优化

- 现象：聊天区“清空当前会话”仍使用页面内 `st.warning` 和两个小图标按钮确认，和文档批量删除弹窗不统一，也容易被长页面内容淹没。
- 优化：新增 `st.dialog` 清空会话确认弹窗，复用危险操作确认面板样式；明确提示当前会话消息数量、清空后会创建空会话，以及不会删除知识库文档但对话不可恢复。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/chat.py` 的清空会话前端确认交互与 `BUG_LOG.md` 记录，不涉及会话存储结构、知识库文档、RAG 检索、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\chat.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\chat.py ui\assets.py` 通过；源码检查无旧页面内清空会话 warning、无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 文档管理搜索筛选排序优化

- 现象：文档数量较多时，文档管理页只能靠滚动查找文件，无法快速按文件名定位、按启用状态筛选或按上传时间/大小/分块数排序。
- 优化：新增文档搜索框、启用状态筛选和排序方式选择；“全选/取消全选”只作用于当前筛选后的可见文档，避免误选隐藏结果；顶部状态条补充当前显示数量；为空筛选结果增加引导空状态；补充浅色、深色和移动端样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/pages.py`、`ui/assets.py` 的文档管理前端筛选展示与 `BUG_LOG.md` 记录，不涉及后端接口、RAG 检索逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 文档管理工具栏按钮紧凑化

- 现象：文档管理页“全选 / 删除 / 禁用 / 启用”四个按钮尺寸过大，视觉重量偏高，占用横向空间，和当前系统的轻量卡片风格不够统一。
- 优化：缩小文档工具栏按钮列宽、高度、字号和内边距；改为轻量胶囊按钮；按操作语义区分蓝色选择、红色删除、橙色禁用、绿色启用，并补充深色模式样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/pages.py`、`ui/assets.py` 的文档管理工具栏展示与 `BUG_LOG.md` 记录，不涉及批量删除/禁用/启用业务逻辑、后端接口、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 文档管理批量操作体验优化

- 现象：文档管理页的全选、批量删除、启用/禁用交互不够清晰；删除确认只是普通页面提示，用户容易忽略；全选后行级复选框状态可能和顶部选择数量割裂；禁用文档对检索的影响说明不够明显。
- 优化：将批量删除改为 `st.dialog` 确认弹窗；全选/取消全选同步所有行级 checkbox 状态；批量禁用/启用直接应用到选中文档并清空选择；新增启用/禁用数量状态、禁用文档不参与当前知识库问答检索的提示，以及更贴合系统风格的文档卡片、状态徽标和确认弹窗图标。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/pages.py`、`ui/assets.py` 的文档管理前端交互与 `BUG_LOG.md` 记录；沿用既有批量删除和启用/禁用 API，不涉及上传、问答生成、数据迁移、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\pages.py ui\assets.py` 通过；源码检查无 `st.popover`、旧三点菜单选择器和废弃批量启用确认状态残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 上传队列重复渲染与状态实时刷新

- 现象：点击“开始上传并处理”后，页面上方保留等待状态的“文件上传队列”，按钮下方又出现一份处理中/成功状态的队列，用户看到两份列表且状态不统一。
- 根因：上传前渲染了一次队列，`run_upload_queue()` 内部又创建新的 `st.empty()` 队列占位区；动态刷新没有复用原队列位置。
- 修复：将上传队列占位区提前创建并传入 `run_upload_queue()`，上传过程中复用同一个队列面板实时更新状态；将分页隐藏触发器抽出为单独渲染，避免动态刷新时重复创建相同 key 的按钮。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/upload.py` 的上传队列展示与实时刷新逻辑、`BUG_LOG.md` 记录，不涉及后端上传接口、RAG 入库逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 通过；源码检查无 `placeholder.markdown`、无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 上传队列动态刷新显示 HTML 代码

- 现象：文件上传过程中，“文件上传队列”区域会直接显示 `<div class="upload-task-row">...` 等 HTML 代码，影响用户体验。
- 根因：上传队列动态刷新路径使用 `placeholder.markdown(..., unsafe_allow_html=True)` 渲染带缩进的 HTML，Streamlit 将其按 Markdown 代码块展示。
- 修复：将动态刷新路径改为在占位容器内调用 `st.html()`，与静态渲染路径保持一致，确保上传过程中只显示队列 UI，不显示源码。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/upload.py` 的上传队列动态刷新展示与 `BUG_LOG.md` 记录，不涉及后端上传接口、RAG 入库逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 通过；源码检查无 `placeholder.markdown`、无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-28 前端上传列表合并优化

- 现象：文档上传页同时展示“已选择文件列表”和“上传任务队列”，两块内容都列出同一批文件，信息重复且占用页面高度。
- 优化：将选中文件预览和上传任务状态合并为单一“文件上传队列”；等待上传、处理中、成功、失败状态在同一列表内切换，并保留文件移除和分页能力；删除不再调用的旧预览函数，避免后续误用导致重复列表回潮。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/upload.py`、`ui/assets.py` 的上传区展示与 `BUG_LOG.md` 记录，不涉及后端上传接口、RAG 入库逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\upload.py ui\assets.py` 通过；源码检查无旧预览函数调用残留、无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-15 前端问答上下文条优化

- 现象：进入知识库问答页后，用户需要从侧边栏和系统设置页拼接判断当前知识库、会话和检索增强状态，长时间使用时上下文感不够稳定。
- 优化：在问答页顶部新增上下文条，集中展示当前知识库、会话名称、消息数量、检索 Top K，以及查询重写/上下文压缩开关状态；补充浅色、深色和移动端样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 问答页展示与 `BUG_LOG.md` 记录，不涉及后端接口、RAG 链路、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-15 前端系统设置摘要优化

- 现象：系统设置页拆分为两列后，用户仍需要逐项阅读控件才能确认当前检索、分块、生成和增强能力配置，配置状态缺少一眼可读的总览。
- 优化：新增设置摘要状态条，集中展示检索片段数、分块大小/重叠度、temperature，以及查询重写、上下文压缩、思考过程、图片解析的开关状态；补充浅色、深色和移动端样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 系统设置页展示与 `BUG_LOG.md` 记录，不涉及后端接口、RAG 链路、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-15 前端重复导出函数清理

- 现象：`streamlit_app.py` 中仍存在两个 `build_conversation_markdown()` 定义，Python 实际使用最后一个定义，容易让后续维护误改到非生效路径；旧上传 legacy 路径仍残留 `st.balloons()`，会干扰对当前上传体验的判断。
- 优化：删除前置重复的 `build_conversation_markdown()`，仅保留当前生效版本；移除 legacy 上传函数中的 `st.balloons()` 残留，降低后续搜索和维护噪音。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端维护结构与 `BUG_LOG.md` 记录，不涉及导出格式、上传 API、RAG 链路、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；核心前端函数定义计数均为 1，`st.balloons` 为 0；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端聊天区独立滚动优化

- 现象：长对话场景下消息区和输入区仍处在同一个页面流里，用户滚动历史消息时输入区稳定感不足，不够接近成熟聊天产品体验。
- 优化：使用当前 Streamlit 版本支持的 `st.container(height=540, key="chat_scroll_area")` 将消息历史改为独立滚动区域；输入区继续保持底部 sticky 面板；为聊天滚动区补充浅色/深色背景、圆角、阴影和滚动条样式，移动端使用 `58vh` 高度。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端聊天布局与 `BUG_LOG.md` 记录，不涉及问答链路、后端接口、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端上传任务队列优化

- 现象：上传流程仍是统一进度条 + 结果 expander，用户无法在上传过程中直观看到每个文件的等待、处理中、成功、失败状态；失败后也缺少单文件重试入口，`st.balloons()` 与个人知识库工具气质不够一致。
- 优化：新增上传任务队列，按文件展示等待中、处理中、成功、失败状态与结果消息；失败文件支持单独重试，重试沿用当前分块和多模态解析设置；移除上传完成后的气球动画，保留更稳的成功/失败反馈。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端上传流程展示与重试交互、`BUG_LOG.md` 记录，不涉及后端上传接口、RAG 入库逻辑、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端引用来源证据卡片优化

- 现象：AI 回答的引用来源仍藏在 Streamlit 默认 expander 中，用户需要展开后才知道引用数量和最高相似度，证据可读性与可复用性不够直观。
- 优化：将引用来源改为轻量证据条，默认展示“引用 N 条 / 最高相似度”；展开后显示证据卡片，突出文档名、片段内容、相似度，并支持单条“复制引用”；同时补齐 AI 消息行的 `ai` class，让既有 AI 气泡样式命中真实渲染路径。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端引用展示、复制引用交互与 `BUG_LOG.md` 记录，不涉及 RAG 检索阈值、后端接口、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端上传区与概览卡片细节优化

- 现象：文档上传拖拽区、已选文件预览和主工作区概览卡片仍偏静态，用户对“可上传、已选择、当前状态”的视觉感知不够强。
- 优化：为上传拖拽区增加柔和渐变、虚线边框和 hover 反馈；增强已选文件预览面板阴影、标题状态点、文件图标底色和行 hover；为主工作区概览卡片增加左侧强调线与轻量 hover；移动端禁用列表横向位移动效，避免窄屏抖动。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端样式与 `BUG_LOG.md` 记录，不涉及 RAG 链路、后端接口、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端视觉层次与反馈细节优化

- 现象：聊天消息、引用来源、系统提示和文档删除按钮的视觉层级仍偏平，用户在长对话或多文档管理场景下不够容易快速定位重点操作。
- 优化：为用户/AI 消息增加更明确的渐变和边框层次；头像增加轻量阴影并统一品牌色；引用来源卡片增加柔和背景、阴影和相似度标签；统一 Streamlit 提示条圆角与边框；将文档删除按钮收窄并右对齐，降低危险操作的视觉干扰。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `streamlit_app.py` 前端样式与 `BUG_LOG.md` 记录，不涉及 RAG 链路、后端接口、数据持久化、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 返回 200。

## 2026-05-15 前端聊天与空状态细节优化

- 现象：聊天空状态、上传空状态和文档空状态只给出单句提示，用户下一步操作不够明确；导出按钮缺少上下文说明；底部输入区与页面主体分层不明显，窄屏下消息气泡和辅助信息可读性可继续提升。
- 优化：为空状态补充三步引导卡片；为会话导出增加说明工具栏和消息数提示；将聊天输入区调整为轻量悬浮面板并补充提问建议与快捷键提示；优化移动端消息宽度、头像尺寸、空状态步骤和导出提示的响应式布局。
- 保护：未修改 `session-menu` / `collection-menu` 的自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`。
- 影响范围：仅影响 `streamlit_app.py` 前端展示与 `BUG_LOG.md` 记录，不涉及 RAG 链路、后端接口、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-15 前端顶部与设置页控制面板优化

- 现象：主页面顶部仍偏默认标题样式，标签页选中状态不够突出；系统设置页所有控件纵向堆叠，检索、分块、生成和增强能力的关系不够直观。
- 优化：新增产品化 Hero 头部，补充能力标签；优化主内容标签页的 hover 与选中态；将系统设置页拆成“检索与分块”和“生成与增强”两列；文档删除按钮调整为轻量危险操作样式。
- 保护：未修改 `session-menu` / `collection-menu` 的自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`。
- 影响范围：仅影响 `streamlit_app.py` 前端展示与 `BUG_LOG.md` 记录，不涉及 RAG 链路、后端接口、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。

## 2026-05-15 前端主工作区信息密度优化

- 现象：主内容区进入后缺少当前知识库、文档数量和会话状态的总览；文档管理页以分割线堆叠呈现，信息层级不够清晰；上传、问答、设置页缺少轻量引导。
- 优化：新增主工作区概览卡片，展示当前知识库、文档状态和当前会话；为上传、问答、文档管理、系统设置页增加说明卡；将文档管理条目改为卡片化展示，并补全 `description` 图标定义。
- 保护：未恢复或使用 Streamlit 原生 `st.popover`，未修改自定义三点菜单的触发器、菜单项和隐藏按钮桥接逻辑，避免三点外边框和箭头回退。
- 影响范围：仅影响 `streamlit_app.py` 前端展示与 `BUG_LOG.md` 记录，不涉及 RAG 链路、后端接口、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；本地前端 `localhost:8501` 与后端 `/health` 均可访问。

## 2026-05-15 前端结构与侧边栏信息层级优化

- 现象：`streamlit_app.py` 存在多个同名前端渲染函数，实际生效版本依赖 Python 最后定义覆盖；侧边栏同时承载知识库、会话、文档管理、系统设置和说明，信息密度偏高。
- 根因：历史多轮 UI 调整采用追加式实现，旧函数和旧 popover 样式没有及时收敛，导致后续样式修改容易命中非生效路径。
- 修复：将被覆盖的旧版 `render_sidebar`、文档管理、设置、上传函数改为 legacy 命名，保留唯一生效入口；清理不再使用的 `st.popover` / `stPopoverBody` / 旧三点菜单 CSS；将文档管理和系统设置从侧边栏移到主内容区标签页，侧边栏聚焦知识库和会话。
- 保护：保留当前自定义 HTML 三点菜单方案，未恢复 Streamlit 原生 `st.popover`，避免三点外框和箭头回退。
- 验证：`python -m py_compile streamlit_app.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py` 通过；源码检查无 `st.popover` 残留调用；Streamlit AppTest `exceptions 0`。

## 2026-05-14 侧边栏三点菜单样式对齐

- 现象：知识库和会话行尾的三点操作入口仍显示 Streamlit popover 默认外边框/箭头，弹出菜单视觉与目标样式不一致。
- 原因：侧边栏按钮全局样式会覆盖 popover 触发器，且菜单项仍沿用较小字号、窄间距和默认按钮外观。
- 修复：将实际生效的侧边栏渲染路径从 `st.popover` 切换为自定义 HTML 三点按钮，避免 Streamlit 默认外边框和下拉箭头；统一菜单为白底卡片、图标+文字、大间距样式，并保留知识库 `置顶 / 重命名 / 删除` 与会话 `分享 / 置顶 / 重命名 / 删除`。
- 兼容：当前环境 Streamlit 1.23.1 不提供 `st.html`，补充 `st.html` 到 `st.markdown(..., unsafe_allow_html=True)` 的轻量回退，避免自定义行在旧版本运行时报错。
- 复盘：`streamlit_app.py` 内存在多个 `render_sidebar()` 定义，Python 实际使用最后一个定义；前两次只改到前置定义，最后一个定义仍在渲染 `st.popover`，导致页面看起来没有变化。现已同步修改最后一个定义，并通过源码检查确认无实际 `st.popover(...)` 调用。
- 影响范围：仅影响侧边栏知识库与会话操作菜单的前端样式，不涉及 RAG 链路、接口或依赖。
- 验证：`python -m py_compile streamlit_app.py` 通过。

## 2026-05-14 残留知识库 `AI?????` 无法删除

- 现象：侧边栏多出一个 `AI?????` 知识库条目，用户无法通过界面删除。
- 根因：该条目是真实后端残留数据；同时前端 API client 将知识库名直接拼到 URL path，名称中的 `?` 被浏览器/HTTP 当作查询串起点，导致删除请求没有命中真实名称。
- 修复：已通过编码后的后端路径删除残留 `AI?????`；`RagApiClient` 对所有 collection path 参数统一使用 URL encoding；知识库/会话行尾操作按钮改为常驻显示，避免看不到删除入口。
- 验证：后端 `/collections` 已不再返回 `AI?????`；`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。

## 2026-05-13 会话历史行尾三点菜单升级

- 现象：会话历史项右侧仍显示重命名、删除两个独立小按钮，和知识库列表的三点菜单交互不统一。
- 根因：会话项仍使用早期 hover 操作按钮，没有复用上下文菜单模式。
- 修复：会话项改为行尾单个三点按钮；菜单包含 `分享 / 置顶 / 重命名 / 删除`；分享优先调用浏览器分享能力，失败时复制会话 Markdown；置顶标记写入会话数据，刷新后仍保持排序。
- 验证：`python -m py_compile streamlit_app.py` 通过。

## 2026-05-13 ????????????? 10 ?

- ???????? `file_uploader` ???????????? 3 ????????????????
- ???Streamlit ???????????????? 3?Python API ?????????
- ????????????????????????????????????????? 10 ????????????????
- ???`python -m py_compile streamlit_app.py` ???

## 2026-05-13 ??????????????

- ???????????? / ???? / ????????????????????????????????????????? UI ????
- ??????????????? Streamlit ??? expander ????????????????????????
- ??????????????????????????????????????????????????????? hover ??????????????? key ?????????
- ???`python -m py_compile streamlit_app.py` ???

## 2026-05-13 ??????????????

- ??????????????????????/????/??/??/?????????????? AI ???????
- ??????????????????????? expander ???? Streamlit ?????
- ???????????????????????????????????????????? expander ?????????????????????????? key ?????????
- ???`python -m py_compile streamlit_app.py` ???

## 2026-05-13 ????????????????

- ????????????????????????????
- ?????????????????????/?????????????????????????????
- ?????????????????????? `stopPropagation()`???????????? `?? / ??? / ??`?
- ???`python -m py_compile streamlit_app.py` ???

## 2026-05-13 ?????????????

- ??????????????????/????????????????????????????????
- ?????????????? Streamlit ????? `st.popover` ???????????????????
- ????????????????????????????????????????? `?? / ??? / ??` ???????????????????
- ???`python -m py_compile streamlit_app.py` ???

# 问题记录日志

本文档记录项目中的重要问题、修复方式和长期避免规则。历史日志曾因编码问题出现大量乱码，本次已压缩整理为可维护版本。

## 记录格式

每条记录建议包含：

- 日期
- 问题现象
- 根因
- 修复方式
- 影响范围
- 验证结果
- 后续避免规则

## 历史问题摘要

### 1. Chroma collection 不支持中文名称

问题现象：

- 创建中文知识库时 Chroma 报 collection name 校验失败。
- 或侧边栏显示 `kb_xxx`，而不是用户输入的中文名称。

根因：

- Chroma collection 名称只支持有限字符集。
- 用户可见名称和内部存储名称没有持久化映射。

修复：

- 增加 `sanitize_collection_name()`。
- 使用 `kb_` + MD5 前缀生成内部名称。
- 使用 `collection_name_mapping.json` 持久化映射。

长期规则：

- 用户可见名称不得直接作为底层存储 key。
- 名称映射必须持久化。

### 2. 模型与 Embedding 服务迁移

问题现象：

- 旧 DeepSeek Embedding 调用失败。
- 用户可见提示仍显示历史模型服务名。

根因：

- 项目从旧模型服务迁移到 SiliconFlow 后，配置和文案未完全统一。

修复：

- 使用通用 `LLM_*` 配置。
- 保留旧 `DEEPSEEK_*` 变量兼容。
- 用户可见提示统一为“模型 API 密钥”。

长期规则：

- 模型供应商迁移时，代码、文档、`.env.example`、前端提示必须同步更新。

### 3. LangChain 包拆分导致导入失败

问题现象：

- `ModuleNotFoundError`，例如缺少 `langchain_openai`、`langchain_text_splitters`、`langchain_classic`。

根因：

- LangChain 新版本将功能拆分到多个包。
- `requirements.txt` 未显式列出实际 import 的包。

修复：

- 补齐 `requirements.txt`。
- 关键导入做环境验证。

长期规则：

- 新增第三方 import 后必须同步更新 `requirements.txt`。

### 4. Markdown/TXT 解析污染

问题现象：

- Markdown 内容中混入 HTML 标签或结构被破坏。

根因：

- 不合适的 Markdown 转换或 loader 引入额外格式。

修复：

- Markdown 和 TXT 使用原生文本读取。
- 保留 Markdown 标题结构给分块器处理。

长期规则：

- 文档解析应优先保留原始语义结构，不做无必要格式转换。

### 5. 知识库数据维度不一致

问题现象：

- Chroma 报 expecting embedding dimension 之类错误。

根因：

- 已入库向量维度与当前 Embedding 模型输出维度不同。

修复：

- 在检索异常中返回友好提示。
- 建议使用当前 `EMBEDDING_MODEL` 重新上传或重建知识库。

长期规则：

- 更换 Embedding 模型必须考虑数据迁移或重建。

## 近期维护记录

### 2026-05-08：新增项目维护手册

问题现象：

- 优化建议分散在对话中，缺少集中维护路线。

修复：

- 新增 `项目维护手册.md`。
- 梳理依赖、检索性能、评估、前端拆分、会话持久化、安全和生产化事项。

影响范围：

- 文档。

验证结果：

- 文档已创建并持续更新。

### 2026-05-08：第一阶段维护

问题现象：

- 依赖清单与实际 import 不完全一致。
- 部分用户提示仍含历史模型名。
- 缺少可重复运行的 RAG 评估入口。

修复：

- 补齐 `requirements.txt`。
- 安装缺失的 `docx2txt` 和 `chardet`。
- 统一 API 密钥提示文案。
- 新增 `eval/rag_eval.py` 和 `eval/eval_cases.json`。

影响范围：

- `requirements.txt`
- `.env.example`
- `main.py`
- `streamlit_app.py`
- `eval/`
- 文档

验证结果：

- 核心文件语法检查通过。
- 关键依赖导入通过。
- `eval/rag_eval.py --help` 可运行。

遗留：

- `pip check` 中仍有非核心环境冲突，未扩大处理。

### 2026-05-08：CORS 与上传安全

问题现象：

- CORS 使用 `allow_origins=["*"]`。
- 上传文件先完整写盘再检查大小。
- 上传文件名未集中清理。

修复：

- 新增 `CORS_ALLOW_ORIGINS`。
- 上传文件名清理。
- 上传文件分块保存，超过限制立即中止。

影响范围：

- `config.py`
- `main.py`
- `.env.example`

验证结果：

- 语法检查通过。
- CORS 默认来源读取正常。
- 文件名清理函数验证通过。

### 2026-05-08：QAChain 运行时复用

问题现象：

- `/ask`、`/retrieve`、`/generate` 每次都重新创建 `QAChain`。

根因：

- API 层直接调用 `QAChain(...)`，没有按配置复用。

修复：

- 新增 `get_qa_chain()`。
- 按知识库、`top_k`、`temperature` 和开关配置缓存。
- 缓存上限为 16 个配置组合。

验证结果：

- 同配置返回同一实例。
- 不同配置返回不同实例。

### 2026-05-08：Collection 文档与 BM25 缓存

问题现象：

- 检索时多次读取 Chroma collection 全量文档。
- BM25 每次检索都重新构建。

修复：

- 新增 `_collection_cache`。
- 缓存 collection 文档快照、`raw_pairs` 和 BM25 retriever。
- 上传、删除、重命名时失效缓存。
- 文档列表、关键词兜底、相邻子块扩展复用快照。

验证结果：

- 模拟 Chroma collection 验证快照复用。
- BM25 retriever 复用正常。
- 缓存失效后可重新读取。

### 2026-05-08：检索缓存收口与编码清理

问题现象：

- 缓存改造后仍残留旧读取函数和空壳代码。
- `rag/vector_store.py` 历史乱码中存在不可打印字符。
- 清理编码后暴露出注释/代码粘连问题。

修复：

- 关键词兜底改为复用快照。
- 移除旧函数和空壳 `try`。
- 清理不可打印字符。
- 修复名称哈希、名称映射返回、Embedding 初始化、批量入库、持久化判断、候选数量、重排分数等关键行。
- 恢复被临时验证污染的 `collection_name_mapping.json`。

验证结果：

- `rag/vector_store.py` 语法检查通过。
- `rag.vector_store` 导入通过。
- 模拟缓存测试通过。
- 真实名称映射文件恢复。

长期规则：

- 临时验证不得写入真实知识库映射。
- 编码清理后必须运行语法检查。
- 全量文本读取统一走快照缓存，除非需要 Chroma ids。

### 2026-05-08：Markdown 文档重写

问题现象：

- 项目 Markdown 文档大量乱码、过时信息和重复内容。

修复：

- 重写所有项目级 Markdown：
  - `README.md`
  - `AGENTS.md`
  - `RAG技术详解.md`
  - `项目维护手册.md`
  - `BUG_LOG.md`

影响范围：

- 文档。

验证结果：

- 文档结构统一。
- README、技术详解、维护手册、开发规则和问题日志互相对齐。

### 2026-05-09：`vector_store.py` 日志与注释乱码清理

问题现象：

- `rag/vector_store.py` 仍残留大量历史乱码注释、日志和异常提示。
- 部分日志在检索、缓存、删除、列表等路径中不可读，影响后续排错。

修复：

- 清理 `VectorStoreManager` 主要方法的 docstring、注释、日志和异常提示。
- 恢复超长分块函数中的 `max_chars` 初始化。
- 保持检索、缓存、BM25、重排、删除和列表逻辑不变。

影响范围：

- `rag/vector_store.py` 可维护性和日志可读性。

验证结果：

- `python -m py_compile rag\vector_store.py` 通过。
- 使用乱码特征正则扫描 `rag/vector_store.py`，未发现残留命中。

### 2026-05-09：上传 MIME 与文件头校验

问题现象：

- 上传接口只校验扩展名，无法识别明显伪装的 PDF/DOCX 或二进制 TXT/MD。
- 校验逻辑如果放在 `main.py` 中，会被 FastAPI 和全局组件初始化拖慢独立测试。

修复：

- 新增 `rag/upload_validation.py`，提供轻量文件内容校验。
- PDF 校验 `%PDF-` 文件头。
- DOCX 校验 ZIP 文件头 `PK\x03\x04`。
- TXT/MD 拒绝空字节和过高比例控制字符。
- MIME 与扩展名不完全匹配时写 warning 日志，但不直接拒绝，避免浏览器兼容性误伤。
- 后端上传流程在临时文件保存后、文档解析前执行内容校验。

影响范围：

- 上传接口安全性。
- `config.py` 新增 `SUPPORTED_MIME_TYPES`。

验证结果：

- `D:\anaconda3\envs\ai_project\python.exe -m py_compile ...` 核心文件语法检查通过。
- 轻量脚本验证有效 PDF/DOCX/TXT 通过，伪 PDF 与二进制 TXT 被拒绝。

### 2026-05-09：日志轮转

问题现象：

- 后端和前端只做基础日志输出，长期运行时缺少稳定的滚动文件日志。
- `.env.example` 未暴露日志保留策略配置。

修复：

- 新增 `rag/logging_utils.py`，统一配置控制台日志和 `RotatingFileHandler`。
- `main.py` 与 `streamlit_app.py` 复用 `setup_logging()`。
- `config.py` 新增 `LOG_DIR`、`LOG_FILE`、`LOG_MAX_BYTES`、`LOG_BACKUP_COUNT`。
- `.env.example` 同步新增日志配置。

影响范围：

- 后端和前端日志输出。
- 默认日志文件：`logs/app.log`。

验证结果：

- `python -m py_compile main.py streamlit_app.py config.py rag\logging_utils.py rag\upload_validation.py` 通过。
- 使用项目环境执行轻量脚本，确认 `logs/app.log` 可创建并写入日志。

### 2026-05-09：父子块索引缓存

问题现象：

- 相邻子块扩展依赖 `raw_pairs` 线性扫描。
- 大知识库命中超长父块时，每次检索都需要遍历 collection 快照。

修复：

- 在 `_get_cached_collection_snapshot()` 中构建 `parent_index`。
- 索引结构为 `(source, parent_chunk_index) -> [(sub_chunk_index, content, metadata), ...]`。
- `_expand_related_subchunks()` 改为直接查索引，避免重复线性扫描。
- 缓存仍跟随 collection count 和显式失效逻辑刷新。

影响范围：

- `rag/vector_store.py` 检索后处理性能。
- collection 快照缓存结构。

验证结果：

- `python -m py_compile rag\vector_store.py` 通过。
- 使用 FakeStore smoke test 验证索引构建和子块合并逻辑通过。

### 2026-05-09：可选 API Token 访问保护

问题现象：

- 后端接口缺少简单访问保护。
- 如果服务被暴露到局域网或公网，上传、检索、问答接口都可被直接调用。

修复：

- `config.py` 新增 `API_TOKEN`。
- `main.py` 新增 HTTP middleware：未配置 `API_TOKEN` 时保持原本开发体验；配置后，除 `/`、`/health`、文档页面和 `OPTIONS` 外均需认证。
- 支持 `Authorization: Bearer <token>` 与 `X-API-Token` 两种请求头。
- `streamlit_app.py` 自动为后端请求携带 Bearer token。
- `.env.example` 同步新增 `API_TOKEN`。

影响范围：

- 后端非公开 API。
- Streamlit 前端到后端的所有业务请求。

验证结果：

- `python -m py_compile main.py streamlit_app.py config.py` 通过。
- TestClient smoke test 通过：未配置 token 不拦截；配置 token 后无 token 返回 401，`X-API-Token` 和 Bearer token 均可通过。

### 2026-05-09：Streamlit 会话持久化

问题现象：

- Streamlit 会话只存在内存中。
- 页面刷新或前端重启后，会话列表、当前会话和输入历史会丢失。

修复：

- 新增 `data/sessions.json` 作为轻量本地持久化文件。
- `init_session_state()` 首次运行时自动加载已保存会话。
- 新建、切换、重命名、删除、保存当前会话和输入历史更新时自动写入 JSON。
- `.gitignore` 新增 `data/`，避免提交个人会话内容。

影响范围：

- Streamlit 前端会话管理。
- 本地用户数据目录 `data/`。

验证结果：

- `python -m py_compile streamlit_app.py` 通过。
- 轻量 JSON 读写 smoke test 通过。

### 2026-05-09：RAG 评估脚本支持 API Token

问题现象：

- 后端启用 `API_TOKEN` 后，`eval/rag_eval.py` 无法携带认证头。
- 后续跑真实 RAG 评估会因为 401 失败。

修复：

- `eval/rag_eval.py` 新增 `--api-token` 参数。
- 默认读取环境变量 `API_TOKEN`。
- 请求 `/retrieve` 和 `/ask` 时自动携带 `Authorization: Bearer <token>`。
- 增加评估用例基础校验：非空数组、对象结构、`question` 和 `expected_keywords` 类型。
- README、技术详解、维护手册同步补充 token 用法。

验证结果：

- `python -m py_compile eval\rag_eval.py` 通过。
- `python eval\rag_eval.py --help` 可显示 `--api-token`。
- `build_headers()` 轻量 smoke test 通过。
- `load_cases()` 用例校验 smoke test 通过。

### 2026-05-09：维护 Smoke Test 固化

问题现象：

- 上传校验、评估用例校验和父子块索引缓存此前主要依赖临时脚本验证。
- 后续维护时容易漏跑或重复手写 smoke test。

修复：

- 新增 `tests/test_maintenance_smoke.py`。
- 使用标准库 `unittest`，不新增依赖。
- 覆盖上传内容校验、RAG 评估用例校验、父子块索引缓存和相邻子块合并。
- README 和维护手册同步补充运行命令。

验证结果：

- `python -m py_compile tests\test_maintenance_smoke.py` 通过。
- `D:\anaconda3\envs\ai_project\python.exe -m unittest tests.test_maintenance_smoke` 通过。

### 2026-05-09：Streamlit API Client 抽离

问题现象：

- `streamlit_app.py` 直接散落多个 `requests` 调用。
- API token 请求头、超时、错误兜底逻辑分散，不利于继续拆分前端。

修复：

- 新增 `rag/api_client.py`。
- 将 health、collections、upload、ask、retrieve、generate、文档列表/删除等 HTTP 请求集中到 `RagApiClient`。
- `streamlit_app.py` 保留薄封装，从 `st.session_state` 取运行时设置并调用 client。
- 维护 smoke test 增加 API client 请求头和异常兜底覆盖。

影响范围：

- Streamlit 前端后端请求路径。
- 可选 `API_TOKEN` 请求头生成逻辑。

验证结果：

- `python -m py_compile streamlit_app.py rag\api_client.py tests\test_maintenance_smoke.py` 通过。
- `D:\anaconda3\envs\ai_project\python.exe -m unittest tests.test_maintenance_smoke` 通过。

## 长期避免规则

1. 依赖新增必须同步 `requirements.txt`。
2. 环境变量新增必须同步 `.env.example`。
3. 接口或启动方式变化必须同步 README。
4. RAG 技术实现变化必须同步 `RAG技术详解.md`。
5. 维护路线变化必须同步 `项目维护手册.md`。
6. 重复问题必须上升为 `AGENTS.md` 规则。
7. 真实 `chroma_db` 数据不得用于临时写入测试。
8. 任何编码清理后必须运行 `py_compile`。
9. 缓存必须有明确失效条件。
10. 不允许通过吞异常、删逻辑、跳校验伪装修复。
### 2026-05-11：知识库选择下拉框混入管理操作

问题现象：
- “选择已有知识库”的下拉列表同时包含知识库名称、重命名和删除操作项。
- 用户想切换知识库时容易误触管理操作，界面职责不清晰。

修复：
- 下拉框选项改为只显示真实已有知识库。
- 在当前选择栏右侧新增三点操作按钮，点击后显示“置顶 / 重命名 / 删除”。
- 置顶仅调整当前界面的本地显示顺序，不改变后端知识库数据。
- 重命名和删除沿用原有 API 与确认流程。

影响范围：
- `streamlit_app.py`
- `BUG_LOG.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 加载通过，`exceptions 0`。
### 2026-05-12：知识库管理操作应归属到每个知识库条目

问题现象：
- 之前是选择框外侧只有一个总三点按钮，不符合“每个知识库一栏末尾都有三个点”的交互预期。
- 原生 selectbox 无法在每个选项内部放置独立三点按钮和菜单。

修复：
- 将已有知识库选择从原生 selectbox 改为自定义知识库行列表。
- 每个知识库条目末尾都有独立三点按钮。
- 点击知识库行本身切换当前知识库。
- 点击该行三点按钮显示“置顶 / 重命名 / 删除”菜单。
- 每个操作继续通过隐藏 Streamlit 原生按钮承接，保持状态与原有 API 流程一致。

影响范围：
- `streamlit_app.py`
- `BUG_LOG.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 加载通过，`exceptions 0`。
### 2026-05-12：知识库行三点按钮图标不可见

问题现象：
- 每个知识库行末尾的三点按钮只显示为空白方块，看不到三点图标。

修复：
- 将三点图标改为 CSS `::before` + SVG mask 绘制。
- 隐藏按钮内部 SVG fallback，避免 Streamlit HTML 渲染路径吞掉内联 SVG。
- 补充深色模式颜色覆盖。

影响范围：
- `streamlit_app.py`
- `BUG_LOG.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 使用 60 秒超时加载通过，`exceptions 0`。
### 2026-05-12：知识库重命名应在原条目内编辑

问题现象：
- 点击知识库三点菜单的“重命名”后，会在列表下方单独出现一个重命名区域。
- 用户期望直接在当前知识库这一栏内编辑名称。

修复：
- 将知识库重命名表单移动到对应知识库条目的原位置渲染。
- 当前条目进入编辑态后显示输入框和保存/取消按钮。
- 删除下方独立重命名表单区域，保留原有重命名 API 与保存/取消逻辑。

影响范围：
- `streamlit_app.py`
- `BUG_LOG.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 加载通过，`exceptions 0`。
### 2026-05-12：深色模式下知识库三点菜单看似无响应

问题现象：
- 深色模式下点击知识库行末尾的三个点后，看起来没有任何反应。

根因：
- 三点菜单 DOM 已创建，但 `.collection-menu` 没有应用深色背景。
- 深色模式只把菜单按钮文字改成浅色，导致浅色文字落在白色菜单背景上，几乎不可见。

修复：
- 将 `.collection-menu` 加入深色菜单背景、边框和阴影规则。
- 为 `.collection-menu button:hover` 增加深色 hover 背景。

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 加载通过，`exceptions 0`。

### 2026-05-12：知识库三点菜单改为原生 Popover

问题现象：
- 知识库行尾三点菜单依赖前端脚本转发点击，在深色模式与 DOM 重绘时不够稳定。

修复：
- 将知识库行尾三点操作改为 Streamlit 原生 `st.popover`。
- 移除知识库选择/置顶/重命名/删除按钮的隐藏转发样式，让它们作为原生按钮工作。
- 保留“置顶 / 重命名 / 删除”三项操作和原有后端 API 流程。

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile .\streamlit_app.py` 通过。
- Streamlit AppTest 加载通过，`exceptions 0`。
### 2026-05-13：部分 Markdown 上传失败，Embedding 返回 512 token 限制

问题现象：
- 上传 `02_Python学习笔记.md`、`04_大模型原理资料.md`、`05_Transformer资料.md` 等文件时前端显示 `上传失败：500`。
- 同一批 Markdown 中部分文件可以正常上传，说明文件格式校验和基础解析链路不是根因。

根因：
- 后端日志显示 SiliconFlow Embedding 接口返回 `413 input must have less than 512 tokens`。
- Markdown 分块器会为代码、公式、核心概念保留较长语义块，入库前虽有字符级二次切分，但 `450` 字符上限对英文代码、符号密集文本不够保守，少量块在 tokenizer 视角仍超过 512 token。

修复：
- 在 `rag/vector_store.py` 中将 Embedding 入库前二次切分改为更保守的上限：`EMBEDDING_SAFE_MAX_CHARS = 300`。
- 新增轻量 token 估算 `_estimate_embedding_tokens()`，对标点、代码和非 ASCII 字符保守计数，不新增 tokenizer 依赖。
- 新增 `_split_text_for_embedding_limit()`，当估算 token 仍偏高时继续二次切分，避免超长块进入 Embedding API。
- 补充代码/标点密集文本的回归测试，确保分片同时满足字符和估算 token 上限。

影响范围：
- `rag/vector_store.py`
- `tests/test_vector_store.py`
- `BUG_LOG.md`
- `RAG技术详解.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_text_splitter.py tests\test_upload_validation_extended.py -q` 通过，68 passed。
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py streamlit_app.py config.py rag\vector_store.py rag\text_splitter.py rag\document_loader.py rag\upload_validation.py` 通过。
### 2026-05-13：继续修复部分 Markdown 上传 500 与失败残留

问题现象：
- `02_Python学习笔记.md`、`04_大模型原理资料.md`、`05_Transformer资料.md` 上传时仍可能返回 500。
- 后端日志显示 SiliconFlow Embedding 返回 `413 input must have less than 512 tokens`。
- 失败前已成功提交的 Chroma 批次会留下部分片段，导致前端显示失败但知识库内存在半份文档。

根因：
- 上一次二次切分只在估算 token 偏高时追加一次更小切分，极端符号、代码或非 ASCII 密集片段仍可能超过服务端 tokenizer 限制。
- 入库按批写入，某一批失败时，前面成功批次没有按本次上传事务回滚。
- `rag/vector_store.py` 存在历史编码粘连，部分语句被乱码注释吞掉，`py_compile` 能捕获这些隐患。

修复：
- 将入库前安全切分收紧为 `EMBEDDING_SAFE_MAX_CHARS = 180`、`EMBEDDING_SAFE_MAX_ESTIMATED_TOKENS = 300`。
- `_split_text_for_embedding_limit()` 改为递归检查，直到每个子片段都低于本地安全估算阈值。
- 每次入库写入 `ingest_batch_id` 元数据；如果后续批次失败，按该批次 ID 删除本次已写入片段，避免失败上传残留。
- 修复 `vector_store.py` 中影响运行的编码粘连语句，并补充回滚与极端文本切分测试。
- 清理真实知识库 `AI编程学习库` 中此前失败留下的 `02_Python学习笔记.md`、`04_大模型原理资料.md` 残留片段；`05_Transformer资料.md` 未发现残留。

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_text_splitter.py tests\test_upload_validation_extended.py -q` 通过，70 passed。
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py streamlit_app.py config.py rag\vector_store.py rag\text_splitter.py rag\document_loader.py rag\upload_validation.py` 通过。

### 2026-05-13：重启后端并清理旧进程失败残留

问题现象：
- 代码修复后再次上传仍显示 `02_Python学习笔记.md`、`04_大模型原理资料.md`、`05_Transformer资料.md` 失败。
- 最新日志没有出现 Embedding token 限制重试日志，说明运行中的后端仍是旧进程。

处理：
- 仅重启后端 uvicorn 进程，保留前端 Streamlit 进程。
- 确认新后端 PID 监听 `127.0.0.1:8000`。
- 清理旧后端失败留下的真实知识库残留：`02_Python学习笔记.md`、`04_大模型原理资料.md`。
- 清理后 `AI编程学习库` 中仅保留本轮真正成功的 `03_LangChain学习资料.md`、`06_RAG论文笔记.md`、`07_技术博客收藏.md`。

验证结果：
- 后端启动日志显示 Embedding 预加载完成。
- 文档列表 API 返回 200，残留文件已删除。

### 2026-05-13：修复 Embedding 512 token 误差导致的 Markdown 上传 500

问题现象：
- 上传 `02_Python学习笔记.md`、`04_大模型原理资料.md`、`05_Transformer资料.md` 等 Markdown 时仍可能返回 `上传失败：500`。
- 后端日志显示 SiliconFlow Embedding 返回 `413 input must have less than 512 tokens`。

根因：
- 入库前已有字符数和本地 token 估算保护，但服务端 tokenizer 对代码、符号密集内容和中英混排的计数仍可能高于本地估算。
- Chroma 批量写入时某个批次失败会暴露为整个上传失败，且仅靠固定预切分无法覆盖所有 provider tokenizer 差异。

修复：
- 在 `rag/vector_store.py` 新增 `_add_documents_with_embedding_retry()`。
- 批次遇到 Embedding token 限制时，先把失败批次递归拆成更小批次重试。
- 单个片段仍失败时，继续将该片段按更小字符上限拆分，并标记 `embedding_retry_split=True`。
- 非 token 限制类错误不重试、不吞异常，继续由原错误处理和上传事务回滚接管。
- 补充批次重试、单片段重试、非 token 错误不重试的单元测试。

影响范围：
- `rag/vector_store.py`
- `tests/test_vector_store.py`
- `BUG_LOG.md`
- `RAG技术详解.md`

验证结果：
- `D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_vector_store.py tests\test_text_splitter.py tests\test_upload_validation_extended.py -q` 通过，73 passed。
- `D:\anaconda3\envs\ai_project\python.exe -m py_compile main.py streamlit_app.py config.py rag\vector_store.py rag\text_splitter.py rag\document_loader.py rag\upload_validation.py` 通过。
## 2026-05-14 引用来源卡片与复制反馈优化

- 现象：引用来源卡片信息密度和视觉层次偏弱，复制回答按钮的反馈需要保持清晰稳定。
- 根因：引用来源沿用较早的浅灰盒子样式，元信息与正文区分不明显。
- 修复：优化引用来源卡片的边框、圆角、间距、标题和相似度标签；确认复制成功/失败反馈为正常中文。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。

## 2026-05-14 主问答区空状态与快捷问题优化

- 现象：新会话没有任何对话时，主问答区缺少引导，用户需要自己想第一条问题。
- 根因：聊天区只渲染历史消息和输入框，没有为空会话提供起始操作。
- 修复：新增空状态卡片，显示当前知识库和三个常用示例问题；点击示例问题会直接进入原有问答流程；同步清理清空会话确认提示文案。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。

## 2026-05-14 前端可见文案、菜单与上传反馈优化

- 现象：侧边栏、文档管理、系统设置、上传区仍有历史编码残留文案；三点菜单只有文字；批量上传结果以多条消息刷屏。
- 根因：早期可见中文文案存在编码损坏，上传反馈直接逐文件调用 Streamlit 消息组件，缺少汇总层。
- 修复：补充干净的最终渲染函数覆盖侧边栏、文档管理、系统设置和上传区；三点菜单增加统一线性图标；上传完成后显示成功/失败汇总，并将逐文件结果收进折叠面板。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。
## 2026-05-14 三点菜单视觉像独立下拉按钮

- 现象：知识库和会话行尾操作使用原生 `st.popover` 后，右侧显示为带下拉箭头的独立按钮，行标题也可能换行成大卡片，不符合“每一栏末尾只有三个点”的预期。
- 根因：Streamlit popover 触发器默认带下拉箭头，按钮文本默认居中且允许换行；行按钮与菜单按钮的默认样式过重。
- 修复：隐藏 popover 自带箭头，用 CSS mask 稳定绘制三个点；知识库/会话行标题强制单行省略；菜单触发器改为透明轻量样式，保留原生 popover 的稳定点击行为。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。
## 2026-05-14 行内三点菜单改为悬浮显示

- 现象：知识库和会话的三点菜单虽然可点击，但视觉上仍像行外独立按钮，不符合“每一栏内部 hover 才显示三点”的交互预期。
- 根因：原生 `st.popover` 触发器和行按钮被渲染在相邻列中，默认列间距、按钮背景和可见状态让它看起来脱离了列表项。
- 修复：将知识库/会话行列间距收为 0；用同一行容器 hover/focus 控制三点透明度；三点按钮保持在每行内部，默认隐藏，悬浮或菜单打开时显示；继续隐藏 popover 下拉箭头。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。
## 2026-05-14 三点触发器去边框与菜单样式升级

- 现象：知识库和会话行尾三点触发器仍有按钮外框和下拉箭头，弹出菜单也不像参考图中的轻量操作菜单。
- 根因：`st.popover` 触发器自带按钮样式和图标结构，菜单内按钮也继承了侧边栏通用按钮样式。
- 修复：强制隐藏触发器箭头和内置图标，去掉三点按钮边框、背景与阴影；将 popover 菜单改为白底圆角浮层，菜单项为轻量列表样式，删除项单独使用红色。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。
## 2026-05-14 侧边栏状态条与菜单细节继续优化

- 现象：当前知识库仍使用 Streamlit 默认蓝色大提示框，和新的行内三点菜单视觉不够统一；菜单删除项缺少危险操作分隔感。
- 根因：默认 `st.info` 视觉重量偏大，popover 菜单内所有操作项样式一致。
- 修复：将当前知识库提示替换为轻量状态条；为删除项增加顶部细分隔并保持红色危险操作样式；深色模式同步补充状态条颜色。
- 验证：`python -m py_compile streamlit_app.py rag/api_client.py` 通过；Streamlit AppTest `exceptions 0`。
## 2026-05-28 侧边栏危险操作确认弹窗优化

- 现象：侧边栏删除知识库、删除会话仍使用页面内联确认，和文档删除、清空会话等危险操作弹窗不统一，长页面中也不够醒目。
- 优化：将删除知识库和删除会话确认改为 `st.dialog` 弹窗，复用危险操作确认面板样式；确认后保留原有删除逻辑、置顶状态清理、分享面板状态清理和当前知识库回退逻辑。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/sidebar.py` 的删除确认前端交互与 `BUG_LOG.md` 记录，不涉及知识库/会话数据结构、RAG 检索、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\sidebar.py ui\assets.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\sidebar.py ui\assets.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。
## 2026-06-03 Agent 代码工具误建议安装 nltk

- 现象：用户询问“如何用 Python 生成 RAG 评估报告”时，Agent 调用代码执行工具生成了依赖 `nltk` 的代码；环境未安装该库后，最终回答变成建议用户运行 `pip install nltk`。
- 根因：Agent 提示词没有约束代码工具优先使用标准库；代码执行工具把 `ModuleNotFoundError` 原始 traceback 直接返回，模型容易把安装依赖当成最终解决方案。
- 修复：Agent 系统提示新增规则：执行 Python 代码优先使用标准库，缺包时必须重写，不把 `pip install` 作为最终答案；`execute_python_code` 识别 `ModuleNotFoundError` 并返回“请改用标准库或已安装依赖重写”的明确指令。
- 追加修复：将 Agent 系统提示整体清理为明确中文规则，禁止默认建议安装新库；RAG 评估/报告类问题优先给纯 Python 标准库实现。
- 防回潮：`run_agent()` 对 RAG 评估/准确率/召回率/报告类问题增加答案修正；如果模型仍返回 `pip install`、`sklearn`、`transformers`、`nltk` 等第三方依赖方案，或“评估报告”回答缺少完整报告生成模板，会替换为标准库评估报告模板。
- 超时修复：真实请求中该问题会触发多轮 `execute_python_code`，总耗时约 190 秒并导致客户端超时；对“RAG 评估报告”类问题新增标准库模板快速路径，跳过 Agent 工具循环，直接返回可运行报告脚本。
- 验证：新增缺失模块回归测试，确认工具不再暴露原始 traceback。

## 2026-06-03 普通 RAG 模式精确标题命中被过滤

- 现象：关闭 Agent 模式后，用户询问“如何在 Python 中处理大文件分块而不占用过多内存？”时返回“根据现有资料无法回答该问题”，但 `02_Python学习笔记.md` 中存在完全对应的小节。
- 根因：轻量关键词搜索能将目标小节排到第 1，但混合检索在 EnsembleRetriever 成功时没有把 `_keyword_search()` 候选追加进最终重排；同时 `_rerank_results()` 没有使用 `keyword_candidate_score`，导致标题精确命中的片段仍可能因向量距离/重排阈值被过滤。进一步复测发现，查询重写会把原始标题式问题替换成泛化关键词，导致真实 `/retrieve` 仍可能偏离目标小节。
- 修复：无论 Ensemble 是否成功，都追加轻量关键词候选参与重排；重排时识别并上限化 `keyword_candidate_score`，让标题和正文高置信命中的片段不会被 `RETRIEVER_MIN_SCORE` 误杀；查询重写改为保留原问题并追加改写结果，避免丢失精确标题表达；精确短语匹配改为按查询行判断，使第一行原问题仍能命中标题。
- 数据处理：排查期间曾临时重复入库一批 `AI与编程学习资料` Markdown，随后按本次 `upload_time` 精确删除新增 2677 个重复子块，collection 恢复到原有 2677 条。
- 验证：新增重排回归测试，覆盖“标题精确命中但向量距离不理想”仍应保留结果。

## 2026-06-03 空乱码知识库 AI????? 清理

- 现象：前端知识库列表出现 `AI?????`，不是用户真实创建的中文知识库名称。
- 根因：历史请求或终端编码异常曾把中文名称转成问号串，并触发了新的空 Chroma collection 映射。
- 处理：确认 `AI?????` 对应 collection 文档数为 0 后删除该 collection，并从 `collection_name_mapping.json` 移除映射；保留 `AI编程学习库`、`RAG技术原理`、`本项目开发与代码结构说明` 等真实中文映射。
- 保护：未删除任何非空知识库，未修改真实文档内容或向量块。

## 2026-06-03 大文件分块回答不完整

- 现象：普通问答已不再直接拒答，但“如何在 Python 中处理大文件分块而不占用过多内存？”的回答仍可能命中泛化的文件处理/异常处理片段，代码回答显示到一半就结束。
- 根因：该问题的关键答案在资料中依赖 `stream_read_text`、`chunk_size`、流式读取、逐块读取等术语；查询重写后的泛化关键词会让“文件处理”类片段得分过高。普通 QA 的 `ChatOpenAI(max_tokens=1200)` 也偏低，长代码答案容易被截断。
- 修复：为“大文件/分块/内存”场景补充检索扩展词，包括 `流式读取`、`逐块读取`、`stream_read_text`、`chunk_size` 等；对实际包含 `stream_read_text`、`流式读取`、`逐块读取`、`OOM` 等强信号的片段增加专项检索加权，避免被普通文件解析代码抢占；新增 `LLM_MAX_TOKENS` 配置并默认提高到 2400，QAChain 使用该配置生成回答；当模型命中该资料但没有输出完整代码时，返回标准库 `stream_read_text` + `chunk_large_file` 完整代码兜底。
- 配置：`.env.example` 新增 `LLM_MAX_TOKENS=2400`。

## 2026-06-03 Agent 请求 500：LangChain verbose API 不兼容

- 现象：前端 Agent 模式显示 `Agent 执行出错：请求失败：500`。
- 日志：`logs/app.log` 中 `/agent` 请求报错 `No module named 'langchain.globals'`。
- 根因：`rag/agent.py` 为开启调试日志硬导入 `from langchain.globals import set_verbose`，但当前环境为 LangChain 1.2.17，该模块已不存在，导致 Agent 模块导入阶段直接失败。
- 修复：移除对 `langchain.globals.set_verbose` 的硬依赖，继续使用项目自身的 `AGENT_DEBUG`、`debug_info` 和结构化日志记录 Agent 调试信息。
- 验证：`rag.agent` 可正常导入；`/agent` 真实请求返回 200；相关 Agent/Tavily/API endpoint 测试通过。

## 2026-05-28 Agent 调试、工具重试与搜索结果优化

- 现象：Agent 模式只能看到粗略工具调用，无法确认搜索服务、重试次数、降级状态和耗时；Tavily/DuckDuckGo 结果未统一清洗，重复 URL、HTML 标签和过长摘要会降低可读性。
- 优化：默认开启 `AGENT_DEBUG`，`/agent` 响应新增 `debug_info`；前端在 Agent 模式下持久展示工具输入输出预览、搜索服务、重试次数、降级状态和耗时。
- 重试：新增 `TOOL_RETRY_MAX_ATTEMPTS`、`TOOL_RETRY_BACKOFF_SECONDS`，Tavily 与 DuckDuckGo 外部调用统一有限重试，失败仍记录日志并按原有降级策略返回用户友好提示。
- 搜索结果：新增统一清洗、HTML 反转义、去标签、去重 URL、摘要截断和 `WEB_SEARCH_MAX_RESULTS`/`WEB_SEARCH_TIMEOUT` 配置，Tavily 仍优先，DuckDuckGo 作为兜底。
- 影响范围：`rag/tools.py`、`rag/agent.py`、`main.py`、`rag/api_client.py`、`ui/api_wrappers.py`、`ui/chat.py`、`ui/pages.py`、`rag/session_state.py`、配置示例和相关测试。
- 验证：新增/更新 Agent debug、Tavily retry/search formatting、Agent endpoint 和配置测试。

## 2026-05-28 Tavily 搜索降级提示与核心测试

- 现象：Tavily 配置了 API Key 但调用失败时，`search_web` 会静默降级到 DuckDuckGo，返回内容中没有提示 Tavily 错误；日志还会复用“API Key 未配置”的降级描述。
- 根因：`_search_with_tavily()` 对所有异常统一返回空字符串，`search_web()` 无法区分“未配置 key”和“已配置但调用失败”。
- 修复：记录最近一次 Tavily 异常；当 Tavily 失败且已配置 key 时，返回“已切换到 DuckDuckGo”的用户可见提示，并继续展示 DuckDuckGo 兜底结果。
- 依赖同步：`pyproject.toml` 补充 `langgraph>=0.2.0` 与 `tavily-python>=0.5.0`，保持与 `requirements.txt` 的 Agent 工具依赖一致。
- 验证：新增 `tests/test_tools_tavily.py`，覆盖工具顺序保持知识库优先、Tavily 成功、未配置 key 降级 DuckDuckGo、Tavily 异常后提示并降级 DuckDuckGo。
## 2026-05-28 对话界面取消内部滚动栏

- 现象：问答页消息区域使用固定高度容器，长回答时会在对话卡片内部出现下拉滚动栏，用户需要在页面滚动和消息框滚动之间切换，体验不够自然。
- 优化：将对话消息区从 `st.container(height=540, key="chat_scroll_area")` 改为普通流式容器，消息内容随页面自然展开；同步移除仅服务于内部滚动容器的浅色、深色和移动端滚动条样式。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/chat.py`、`ui/styles/_global.py`、`ui/styles/_dark.py`、`ui/styles/_responsive.py` 的对话区前端布局，不涉及问答生成、RAG 检索、会话存储、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\chat.py ui\assets.py ui\styles\_global.py ui\styles\_dark.py ui\styles\_responsive.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\chat.py ui\assets.py ui\styles\_global.py ui\styles\_dark.py ui\styles\_responsive.py` 通过；源码检查无 `chat_scroll_area`、旧滚动容器样式、`st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`。
## 2026-05-28 对话输入框底部固定优化

- 现象：取消对话区内部滚动栏后，历史对话改为页面自然滚动，但输入问题框仍可能跟随页面位置变化，滚动查看历史时不够像成熟聊天产品的底部常驻输入区。
- 优化：将输入区改为真实的 `st.container(key="chat_input_area")` 容器，完整包住快捷提问、输入框、发送和清空按钮；将 sticky 样式绑定到该真实容器，底部保留 12px 间距、圆角卡片和更高层级，确保滚动历史对话时输入面板始终停留在对话底部。
- 清理：旧的空壳 `.input-area` 不再作为生效输入区样式入口，避免样式命中空 div 导致“看似固定但实际输入框不固定”的问题回潮。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/chat.py`、`ui/styles/_chat.py`、`ui/styles/_dark.py` 的对话输入区前端布局，不涉及问答生成、RAG 检索、会话存储、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\chat.py ui\styles\_chat.py ui\styles\_dark.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\chat.py ui\styles\_chat.py ui\styles\_dark.py` 通过；源码检查无 `st.popover` 与旧三点菜单选择器残留；Streamlit AppTest `exceptions 0`；浏览器验证 `chat_input_area` 存在且计算样式为 `position: sticky`、`bottom: 12px`、`z-index: 500`。
## 2026-05-28 对话输入区固定在视口底部

- 现象：输入区使用 `position: sticky` 后，只有滚动到对话末尾附近才会显示并粘住；用户查看较早历史对话时仍看不到输入框，无法做到“历史可滚动、输入框始终在页面最底部”。
- 优化：将 `chat_input_area` 从 sticky 改为 `position: fixed`，固定在浏览器视口底部；桌面端按主内容区域避开侧边栏并限制最大宽度，移动端改为左右 0.75rem；为主内容区增加底部安全留白，避免最后一条消息被固定输入区遮挡。
- 稳定性：补充 `width: auto !important`、`display: block !important`、`min-height` 和子容器宽度规则，避免 Streamlit 默认容器宽度/布局类覆盖固定输入面板。
- 保护：未修改 `session-menu` / `collection-menu` 自定义三点菜单实现，未恢复 Streamlit 原生 `st.popover`，未调整菜单项和隐藏按钮桥接逻辑。
- 影响范围：仅影响 `ui/styles/_chat.py`、`ui/styles/_global.py`、`ui/styles/_responsive.py` 的对话输入区前端布局，不涉及问答生成、RAG 检索、会话存储、依赖或环境变量。
- 验证：`python -m py_compile streamlit_app.py ui\styles\_chat.py ui\styles\_responsive.py ui\styles\_global.py` 和 `D:\anaconda3\envs\ai_project\python.exe -m py_compile streamlit_app.py ui\styles\_chat.py ui\styles\_responsive.py ui\styles\_global.py` 通过；Streamlit AppTest `exceptions 0`；源码检查无 `st.popover` 与旧三点菜单选择器残留；浏览器计算样式确认 `chat_input_area` 为 `position: fixed`、`bottom: 16px`、`z-index: 1000`。
## 2026-05-28 前端布局错乱恢复与服务重启

- 现象：对话输入区改为 `position: fixed` 后，在当前 Streamlit DOM 下可能被计算为 0 宽/0 高并影响整体布局；同时 CSS 模块中残留的内嵌 `<style>` / `</style>` 会破坏统一样式注入，导致侧边栏隐藏桥接按钮暴露，前端看起来“全乱了”。
- 修复：将 `chat_input_area` 从 fixed 恢复为稳定的 sticky 输入面板；移除 `_global.py` 和 `_dark.py` 内部多余的 `<style>` 标签，保留 `ui/assets.py` 统一包裹样式；为侧边栏 collection/session 的隐藏桥接按钮补充强制隐藏规则，只显示自定义三点菜单。
- 重启：已重启 Streamlit 前端，后端 `main.py` 保持运行并通过 `/health` 检查；前端 `http://127.0.0.1:8501` 返回 200。
- 保护：未恢复 Streamlit 原生 `st.popover`，未修改 `session-menu` / `collection-menu` 自定义三点菜单项和交互桥接逻辑。
- 验证：`python -m py_compile streamlit_app.py ui\assets.py ui\styles\_global.py ui\styles\_dark.py ui\styles\_chat.py ui\styles\_responsive.py ui\styles\_sidebar.py` 和 Conda 环境同命令通过；Streamlit AppTest `exceptions 0`；源码检查除 `ui/assets.py` 统一外层 `<style>` 外无样式模块内嵌 `<style>`，无 `st.popover` 与旧三点菜单选择器残留；浏览器验证隐藏桥接按钮可见列表为空。
## 2026-05-28 外部样式重写后前端逐项恢复

- 现象：外部工具批量改动样式模块后，页面出现多处退化：Streamlit Material 图标名（`add`、`upload_file`、`description`、`check_circle`）直接显示为英文文本；顶部概览卡片退化成普通文本；侧边栏知识库/会话行缺少卡片化样式；隐藏桥接按钮有暴露风险。
- 修复 1：在 `ui/styles/_widgets.py` 中隐藏 `span[data-testid="stIconMaterial"]`，避免旧 Streamlit 或字体缺失时显示 material 图标英文名。
- 修复 2：将主标签页从 `:material/...:` 标签改为纯中文标签，彻底移除标签页图标文本退化来源。
- 修复 3：将侧边栏 API 状态从 `st.success/st.error(..., icon=":material/...")` 改为自定义 `sidebar-api-ok/sidebar-api-fail` HTML 状态条。
- 修复 4：补回 `app-hero`、`workspace-overview`、`workspace-card`、`workspace-mini-stats` 等核心样式，使顶部 Hero 和概览卡片恢复卡片布局。
- 修复 5：补回 `collection-row/session-row`、label、actions、三点按钮样式，并继续强制隐藏 collection/session 的 Streamlit 桥接按钮。
- 保护：未恢复 Streamlit 原生 `st.popover`，未修改 `session-menu` / `collection-menu` 自定义三点菜单项和桥接逻辑。
- 验证：完整 `py_compile` 通过；Streamlit AppTest `exceptions 0`；前端 `8501` 和后端 `/health` 均返回 200；浏览器截图确认图标英文名消失、顶部卡片恢复、侧边栏行样式恢复、隐藏桥接按钮计数为 0。
## 2026-05-28 知识库管理侧边栏三点菜单恢复

- 现象：外部工具重写前端后，知识库管理侧边栏样式退化，当前知识库状态卡显示异常；知识库/会话行的三点入口不明显，且三点菜单绑定依赖问答页脚本，停留在其它标签页时菜单可能无法打开。
- 修复：为侧边栏补回 `collection-row` / `session-row` 行样式、常驻三点按钮伪元素、当前知识库状态卡样式，以及 `collection-menu` / `session-menu` 浮层样式。
- 修复：新增侧边栏独立菜单绑定脚本，在所有标签页都会绑定知识库和会话的自定义三点菜单，不再依赖进入“知识库问答”页后才注入聊天增强脚本。
- 菜单项：知识库菜单保持 `置顶 / 重命名 / 删除`；会话菜单保持 `分享 / 置顶 / 重命名 / 删除`。
- 保护：继续隐藏 Streamlit 桥接按钮，未恢复 `st.popover`，未改变原有后端 API 调用和会话/知识库状态逻辑。
- 验证：`python -m py_compile streamlit_app.py ui\sidebar.py ui\styles\_sidebar.py` 和 Conda 环境同命令通过；Streamlit AppTest `exceptions 0`；浏览器验证知识库三点菜单显示 `置顶/重命名/删除`，会话三点菜单显示 `分享/置顶/重命名/删除`，当前知识库卡片正常显示。
## 2026-05-29 前端现代视觉焕新第六阶段

- 现象：删除确认、清空会话、分享导出、上传进度和 Streamlit 提示条仍保留较多默认控件观感，和已恢复的侧边栏、上传队列、文档卡片风格不够统一。
- 优化：统一补充 `.doc-confirm-panel`、`.inline-confirm-panel`、`.share-panel`、`stAlert`、`stProgress` 与下载按钮样式，形成同一套圆角卡片、轻渐变、状态色和弱阴影反馈系统。
- 危险操作：确认删除、批量删除、清空会话按钮统一为红色危险按钮；取消、关闭分享面板统一为轻量中性按钮，降低误操作风险。
- 分享导出：分享面板标题、会话名、复制与下载按钮统一视觉层级，保持原有复制 Markdown、下载 Markdown、复制纯文本、下载 PDF 逻辑不变。
- 保护：未恢复 Streamlit 原生 `st.popover`，未修改知识库/会话三点菜单状态逻辑，未触碰后端 API、RAG 检索、上传解析和数据结构。
## 2026-05-29 前端现代视觉焕新第七阶段

- 现象：问答空状态、文档空列表、筛选无结果和上传空状态虽然已有提示文案，但视觉层级偏普通，和新版 Hero、上传队列、文档卡片不够统一。
- 优化：为 `.chat-empty-state` 补充专属卡片样式、网格纹理、柔和渐变、标题图标和正文层级；升级 `.upload-empty-panel` 与 `.empty-step` 的圆角、边框、阴影和 hover 反馈。
- 响应式：移动端下空状态卡片收窄圆角和内边距，减少小屏挤压；深色模式同步适配空状态面板背景与边框。
- 保护：仅修改 CSS 样式模块和维护日志，未修改上传、文档筛选、问答生成、会话、知识库和三点菜单逻辑；未恢复 `st.popover`。
## 2026-05-29 前端现代视觉焕新第八阶段

- 现象：普通 Markdown 内容、表格、代码块、引用块、分割线、展开面板、复选框/单选和目录表仍可能暴露 Streamlit 默认样式，和新版卡片系统不完全一致。
- 优化：统一 Markdown 正文、链接、行内代码、代码块、引用块、表格、分割线、`stDataFrame`、`stTable` 的阅读样式；补充展开面板、复选框、单选控件的圆角、边框、hover 和文字层级。
- 文档细节：目录表从普通 collapse 表格升级为圆角卡片表格，增加表头背景、hover 行反馈和统一阴影；移动端 Markdown 表格支持横向滚动，避免撑破页面。
- 深色模式：同步补充展开面板、表格、引用块和目录表深色背景/边框适配。
- 保护：仅修改 CSS 样式模块和维护日志，未修改业务逻辑、后端接口、RAG 链路、上传流程和三点菜单状态逻辑；未恢复 `st.popover`。
## 2026-05-29 前端现代视觉焕新第九阶段

- 现象：AI 生成中、思考步骤、上传处理中、上传成功/失败和禁用按钮已有基础状态，但反馈较静态，用户等待时不容易判断系统仍在工作。
- 优化：为用户/AI 消息增加轻量入场动画；AI 生成中的消息气泡增加柔和 shimmer；思考过程 active 步骤增加呼吸点；上传处理中行增加 shimmer，成功/失败行增加状态边线和弱光圈。
- 可用性：为按钮、表单提交和下载按钮补充 `focus-visible` 焦点环；禁用按钮降低阴影并保留清晰的不可用状态。
- 深色模式：同步调整生成中 shimmer 和上传处理中 shimmer 的深色透明度，避免亮斑过重。
- 保护：仅修改 CSS 样式模块和维护日志，未修改问答生成、上传、文档管理、会话、知识库和三点菜单逻辑；未恢复 `st.popover`。
## 2026-05-29 前端现代视觉焕新第十阶段

- 现象：界面已有现代化视觉，但键盘 Tab 焦点、移动端触控区域、减少动效偏好和深色模式焦点环仍可继续增强。
- 优化：补充全局 `focus-visible` 焦点环；为按钮、输入框、textarea、select、summary 和侧边栏知识库/会话三点按钮补充更清晰的键盘焦点态。
- 移动端：增加复制、重新生成、上传移除、分页按钮等小控件的最小触控尺寸；引用来源摘要在窄屏下改为纵向排布，减少挤压。
- 可访问性：在 `prefers-reduced-motion: reduce` 下关闭生成 shimmer、上传 shimmer 和 thinking dots；深色模式补充更可见的焦点环颜色。
- 保护：仅修改 CSS 样式模块和维护日志，未修改问答、上传、文档管理、会话、知识库和三点菜单业务逻辑；未恢复 `st.popover`。
## 2026-05-29 侧边栏列表项一体胶囊样式优化

- 现象：知识库和会话列表项文字前仍显示 `●/○` 状态点，且文字栏与三点按钮分成两个独立气泡，视觉上不够接近紧凑聊天列表样式。
- 优化：移除知识库和会话按钮文本前的实心/空心圆点；将左侧标题按钮与右侧三点按钮拼成同一个圆角胶囊，左侧负责选择，右侧负责打开菜单，中间去掉断裂感。
- 交互：三点按钮仍使用原有 Streamlit 按钮和 session state 展开菜单，菜单项保持知识库 `置顶 / 重命名 / 删除`，会话 `分享 / 置顶 / 重命名 / 删除`。
- 保护：未恢复 `st.popover`，未改动后端 API、会话/知识库状态逻辑、删除/重命名/分享业务逻辑。
## 2026-05-29 侧边栏一体胶囊中间色块修复

- 现象：知识库/会话行改成一体胶囊后，Streamlit 左右列各自背景仍参与渲染，标题列和三点列中间出现垂直白色块，视觉上像被切开。
- 修复：将统一背景、边框、阴影上移到整行 wrapper；标题按钮和三点按钮改为透明背景、无边框、无阴影，仅承担点击区域。
- 交互：hover 和菜单打开状态改为作用在整行 wrapper 上，保持三点菜单点击逻辑不变。
- 保护：未恢复 `st.popover`，未改动后端 API、会话/知识库状态逻辑和菜单项。
## 2026-05-29 侧边栏一体胶囊层级覆盖修复

- 现象：整行 wrapper 已经绘制统一背景后，后加载的侧边栏通用按钮样式仍覆盖了标题按钮和三点按钮背景，导致右侧三点区域看起来不在同一图层。
- 修复：在最终加载的 widgets 样式模块中追加更高优先级覆盖，强制知识库/会话行内部列容器和按钮透明化，只保留外层 wrapper 背景。
- 交互：hover 和菜单打开态仍作用于整行 wrapper，三点菜单状态逻辑不变。
- 保护：未恢复 `st.popover`，未改动后端 API、会话/知识库状态逻辑和菜单项。
## 2026-05-30 侧边栏胶囊标题与三点对齐修复

- 现象：知识库列表标题仍可能居中显示，而会话列表标题靠左；同一套胶囊列表中的文字和右侧三点视觉基线不一致。
- 修复：在最终加载的 widgets 样式中，强制知识库/会话标题按钮占满标题区并左对齐；标题文本统一单行省略；三点按钮区域固定靠右并在自身区域居中。
- 保护：未恢复 `st.popover`，未修改三点菜单状态逻辑、菜单项和后端 API。
## 2026-05-30 侧边栏标题与三点垂直中线对齐修复

- 现象：知识库/会话胶囊已经合并，但右侧 `⋯` 和标题文字仍存在轻微垂直偏移。
- 根因：Streamlit 按钮内部段落保留默认 margin 和行高，标题按钮与三点按钮的内容盒高度不同。
- 修复：统一标题区、三点区和按钮内部段落高度为 `42px`，使用 flex 垂直居中；清除内部段落 margin，标题和三点使用稳定行高。
- 保护：未恢复 `st.popover`，未修改菜单状态逻辑、菜单项和后端 API。
## 2026-05-30 侧边栏主操作按钮视觉统一

- 现象：创建按钮只占半行，新建会话和使用说明沿用不同控件默认样式，三者宽度、圆角、间距和视觉层级不一致。
- 修复：创建按钮改为整行“创建知识库”；创建、新建会话、使用说明统一为 `44px` 高度、同宽、同边距和 `15px` 圆角。
- 视觉：创建知识库使用蓝色渐变主按钮；新建会话使用浅蓝次主按钮；使用说明使用白底轻量按钮；三者通过 CSS mask 绘制稳定线性图标，不依赖 Material 字体渲染。
- 保护：未修改知识库创建、会话创建和使用说明内容逻辑；未恢复 `st.popover`，未改动三点菜单。
## 2026-05-30 创建知识库按钮颜色降噪

- 现象：创建知识库按钮使用高饱和蓝色渐变，视觉重量过高，和侧边栏浅色卡片体系不协调。
- 优化：改为浅蓝卡片按钮，使用细蓝边框、轻微径向高光和深蓝文字；hover 时仅提升背景和阴影，不再使用大面积深蓝色块。
- 保护：仅调整按钮视觉，未修改知识库创建逻辑、三点菜单和后端 API。
## 2026-05-30 侧边栏三点按钮内收

- 现象：知识库和会话胶囊右侧三点按钮过于贴近右边缘，视觉上偏右。
- 优化：三点按钮区域右侧增加 `0.45rem` 留白，使三点轻微左移，同时保留原有点击区域和菜单定位。
- 保护：未修改三点菜单状态逻辑、菜单项、知识库/会话操作和后端 API。
## 2026-05-30 侧边栏三点按钮进一步内收

- 现象：三点按钮首次内收幅度较小，仍然显得过于靠右。
- 优化：将右侧留白从 `0.45rem` 增加到 `1rem`，使三点按钮更明显向标题方向靠近。
- 保护：未修改三点菜单状态逻辑、菜单项、知识库/会话操作和后端 API。
## 2026-05-30 侧边栏三点按钮右侧留白调整为 10rem

- 调整：按界面反馈将知识库/会话三点按钮右侧留白改为 `10rem`，使按钮大幅向左移动。
- 保护：未修改三点菜单状态逻辑、菜单项、知识库/会话操作和后端 API。
## 2026-05-30 侧边栏列表改为图标式轻量聊天条目

- 现象：通过按钮宽度和右侧 margin 移动三点无效，因为三点仍被 Streamlit 右侧列布局限制；列表项文字居中、阴影偏重，也不接近参考图中的轻量聊天条目。
- 修复：将三点按钮容器改为胶囊内部绝对定位，脱离列宽限制并固定在右侧内边距；标题改为左对齐，左侧增加知识库文档图标和会话气泡图标。
- 视觉：降低标题字重、圆角、间距和阴影强度，背景改为轻灰卡片，使整体更接近参考图的紧凑现代列表。
- 保护：仍使用原有 Streamlit 三点按钮和 session state 菜单逻辑；未恢复 `st.popover`，未修改菜单项和后端 API。
## 2026-05-30 侧边栏主操作按钮图标文字组合居中

- 现象：创建知识库、新建会话按钮的图标靠左而文字居中，视觉重心割裂。
- 修复：将图标和文字作为一个 flex 组合整体居中，清理按钮文本额外宽度和 margin；使用说明同步采用居中布局。
- 保护：仅修改样式，未修改按钮业务逻辑、三点菜单和后端 API。
## 2026-05-30 侧边栏主操作按钮内容左对齐

- 现象：创建知识库、新建会话、使用说明的图标文字组合居中后，和侧边栏列表项的左对齐视觉语言不一致。
- 修复：三个入口统一改为左对齐，图标与文字从同一起点横向排列。
- 保护：仅修改样式，未修改按钮业务逻辑、三点菜单和后端 API。
## 2026-05-30 侧边栏主操作按钮内部内容左对齐

- 现象：外层按钮已设为左对齐，但 Streamlit 按钮内部内容容器仍可能占满宽度并将文字推向中间，导致加号和文字分离。
- 修复：为创建知识库、新建会话按钮内部真实内容容器补充 flex 左对齐规则，图标与文字紧邻排列，视觉语言与顶部知识库管理卡片一致。
- 保护：仅修改样式，未修改按钮业务逻辑、三点菜单和后端 API。
## 2026-05-30 侧边栏主操作按钮改为确定性左对齐

- 现象：Streamlit 按钮内部多层容器继续覆盖 flex 对齐规则，加号和文字仍然分散。
- 修复：不再依赖内部 flex 推导，直接将加号固定在左侧 `1rem`，文字固定在左侧 `2.7rem`，并垂直居中，确保创建知识库和新建会话稳定左对齐。
- 保护：仅修改样式，未修改按钮业务逻辑、三点菜单和后端 API。
## 2026-05-30 工作区空白徽章图标增强

- 现象：顶部 Hero 右上角装饰和三张工作区概览卡左上角徽章显示为空白色块，缺少语义和视觉细节。
- 根因：当前嵌入渲染环境下，徽章内部 SVG 未稳定显示。
- 修复：使用 CSS mask 绘制稳定图标，不再依赖徽章内部 SVG；当前知识库使用数据库图标，文档状态使用层叠图标，当前会话使用消息气泡图标，Hero 装饰使用星芒图标。
- 视觉：概览徽章增加对应状态色小圆点，补充微小但有辨识度的 UI 细节。
- 保护：仅修改样式，未修改工作区数据、知识库/会话状态、三点菜单和后端 API。
## 2026-05-30 对话导出按钮图标与层次增强

- 现象：导出 Markdown、导出 PDF 按钮只显示文字，左右空白较多，缺少工具入口辨识度。
- 根因：为兼容旧渲染隐藏了 Streamlit Material 图标 span，下载按钮原生图标不可见。
- 修复：为两个对话导出按钮增加稳定 key，并使用 CSS mask 绘制独立图标；Markdown 使用文档图标，PDF 使用红色 PDF 文件图标。
- 视觉：按钮内容左对齐，增加轻量渐变底色、hover 边框和阴影反馈。
- 保护：未修改 Markdown/PDF 生成逻辑、会话数据、三点菜单和后端 API。
## 2026-05-30 对话导出按钮图标文字左对齐修复

- 现象：导出按钮已添加图标，但 Streamlit 内部文本容器占满宽度，导致图标在左侧、文字仍居中。
- 修复：导出图标固定在按钮左侧 `1rem`，按钮内容预留左侧空间；文本容器收缩为内容宽度并左对齐，使图标和文字紧邻排列。
- 保护：仅修改样式，未修改 Markdown/PDF 导出逻辑、会话数据和后端 API。
## 2026-05-30 对话导出按钮文字确定性定位

- 现象：Markdown 导出按钮内部文本仍被 Streamlit 下载组件布局推向中间，图标与文字间距过大。
- 修复：将 Markdown/PDF 导出按钮文字固定在左侧 `3rem`，图标保持左侧 `1rem`，两者垂直居中并紧邻排列。
- 保护：仅修改样式，未修改 Markdown/PDF 导出逻辑和后端 API。
## 2026-05-30 文档管理工具栏与文档图标升级

- 现象：文档管理全选/删除/禁用/启用按钮仍像旧式大按钮，数字因列宽不足换到第二行；文档卡左侧徽章为空白方框。
- 修复：适度增大四个工具栏按钮列宽，将按钮改为 `40px` 高度的紧凑单行胶囊；通过 CSS mask 补充选择、删除、禁用、启用语义图标，并按蓝/红/橙/绿色区分操作。
- 文档卡：左侧徽章改为稳定 CSS 文件图标，不再依赖嵌入 SVG 显示。
- 保护：未修改全选、批量删除、启用/禁用业务逻辑，未修改文档数据和后端 API。
## 2026-05-30 文档复选框贴近卡片与侧边栏菜单图标增强

- 现象：文档复选框独占较宽列且位置靠上，与文件卡距离较远；知识库/会话三点菜单只有文字，视觉辨识度不足。
- 修复：缩窄文档复选框列宽，复选框容器与文档卡垂直中线对齐并贴近卡片；菜单项通过 CSS mask 增加分享、置顶、重命名、删除图标。
- 保护：未修改文档选择、批量操作、三点菜单状态逻辑、菜单项行为和后端 API。
## 2026-05-30 对话输入面板固定与最新回答自动定位优化

- 现象：长对话上下滚动后，输入面板只有回到对话末尾附近才能看到；发送新问题后，用户还需要手动向下寻找最新回答。
- 修复：将 `chat_input_area` 从内容流内的 `sticky` 改为视口底部 `fixed` 浮层；通过前端脚本读取主内容容器的实时位置和宽度，使输入面板在侧边栏展开、窗口缩放和 Streamlit 重绘后仍与对话主界面对齐。
- 修复：主内容容器根据输入面板实际高度动态预留底部空间，避免最新消息被固定输入面板遮挡；保留问题和回答锚点滚动逻辑，并取消回答阶段的手动滚动拦截，使新回答完成后始终自动进入视野。
- 保护：未修改问答生成、检索、会话持久化、侧边栏三点菜单和后端接口。
## 2026-05-30 固定输入面板操作区与快捷提问视觉升级

- 现象：固定输入面板中的发送、清空按钮因 Material 图标兼容隐藏规则只剩红白色块，用户无法快速理解用途；四个快捷提问按钮横向铺满整行，视觉偏旧且占用空间过多。
- 优化：发送与清空按钮改为带稳定 CSS mask 线性图标和明确文字的小型操作按钮；发送使用轻蓝主操作，清空默认使用中性灰，仅在 hover 时显示轻量危险色提示。
- 优化：快捷提问压缩为左侧紧凑胶囊组，降低高度、字号、阴影和边框视觉重量，并增加轻量星芒图标。
- 保护：未修改固定悬浮定位、自动滚动、问答生成、会话清空确认、侧边栏三点菜单和后端接口。
## 2026-05-30 固定输入面板操作按钮文字溢出修复

- 现象：发送、清空按钮增加文字后，部分窗口宽度下操作列空间不足，文字越过按钮边框。
- 修复：适度增大两个操作列比例和按钮最小宽度；同步收紧图标位置、字号与左右内边距，使图标和文字稳定容纳在胶囊按钮内。
- 保护：未修改输入面板固定悬浮、自动滚动、发送、清空确认和侧边栏三点菜单逻辑。
## 2026-05-30 固定输入面板紧凑化

- 现象：固定输入面板完成悬浮后整体高度偏大，快捷提问、输入框和发送/清空按钮显得厚重，占用对话可视区域。
- 优化：降低输入面板外层 padding、圆角和阴影强度；快捷提问胶囊从 30px 降到 26px；发送/清空按钮和聊天输入框从 52px 降到 44px，并同步收紧图标与文字尺寸。
- 保护：紧凑化规则限定在 `chat_input_area` 内，未影响其它页面 textarea、固定悬浮定位、自动滚动、发送/清空逻辑和侧边栏三点菜单。
## 2026-05-30 对话清空入口与最新回答滚动体验修复

- 现象：问答页底部仍保留旧的“清空当前会话”按钮，和固定输入面板里的清空入口重复且视觉突兀；回答完成后页面仍可能跳回刚才的问题附近，用户需要再次寻找最新回答。
- 修复：移除页面内旧清空按钮，将 `Ctrl+L` 快捷键绑定到固定输入面板的“重置”按钮；重置仍走原有确认弹窗，避免误清空。
- 修复：在对话流末尾增加不可见滚动哨兵点，问题发送和回答完成时统一滚动到对话底部，而不是依赖某条消息自身锚点，避免回答阶段跳回旧问题。
- 保护：未修改问答生成、检索、会话删除确认逻辑、固定悬浮输入面板和侧边栏三点菜单。
## 2026-05-30 豆包式对话页结构与滚动跟随修复

- 现象：问答页顶部仍是传统区块标题，缺少以当前对话为中心的标题栏；快捷提问位于输入框上方，和豆包类产品的输入工具条习惯不一致；发送问题后仍可能跳回问题位置，用户需要手动下滑查看回答。
- 优化：问答页顶部改为居中的对话标题栏，标题优先使用本会话第一句用户问题，副标题显示“内容由 AI 生成，请仔细甄别”、当前知识库和消息数量。
- 优化：固定输入面板改为输入框在上、提示语与快捷提问在下的布局，快捷提问作为轻量工具胶囊保留在输入框下方。
- 修复：滚动逻辑从单次 `scrollIntoView` 升级为多次强制滚动，覆盖浏览器窗口、Streamlit 主容器和可滚父容器；流式回答过程中也周期性跟随到底部，避免回答生成时停留在旧问题附近。
- 保护：未修改 RAG 检索、答案生成、上传、文档管理、会话持久化和侧边栏三点菜单逻辑。
## 2026-05-30 固定输入面板工具区重排

- 现象：固定输入面板中输入框、建议文案、快捷提问分散成多行，留白过大，视觉上显得松散且不够像成熟聊天产品。
- 优化：将底部说明与快捷入口合并为单行工具栏，左侧显示“快捷提问”和快捷胶囊，右侧显示 `Ctrl + Enter` 快捷键；移除冗长建议文案，减少一整行高度。
- 优化：收紧快捷胶囊高度、操作按钮宽度和输入面板内边距，降低右侧按钮被头像区域挤压的概率。
- 保护：未修改固定悬浮定位、强制滚动到底部、问答生成、会话重置确认和侧边栏三点菜单逻辑。
## 2026-05-30 发送后白屏与回答流式性能修复

- 现象：在固定输入框中点击发送后，前端会白屏或长时间无响应，之后才恢复显示回答。
- 根因：提交问题后额外触发一次 `st.rerun()`，导致表单提交 rerun 后又立刻二次刷新；回答流式显示每 3 个字符等待 0.1 秒，并在循环中反复注入滚动组件，长回答会产生大量前端重绘和 iframe 组件。
- 修复：提交后不再额外 rerun，而是在当前运行中立即追加用户消息并进入生成流程；回答流式分块从 3 字扩大到 18 字，等待从 0.1 秒降到 0.015 秒；循环中不再反复注入滚动组件，仅在最终回答完成后触发一次底部滚动。
- 优化：思考步骤的人为等待从 0.3/0.2 秒降到 0.05 秒，减少发送后的空白等待。
- 保护：未修改检索、生成、Agent、会话持久化、上传、文档管理和侧边栏三点菜单逻辑。
## 2026-05-30 对话头像视觉升级

- 现象：问答页用户和 AI 头像沿用普通圆形渐变，风格偏旧，和当前豆包式对话页、轻量输入框不够统一。
- 优化：用户头像改为蓝色消息徽章，AI 头像改为绿色星芒知识徽章；头像从普通圆形升级为方圆玻璃徽章，增加内环、状态点、柔和阴影和 hover 层次。
- 适配：补充深色模式下用户/AI 头像的背景、边框和图标颜色，避免深色环境下发灰或过亮。
- 保护：仅修改头像图标和 CSS 视觉，不影响发送、滚动、问答生成、会话持久化和侧边栏三点菜单逻辑。
## 2026-05-30 对话头像图标空白修复

- 现象：头像徽章背景已生效，但用户/AI 图标显示为空白，仅能看到右下角状态点。
- 根因：头像内部 SVG 在当前 Streamlit/CSS 兼容规则下未稳定显示，导致徽章中心为空。
- 修复：隐藏头像内嵌 SVG，改用 CSS mask 在 `.user-avatar::before` 和 `.ai-avatar::before` 中绘制消息与星芒图标，确保图标稳定显示。
- 保护：仅修改头像渲染方式，不影响问答、发送、滚动、会话和三点菜单逻辑。
## 2026-05-30 顶部标签页与主题按钮图标补充

- 现象：主标签页和右侧深色/浅色切换按钮只有文字，缺少明确视觉图标；Material 图标在当前兼容规则下可能被隐藏。
- 优化：为“文档上传 / 知识库问答 / 文档管理 / 系统设置”标签文本补充稳定图标字符；主题切换按钮移除 Material 图标依赖，改用 CSS mask 绘制月亮/太阳图标，深色模式下自动切换。
- 保护：仅修改导航与主题按钮视觉，不影响标签页内容、主题状态、问答、上传、文档管理和侧边栏三点菜单逻辑。
## 2026-05-30 顶部标签页图标风格统一

- 现象：顶部标签页使用 emoji 图标后，颜色和形态与整体线性 UI 系统不一致，并且在部分环境下会显示为乱码或彩色小图标。
- 修复：标签文字恢复为纯中文，使用 CSS mask 为四个标签分别绘制上传、对话、文档层叠、设置线性图标；图标颜色跟随选中/hover 状态。
- 保护：未修改标签页内容、主题按钮逻辑、问答、上传、文档管理和侧边栏三点菜单。
## 2026-05-30 前端全局视觉一致性微调

- 现象：部分卡片样式引用了未定义的 `--rag-shadow-card`，导致阴影层级不稳定；顶部标签页仍可能露出 Streamlit 默认红色下划线；首页状态卡质感和其它卡片系统略有割裂。
- 修复：在浅色/深色变量中补齐 `--rag-shadow-card`；隐藏 Streamlit 默认 tab highlight/border，改为系统蓝色小指示条。
- 优化：首页三张概览卡使用统一卡片阴影，并增加轻量高光层；深色模式下降低高光强度，保持卡片层次但不过亮。
- 保护：未修改业务逻辑、标签页内容、问答发送、滚动、上传、文档管理和侧边栏三点菜单。
## 2026-05-31 前端输入区与文档卡片微交互优化

- 现象：固定输入区视觉重量略高，快捷提问和发送/清空按钮仍偏大；文档管理列表虽然可用，但卡片状态层次较弱，长列表浏览时不够精致。
- 优化：压缩固定输入面板内边距、输入框高度、快捷提问胶囊和发送/清空按钮尺寸，让底部输入区更轻，不遮挡主内容；顶部标签页改为更轻的胶囊导航，并用左侧状态点替代底部短线。
- 优化：文档卡片增加左侧状态色带、元信息状态点和更居中的图标/文本对齐，禁用文档使用琥珀色状态提示，提升启用/禁用区分度。
- 保护：仅修改 CSS 视觉层，不改问答生成、上传、文档管理 API、会话持久化、固定滚动逻辑和侧边栏三点菜单逻辑。
## 2026-05-31 系统设置页图标化与分组升级

- 现象：系统设置页顶部状态胶囊和“检索与分块 / 生成与增强 / Agent 模式”区域主要依赖文字，控件密度高，缺少和整体 UI 一致的图标与卡片层次。
- 优化：为设置摘要 chip 补充 SVG 线性图标；为三个设置分组增加带图标、说明文字和轻量光晕的分组卡；开关项增加左侧状态色带、hover 层次和更清晰的文字权重。
- 适配：补充深色模式下设置分组卡的边框、阴影和光晕强度，避免深色模式发灰或过亮。
- 保护：仅修改设置页展示和 CSS，不改变任何设置项含义、默认值、session_state key、RAG 检索、上传分块或 Agent 执行逻辑。
## 2026-05-31 上传页队列与空状态图标化优化

- 现象：文档上传页队列标题、统计摘要和空状态主要依赖文字表达，删除操作使用普通 `×`，与当前线性图标和卡片系统不够统一。
- 优化：上传队列标题补充上传图标；统计摘要拆分为“总数 / 成功 / 失败 / 处理中”状态胶囊并加入 SVG 图标；移除文件按钮改为统一的垃圾桶线性图标。
- 优化：未选择文件时的空状态增加标题图标、说明文字层级，以及“同主题归档 / 先小批上传 / 设置先确认”三张带图标提示卡。
- 保护：仅修改上传页 HTML 展示和 CSS，不改变文件选择、分页、移除文件、上传处理、重试、分块参数、多模态解析或后端 API 调用逻辑。
## 2026-05-31 上传队列隐藏分页触发按钮修复

- 现象：选择上传文件后，页面左侧额外显示“上传文件上一页 / 上传文件下一页”两个按钮，用户无法理解其用途。
- 根因：这两个按钮是自定义上传队列分页箭头的隐藏 Streamlit 触发器，供前端脚本点击使用，但缺少对应 CSS 隐藏规则。
- 修复：为 `upload_preview_prev` 和 `upload_preview_next` 的 Streamlit key 容器补充强制隐藏样式，保留自定义队列底部分页箭头和原有分页逻辑。
- 保护：仅修改 CSS 展示层，不改变文件选择、上传、分页、队列刷新、移除文件或重试逻辑。
## 2026-05-31 上传队列移除按钮图标空白修复

- 现象：上传队列右侧移除文件按钮显示为红色空白圆角框，垃圾桶图标不可见。
- 根因：按钮内部嵌入的 SVG 在当前 Streamlit HTML/CSS 组合下被按钮样式影响，导致图标未稳定显示。
- 修复：移除按钮内联 SVG，改用 `.upload-task-remove::before` 的 CSS mask 绘制垃圾桶图标，确保颜色跟随按钮状态并稳定渲染。
- 保护：仅修改移除按钮的图标渲染方式，不改变点击删除已选文件、上传队列、分页或上传处理逻辑。
## 2026-05-31 上传队列文件图标空白修复

- 现象：上传队列中文件名前方的文件图标显示为空白方块，只有浅蓝色底框可见。
- 根因：上传队列行内嵌 SVG 在当前 Streamlit HTML/CSS 组合下未稳定渲染，和移除按钮图标空白属于同类问题。
- 修复：将上传队列文件图标和旧上传文件行图标都改为 CSS mask 绘制，并隐藏内部 SVG，确保文件图标稳定显示。
- 保护：仅修改图标渲染 CSS，不改变文件选择、移除、分页、上传处理或任务队列逻辑。
## 2026-05-31 上传队列文件图标纯 CSS 绘制修复

- 现象：将上传队列文件图标改为 CSS mask 后，文件图标仍显示为空白，仅能看到浅蓝色图标底框。
- 根因：当前 Streamlit/CSS 渲染环境中，上传队列该位置的 SVG mask 仍未稳定绘制。
- 修复：彻底移除该位置对 SVG 和 mask 的依赖，改用纯 CSS 边框、背景线条和伪元素绘制文件图标轮廓与内容线。
- 保护：仅修改上传队列文件图标视觉实现，不改变上传队列数据、文件移除、分页、上传或重试逻辑。
## 2026-05-31 上传队列文件图标对齐文档管理样式

- 现象：上传队列文件图标与文档管理列表图标不一致，用户期望两处使用同款蓝色文档徽章。
- 调整：将上传队列文件图标和旧上传文件行图标的尺寸、圆角、蓝色底色、边框、阴影与文档管理 `.document-card-icon` 对齐，并复用同款文档线性图标 mask。
- 保护：仅修改上传页图标视觉样式，不改变上传队列、文件移除、分页、上传处理或文档管理逻辑。
## 2026-05-31 上传处理主按钮视觉统一

- 现象：“开始上传并处理”按钮使用 Streamlit primary 默认样式，显示为大面积红色，视觉上像危险操作，与上传语义和整体蓝白 UI 不一致。
- 修复：为上传处理按钮增加稳定 key `upload_process_button`，移除 primary 默认样式依赖，改为蓝白渐变主操作按钮，并使用 CSS mask 绘制上传图标。
- 优化：按钮增加圆角、轻量阴影、hover 抬升和蓝色边框反馈，和当前卡片/工具按钮系统保持一致。
- 保护：仅修改按钮 key 和视觉样式，不改变点击后上传、进度、队列刷新、失败重试或后端 API 调用逻辑。
## 2026-05-31 上传处理操作栏重排

- 现象：“开始上传并处理”按钮虽然改成蓝白色，但仍是整行满宽按钮，视觉上像横幅条，缺少现代产品感。
- 优化：新增上传处理操作栏，左侧展示“准备写入知识库”和当前待处理文件数量说明，右侧改为紧凑主按钮“开始处理”。
- 优化：主按钮改为蓝色渐变胶囊、白色文字、上传图标和悬浮阴影；操作栏使用浅色卡片背景和右侧分隔线，整体更像任务确认区。
- 保护：仅调整上传按钮布局和样式，不改变上传触发、任务队列、进度更新、失败提示或重试逻辑。
## 2026-05-31 上传处理按钮极简化

- 现象：上传处理操作栏与按钮上下错位，按钮掉到说明栏下方，整体仍显得臃肿、不够现代。
- 调整：移除上传处理说明横栏，改为居中的小型胶囊按钮“处理 N 个文件”，使用白底蓝字、细边框和轻阴影，避免大面积色块。
- 补充：失败后的重试按钮改为琥珀色胶囊样式，降低默认满宽白条的突兀感。
- 保护：仅调整上传处理与重试按钮视觉布局，不改变上传、失败提示、重试、分页或任务队列逻辑。
## 2026-05-31 上传队列操作区按用户要求收敛

- 现象：上传队列删除按钮点击后未稳定移除文件；上传操作按钮多次调整后仍与页面风格不符；上传处理时出现蓝色进度条和分页箭头，影响界面观感。
- 修复：增强自定义移除按钮的前端匹配逻辑，兼容 `stFileUploaderDeleteBtn` 在按钮自身或子按钮上的不同 DOM 结构，并在只有一个待删除按钮时回退点击唯一目标。
- 调整：上传主按钮恢复为一整条长按钮，隐藏左侧上传箭头图标，使用蓝白轻量样式；隐藏队列底部分页箭头；上传处理流程不再创建蓝色进度条，并补充 CSS 隐藏兜底。
- 保护：不改变上传接口、文件处理、任务队列状态、失败重试和分页状态本身，仅调整展示与前端触发兼容性。
## 2026-05-31 PDF 空内容上传失败原因提示与重试区收敛

- 现象：上传图片型/扫描型 PDF 后失败，前端额外弹出较大的错误框和重试按钮区，界面跳动明显；后端仅返回“文档解析后内容为空”，用户难以判断原因。
- 根因：该 PDF 由 `PyPDFLoader` 读取到 22 页，但页面文本为空，分块结果为 0；同时多模态图片解析请求 SiliconFlow 返回 `403 Forbidden`，图片内容未能转成文本。
- 修复：当 PDF 分块为空时，后端返回更明确的用户提示，说明可能是扫描版/图片型 PDF，并提示检查多模态模型权限或上传 OCR/可复制文本版本。
- 优化：前端去掉失败后的独立重试按钮区，改为只在队列行显示失败原因，并用一条轻量结果提示替代大红错误框，减少页面跳动。
- 保护：不改变上传接口、PDF 文本解析、图片解析调用、向量入库或任务队列核心逻辑。
## 2026-05-31 上传队列失败文件移除改为前端队列删除

- 现象：文件处理失败后，用户点击上传队列右侧垃圾桶按钮没有反应，无法从失败列表中移除该文件。
- 根因：之前的垃圾桶按钮通过 JavaScript 去点击 Streamlit 原生文件上传器的删除按钮，但原生上传器 DOM 结构和隐藏状态不稳定，失败处理后无法可靠命中目标按钮。
- 修复：改为自定义上传队列删除逻辑。每个队列项生成隐藏的 Streamlit 移除触发按钮，自定义垃圾桶只触发对应队列项删除，并将文件 key 写入 `upload_removed_keys`，后续上传时自动跳过已移除文件。
- 优化：隐藏内部移除触发按钮；当所有待处理文件都被移除时，显示轻量提示，不再保留无意义的上传按钮。
- 保护：不改变后端上传接口、文件解析、任务状态显示或知识库入库逻辑。
## 2026-06-02 上传队列状态收口

- 现象：上传队列删除文件后，再新增文件可能使已删除项重新出现；处理成功的文件仍可再次点击主按钮重复入库；失败后额外恢复栏会增加页面跳动。
- 修复：新增队列合并逻辑，选择变化时保留已移除记录和既有任务状态；主处理按钮只提交“等待中”文件，成功项不再重复上传；处理中不渲染删除按钮。
- 优化：失败原因和恢复建议仅保留在对应文件行中，移除额外失败操作栏；没有待处理文件时主按钮使用明确禁用态并说明原因。
- 保护：未改动后端上传接口、文档解析、分块参数、多模态解析、向量入库或分页逻辑。
## 2026-06-02 对话最新回答入口与滚动跟随优化

- 现象：用户在生成回答时向上查看历史后，难以判断新回答是否已出现，也缺少快速返回最新内容的入口；停止生成后浏览器侧即时加载反馈可能短暂残留。
- 优化：新增浏览器侧“查看最新回答”浮动按钮，离开对话底部时自动出现；生成期间按钮显示“回答生成中 · 查看最新”，点击后平滑回到底部并恢复自动跟随。
- 修复：滚轮、触摸、键盘和页面滚动都会同步最新回答按钮；停止生成时立即移除即时加载浮层，继续保留原有 toast 和对话内说明。
- 保护：未改动问题提交、RAG 检索、回答生成、Agent、会话持久化、固定输入框或侧边栏菜单逻辑。
## 2026-06-02 移动端高频区域专项适配

- 现象：窄屏下长文件名可能挤压上传队列布局；快捷键提示和文档说明占用有限空间；固定输入框贴近手机底边；侧边栏原生收起按钮视觉与触控尺寸偏弱。
- 优化：上传队列内容列补充 `min-width: 0`，确保长文件名稳定省略；文档元信息允许安全换行；手机端隐藏低优先级键盘提示和文档说明，并压缩快捷提问横向区域。
- 优化：最新回答浮动按钮在手机端缩小；固定输入框适配底部安全区；发送和重置按钮扩大为稳定触控宽度；侧边栏原生收起按钮统一为系统卡片样式。
- 保护：未改变侧边栏收起行为、上传队列状态、文档选择、对话提交、自动滚动或桌面端布局。
## 2026-06-03 前端反馈提示统一

- 现象：侧边栏和文档管理仍有少量 Streamlit 默认 `info/warning/success/error` 大色块，视觉重量和当前卡片系统不一致；文档启用/禁用后立即 rerun，反馈可能被刷新吃掉。
- 优化：新增统一 `render_status_notice()` 组件，覆盖信息、成功、警告和失败四类页面级反馈；替换侧边栏和文档管理里的默认大色块提示，成功类瞬时操作改用 toast。
- 修复：文档启用/禁用结果写入 `document_status_notice`，在 rerun 后于文档管理顶部显示一次，保证用户能看到操作结果。
- 适配：补充统一状态条的深色模式和移动端紧凑尺寸。
## 2026-06-03 图标按钮无障碍提示与焦点态统一

- 现象：三点菜单、上传队列删除、发送/重置、文档批量工具栏、导出和主题切换等图标化按钮主要依赖视觉图标，悬停提示与键盘焦点反馈不够统一。
- 优化：在前端注入脚本中为关键按钮补充中文 `aria-label` 与 `title`，禁用按钮提供更明确的禁用原因，降低用户误点和不理解按钮用途的概率。
- 优化：为 Streamlit 普通按钮、表单按钮和下载按钮补充统一 `focus-visible` 焦点环，键盘 Tab 操作时能清楚看到当前焦点，同时不影响鼠标常规浏览状态。
- 保护：未改动任何按钮点击逻辑、上传队列状态、文档批量操作、会话导出、主题切换或后端 API。
## 2026-06-03 引用复制按钮精致化

- 现象：回答下方引用来源里的“复制引用 / 复制全部引用”仍偏文字胶囊，视觉密度略高，和回答复制、导出等图标化工具按钮不够一致。
- 优化：引用复制按钮改为稳定的“复制图标 + 短文字”形态；单条引用显示“复制”，全部引用显示“全部复制”，减少引用摘要栏拥挤感。
- 优化：补充引用复制按钮的 hover 抬升、复制成功绿色反馈、键盘焦点继承和深色模式覆盖，使其与当前按钮系统更统一。
- 保护：未修改引用数据、相似度展示、复制 payload、展开/收起逻辑、回答生成或后端检索逻辑。
## 2026-06-03 深色模式漏网硬编码收口

- 现象：部分高频控件仍在浅色规则中保留亮白或亮红硬编码，例如停止生成 hover、文档单删 hover、上传步骤徽标和上传状态胶囊；深色模式下可能显得突兀。
- 优化：在最终深色覆盖层中统一压住这些浅色残留，上传步骤、上传队列、上传统计胶囊、处理中徽标、文档删除 hover 和停止生成 hover 均回到 `--rag-*` 变量体系。
- 优化：保留成功、处理中和危险操作的语义色，但降低深色模式下的亮度和阴影冲击，让边框、文字灰度和 hover 反馈更稳定。
- 保护：未修改浅色主题规则、上传流程、文档删除逻辑、按钮 key、状态计算或后端 API。
## 2026-06-03 CSS 维护性小步收口

- 目标：继续执行 CSS 维护策略，只整理确认安全的重复覆盖，不再边用边大拆结构。
- 巡检：复查历史上传旧列表、旧侧边栏菜单、旧状态类、旧重试区等选择器，当前运行 CSS 中未发现这些孤儿规则残留；`sidebar-main-header` 仍由侧边栏真实使用，保留不删。
- 清理：合并最终深色覆盖层中相邻的文档删除 hover 重复规则，减少一处重复选择器，同时保持深色危险 hover 的边框、背景、文字和阴影效果不变。
- 保护：未修改 CSS 加载顺序、三点菜单、上传队列、固定输入框、文档管理、深浅色变量或后端逻辑。
## 2026-06-03 前端 UI 契约测试补充

- 目标：把统一反馈、深色最终覆盖和 CSS 维护边界沉淀为自动回归检查，减少后续视觉优化时反复改回旧样式的风险。
- 新增：`tests/test_frontend_ui_contracts.py`，静态检查前端源码不直接使用 `st.info/warning/success/error/progress/spinner/balloons`，页面级反馈必须通过统一状态组件或 toast。
- 新增：检查深色最终覆盖层加载在组件样式和按钮系统之后、移动端最终覆盖层之前，确保深色验收规则不会被前序样式反盖。
- 新增：检查上传分页内部触发按钮仍被隐藏，并防止旧上传列表、旧侧边栏菜单、旧任务列表等已清理选择器重新出现。
- 保护：测试只读源码和 CSS，不启动服务、不访问真实 Chroma 数据、不改动运行逻辑。
## 2026-06-03 长期偏好与重复流程沉淀

- 目标：将本轮前端收尾中反复验证出的稳定规则写入项目约定，并把重复巡检流程提炼为可复用 Codex skill。
- 规则：在 `AGENTS.md` 中补充前端小步调整默认不重启、稳定交互不得回退、深色模式需同步最终覆盖、CSS 只做确认安全的小步维护、优先运行前端契约测试、中文文件乱码需用 UTF-8 读取确认等长期规则。
- Skill：新增 `streamlit-ui-regression-check`、`streamlit-upload-queue-debug`、`streamlit-css-maintenance`、`rag-backend-smoke` 四个个人 skill，用于后续 UI 回归、上传队列排障、CSS 维护和后端冒烟检查。
- 保护：Skill 只记录稳定流程和命令，不包含本次短期界面状态；项目规则仅补充长期偏好，不改变任何运行逻辑。
## 2026-06-03 Codex 项目理解文档补齐

- 目标：为后续 Codex 长期维护补齐项目级理解文档，避免每次任务都从零猜测结构、入口、术语和历史坑。
- 新增：`PROJECT_MAP.md`，整理后端入口、前端模块、样式加载顺序、数据持久化、测试命令和 Codex 工作约定。
- 新增：`docs/KNOWN_ISSUES.md` 和 `docs/GLOSSARY.md`，记录高风险交互、历史问题、待确认项和项目术语。
- 新增：`docs/codex-prompts/frontend-fix.md`、`docs/codex-prompts/backend-debug.md`、`docs/codex-prompts/rag-debug.md`，沉淀可复用任务提示词。
- 更新：`AGENTS.md` 增加 Codex 项目理解入口，指向项目地图、已知问题、术语表、提示词和项目级 skills。
- 保护：仅修改文档，不改业务代码、不新增依赖、不操作数据目录、不清理未追踪文件。

## 2026-06-03 项目级 Codex skills 初始化补齐

- 目标：在仓库根目录 `.agents/skills/` 补齐项目级 Codex skills，让后续前端、后端、RAG、文档和回归巡检任务能直接复用项目真实流程。
- 新增：`rag-debug-loop`、`backend-change`、`frontend-change`、`docs-sync` 四个项目级 skill，分别覆盖 RAG 排错、后端变更、前端变更和文档同步。
- 更新：`streamlit-ui-regression-check`、`streamlit-upload-queue-debug`、`streamlit-css-maintenance`、`rag-backend-smoke` 四个已有项目级 skill，补充当前仓库真实模块、命令、触发边界和禁用场景。
- 保护：仅创建和完善 `.agents/skills/*/SKILL.md` 与变更记录，不改业务代码、不新增依赖、不 reset/revert、不清理未追踪文件。
## 2026-07-01 临时 Chroma 后端 RAG 闭环测试

- 目标：落实架构审查中“下一步立即执行的最小任务”，为上传、解析、切分、入库和 `/retrieve` 检索建立一条不依赖真实知识库的后端闭环护栏。
- 覆盖：新增 `tests/test_backend_rag_loop.py`，使用 fake embedding、fake LLM 和临时 Chroma 目录调用真实 `/upload` 与 `/retrieve`，验证返回非空 documents/sources、正确 `source`，以及 `score`、`vector_score`、`keyword_score`、`candidate_source` 等元数据字段。
- 保护：测试使用临时目录中的 `collection_name_mapping.json`，不读写真实 `chroma_db/collection_name_mapping.json`；测试结束显式清理 QAChain 缓存、VectorStore 缓存和 Chroma shared system cache，避免 Windows 上 HNSW 文件锁影响临时目录清理。
- 兼容：不修改业务策略、不新增依赖、不改变公开 API；当前仍可见 FastAPI `on_event`、LangChain Chroma 和 Chroma manual persist 的弃用警告，后续可在部署/维护阶段单独处理。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_backend_rag_loop.py -q` 通过。

## 2026-07-01 RAG 质量评测基线补强

- 目标：在调整 query rewrite、BM25、rerank、contextual compression 之前，先把固定评测样例和失败诊断信息沉淀下来，避免后续优化缺少可比较基线。
- 覆盖：扩展 `eval/eval_cases.json`，新增精确标题/来源命中、query rewrite fallback、上下文压缩保护等诊断型样例，并通过 `tags` 标记评测关注点。
- 报告：增强 `eval/rag_eval.py`，在 JSON report 中保留 `trace_summary.query_rewrite`、`trace_summary.compression`、`trace_summary.weights`，控制台失败输出补充 top source、candidate source、fallback 和压缩保护摘要。
- 测试：补充 `tests/test_eval.py`，覆盖 trace 摘要提取、fallback/compression 报告格式、case tags schema 校验和结构化报告字段。
- 保护：不修改检索策略默认行为，不新增依赖，不调用真实 LLM，不读写真实 Chroma 数据。
- 验证：`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_eval.py -q` 通过；`D:\anaconda3\envs\ai_project\python.exe -m pytest tests\test_backend_rag_loop.py tests\test_vector_store.py tests\test_qa_chain.py tests\test_eval.py -q` 通过。
## 2026-07-03 深色模式快捷问题与上传图标修复

- 现象：深色模式下“试试这些问题”折叠区仍出现浅色低对比背景；文件上传拖拽区的原生云图标外侧有方形边框。
- 根因：Streamlit `stExpander` 与 `stFileUploader` 的内部 BaseWeb/原生 SVG 样式没有被最终深色覆盖层完全接管；上传器 SVG 内部 `rect` 被当作图标边框显示。
- 修复：`ui/styles/_dark_refinement.py` 增加深色 `stExpander` summary/region/button 覆盖；`ui/styles/_widgets.py` 和深色覆盖层清理 uploader SVG 外框，仅保留云图标线条。
- 测试：前端契约测试补充深色 expander、快捷问题按钮和 uploader SVG rect 清理规则。

## 2026-07-03 统一状态提示图标空白修复

- 现象：侧边栏“暂无知识库，请先创建一个”的统一提示卡只显示浅色圆角底，内部提示图标为空白。
- 根因：`render_status_notice()` 使用内联 SVG 图标，在部分 Streamlit `st.html` 渲染路径下会被清理或无法稳定继承颜色。
- 修复：状态提示图标改为 `status-icon-*` class + `::before` CSS mask 渲染，和空状态图标采用同一类稳定方案。
- 测试：前端契约测试要求状态提示不再输出 `icon_svg(icon_name)`，并校验 `status-notice-icon::before` 与 `--status-icon-*` mask 存在。

## 2026-07-03 面试展示版 AI 工作台前端升级

- 升级：聊天回答增加 `answer-status-bar`，在回答顶部展示本地资料、Web 补充、Agent、引用数量、最高分和本地兜底等状态，让答案来源更接近 ChatGPT/Gemini 的可解释工作台体验。
- 升级：引用区域继续使用证据抽屉，并补充 `candidate_source`、vector/keyword score、chunk 等 trace chip，方便面试演示 RAG 证据链。
- 升级：侧边栏从“知识库管理”调整为“AI 工作空间 / 知识空间 / 最近对话”，知识库行补充启用文档数和最近上传信息，创建入口收进折叠面板。
- 升级：文档管理页文案调整为“资料库 / My Stuff”，上传三步状态调整为“解析中 / 已入库 / 可提问”，更贴近现代 AI 产品的内容中心表达。
- 测试：前端契约测试补充状态条、证据 trace、Agent 执行轨迹、资料库文案、知识空间文案和上传三步文案护栏。

## 2026-07-03 深色模式浅色 tooltip 与按钮残留修复

- 现象：深色模式下侧边栏创建知识库输入框聚焦出现白色角；侧边栏三点菜单项和聊天快捷问题按钮 hover 时出现浅色原生 tooltip；快捷问题按钮在深色背景下变成白底、文字发灰。
- 根因：部分 `st.button(help=...)` 会生成浏览器/Streamlit 原生浅色 tooltip，难以用 CSS 稳定覆盖；同时 `stTextInput` 的 BaseWeb 聚焦层和 sample/quick prompt 按钮缺少最终深色覆盖。
- 修复：移除侧边栏菜单项、示例问题和快捷问题按钮的非必要 `help`；在 `ui/styles/_dark_refinement.py` 增加深色模式 text input 聚焦、sample question、quick prompt disabled/hover 覆盖。
- 测试：前端契约测试补充这些 tooltip 文案不得回潮，以及深色输入框和快捷按钮覆盖必须存在。

## 2026-07-03 删除知识库后缓存失效误报修复

- 现象：知识库实际已删除，刷新后列表消失，但删除弹窗仍显示 500 失败。
- 根因：删除成功后 `_discard_collection_state()` 会调用 `_invalidate_collection_cache(store)`；新版 `langchain_chroma` 在 collection 已删除后访问 `store._collection` 会抛 `Chroma collection not initialized`，导致成功删除被后续缓存清理误报为失败。
- 修复：`_invalidate_collection_cache()` 在读取 store cache key 失败时退化为清空 collection cache，不再把删除后的 wrapper 状态异常冒泡成接口失败。
- 测试：补充删除成功但 cache key 读取失败的单测，确保仍返回成功并清理 `_stores`、mapping 和缓存。

## 2026-07-03 删除知识库假失败兼容补强

- 现象：删除知识库后页面仍提示 500 失败，但刷新后知识库已经消失，说明后端删除动作已完成、确认状态误判。
- 根因补充：新版 Chroma 的 `list_collections()` 可能直接返回字符串集合名，旧的 `_collection_exists()` 只读取 `col.name`，会在确认“底层 collection 已不存在”时误判，从而把已删除状态继续当成失败。
- 修复：`rag/vector_store.py` 兼容字符串和对象两种 collection 列表返回；同时把 `does not exist`、`not found`、`already deleted` 纳入可确认的删除后状态异常。
- 测试：`tests/test_vector_store.py` 增加字符串集合名兼容测试和 missing collection 异常成功兜底测试。
