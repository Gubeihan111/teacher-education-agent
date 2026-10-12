# 教师教育智能体七人团队完整开发手册

## 1. 文档目的

本手册用于指导七名开发人员在同一个 GitHub 仓库中并行开发四条 LangGraph 工作流、工具及前端。目标是明确每个人负责什么、可以修改哪些目录、如何使用 Codex 或 Claude Code、如何提交 Pull Request，以及负责人如何验收和合并。

团队采用以下结构：

```text
项目负责人
├── 成员1：WF1 会学习工作流负责人
├── 成员2：WF2 会设计工作流负责人
├── 成员3：WF3 会实施与判断工作流负责人
├── 成员4：WF4 会反思与迁移工作流负责人
├── 成员5：分析、检测与评价工具负责人
├── 成员6：生成、推荐与服务工具负责人
└── 成员7：前端网页与交互负责人
```

四名工作流负责人只维护工作流节点、State、路由和本工作流 Manifest。两名工具负责人维护四条工作流使用的 122 个工具。公共注册、共享契约和部署文件由项目负责人指定一人统一修改。

## 2. 架构协作原则

### 2.1 工作流与工具分离

工作流负责人决定：

- 当前执行哪个节点；
- 节点需要哪些输入；
- 调用哪个工具；
- 工具结果写入哪些 State 字段；
- 满足什么条件后进入哪个节点；
- 何时暂停、恢复、失败或结束。

工具负责人决定：

- 工具接受什么参数；
- 如何校验参数；
- 使用确定性算法还是模型服务；
- 返回什么结构化结果；
- 外部服务不可用时如何降级；
- 如何记录候选证据、错误和告警。

工具不能自行决定工作流路由，工作流也不能复制工具内部算法。

### 2.2 模型决策边界

大模型可以：

- 生成候选目标、问题、内容、策略和反馈；
- 给出冲突分类、专业判断或阶段评价候选；
- 组织证据和生成解释；
- 推荐资源和支架。

大模型不能直接决定：

- 用户权限；
- 数据库事务是否提交；
- 正式 Rubric 分数；
- CCI 最终计算值；
- 工作流强制路由；
- 取消、失败、过期和完成终态；
- 是否执行需要授权的课堂控制命令。

### 2.3 数据边界

- LangGraph State 只保存当前执行所需的小型状态和引用。
- 大型文档、音视频、完整转写和模型制品保存在外部存储中。
- Checkpointer 保存工作流执行位置。
- PostgreSQL 业务表保存任务、证据、评价和成长画像。
- 四条工作流通过 `contracts/` 中的稳定契约交换数据。

## 3. 开发目录说明

### 3.1 仓库顶层

```text
teacher-education-agent/
├── apps/                         # API、前端和异步任务入口
├── configs/                      # 环境配置和功能开关
├── contracts/                    # API、事件、工具及跨工作流契约
├── data/                         # 示例、种子和开发数据
├── deploy/                       # Docker、FunASR、Kubernetes、Nginx
├── docs/                         # 架构、业务、迁移和协作文档
├── knowledge_base/               # 课程标准、案例、Rubric 等知识
├── migrations/                   # Alembic 数据库迁移
├── model_artifacts/              # 模型制品清单
├── observability/                # 日志、指标、告警和仪表盘
├── prompts/                      # 版本化提示词
├── scripts/                      # 映射、知识、数据库和部署脚本
├── src/teacher_education_agent/  # 核心 Python 源码
├── tests/                        # 各级测试目录
├── AGENTS.md                     # Codex 和开发人员工程约束
├── compose.yml                   # 本地服务编排
└── pyproject.toml                # Python 工程配置
```

### 3.2 核心源码

```text
src/teacher_education_agent/
├── agents/            # 智能体角色和注册
├── application/       # 应用用例、命令、查询和 DTO
├── core/              # 配置、安全、权限、日志和事务
├── domains/           # 教师教育领域模型
├── infrastructure/    # 数据库、Checkpointer、缓存和队列
├── integrations/      # 外部系统适配
├── knowledge/         # 知识解析、切分、索引和检索
├── model_services/    # LLM、嵌入、语音和视觉模型网关
├── orchestration/     # 四阶段培养链编排
├── tools/             # 122 个工作流工具
└── workflows/         # 145 个 LangGraph 节点及路由
```

### 3.3 单条工作流目录

```text
wf*_*/
├── graph.py            # 创建和编译 LangGraph
├── state.py            # 工作流 State
├── routes.py           # 确定性条件路由
├── policies.py         # 次数、权限和业务限制
├── contracts.py        # 本工作流输入输出契约
├── nodes/              # 节点处理函数
├── subgraphs/          # 阶段子图
├── schemas/            # 结构化输入输出模型
├── prompts/            # 本工作流提示词
└── specification.md    # 业务和技术规格
```

### 3.4 工具目录目标结构

当前工具主要集中在各自的 `catalog.py`。为避免成员5和成员6同时修改同一个文件，后续应拆为：

```text
wf*_*/
├── analysis_tools.py   # 成员5负责
├── action_tools.py     # 成员6负责
├── catalog.py          # 只负责合并和注册
└── __init__.py
```

拆分完成前，两名工具负责人不能同时修改同一个 `catalog.py`；应按工作流顺序错峰提交，或者由其中一人先完成结构拆分并合并。

## 4. 七人详细分工

## 4.1 成员1：WF1会学习工作流负责人

建议分支：`feat/wf1-workflow`

允许修改：

```text
src/teacher_education_agent/workflows/wf1_cr_sdl_v3/
src/teacher_education_agent/workflows/workflow_manifests/wf1_manifest.py
docs/workflow-node-tool-route-mapping.md 中的 WF1 部分
```

具体任务：

1. 维护 WF1 的 52 个原图节点。
2. 维护初始化、学习定向、目标设定、问题规划、探究、认知冲突调节、验证和反思阶段。
3. 确保每个原图节点对应独立 LangGraph 节点。
4. 为每个节点明确输入字段、输出字段和工具调用。
5. 维护认知冲突不足、适宜和过载三类分支。
6. 维护退回目标、退回问题、补充证据和重新验证路由。
7. 为循环设置访问次数上限。
8. 对教师或学习者确认步骤使用中断和恢复。
9. 检查 WF1 使用的 16 个工具是否存在并完成注册。
10. 同步更新节点—工具—输入输出—路由对照表。

交付内容：

- WF1 Manifest；
- WF1 State；
- WF1 节点和路由；
- WF1 工具输入输出映射；
- WF1 对照表；
- 语法、导入、节点注册和路由一致性检查结果。

## 4.2 成员2：WF2会设计工作流负责人

建议分支：`feat/wf2-workflow`

允许修改：

```text
src/teacher_education_agent/workflows/wf2_instructional_design_v1/
src/teacher_education_agent/workflows/workflow_manifests/wf2_manifest.py
docs/workflow-node-tool-route-mapping.md 中的 WF2 部分
```

具体任务：

1. 维护 18 个原图节点和 4 个补充节点。
2. 维护教学需求和学习者分析。
3. 维护教学目标、内容、策略、方法、媒体、练习和评价设计。
4. 维护教学过程设计和整体一致性检查。
5. 一致性不通过时进入限定次数的修订循环。
6. 需要设计者选择或确认时使用人工中断。
7. 维护取消、过期、失败和完成终态。
8. 检查 WF2 的 17 个工具与 State 字段是否一致。
9. 更新 WF2 对照表。

交付内容与成员1相同，但范围限定为 WF2。

## 4.3 成员3：WF3会实施与判断工作流负责人

建议分支：`feat/wf3-workflow`

允许修改：

```text
src/teacher_education_agent/workflows/wf3_teaching_implementation_judgment_v1/
src/teacher_education_agent/workflows/workflow_manifests/wf3_manifest.py
docs/workflow-node-tool-route-mapping.md 中的 WF3 部分
```

具体任务：

1. 维护 24 个原图节点和 5 个补充节点。
2. 维护实践任务、教学方案、虚拟学生和课堂事件配置。
3. 维护教师语言与行为、虚拟学生反应和课堂时间线。
4. 维护提问、等待、追问、反馈和参与度特征处理。
5. 维护课堂事件检测、学习状态判断和预警。
6. 维护支架推荐、人工授权和执行控制。
7. 维护观察量规、专业判断证据和证据回放。
8. 维护前后比较、再教学和稳定性判断。
9. 为再教学和重试设置上限。
10. 检查 WF3 的 43 个工具与路由条件。

交付内容与成员1相同，但范围限定为 WF3。

## 4.4 成员4：WF4会反思与迁移工作流负责人

建议分支：`feat/wf4-workflow`

允许修改：

```text
src/teacher_education_agent/workflows/wf4_reflection_transfer_v1/
src/teacher_education_agent/workflows/workflow_manifests/wf4_manifest.py
docs/workflow-node-tool-route-mapping.md 中的 WF4 部分
```

具体任务：

1. 维护 36 个原图节点和 6 个补充节点。
2. 维护反思任务和多来源证据读取。
3. 维护问题候选、反思维度和问题优先级。
4. 维护归因解释、替代解释和因果主张检查。
5. 维护策略候选、对齐、风险、计划和人工选择。
6. 维护实践验证、前后证据比较和验证重试。
7. 维护迁移任务、迁移条件、迁移表现和迁移支架。
8. 维护教学研究问题、研究计划、证据和结论循环。
9. 维护阶段成果、成长证据和正式评价请求。
10. 检查 WF4 的 46 个工具及跨工作流输出契约。

交付内容与成员1相同，但范围限定为 WF4。

## 4.5 成员5：分析、检测与评价工具负责人

建议分支：`feat/analysis-tools`

主要负责确定性分析、检测、分类、计算、比较、评价和验证。合计负责 58 个工具。

### WF1：8个

`readiness_assessor`、`goal_level_assessor`、`question_assessor`、`conflict_detector`、`conflict_classifier`、`cci_calculator`、`source_verifier`、`rubric_evaluator`

### WF2：8个

`needs_analysis`、`learning_data_analysis`、`learner_diagnosis`、`goal_validator`、`review_summarizer`、`automatic_evaluator`、`design_effect_analyzer`、`alignment_validator`

### WF3：19个

`scenario_complexity_calculator`、`teacher_action_recognizer`、`question_feature_extractor`、`wait_time_calculator`、`follow_up_feature_extractor`、`feedback_feature_extractor`、`participation_feature_extractor`、`classroom_event_detector`、`retry_counter`、`phase_classifier`、`rubric_evidence_mapper`、`interaction_quality_analyzer`、`student_state_estimator`、`event_trigger_evaluator`、`judgment_evidence_validator`、`control_command_validator`、`pre_post_comparator`、`key_timeline_extractor`、`observation_evidence_validator`

### WF4：23个

`reflection_evidence_organizer`、`problem_candidate_detector`、`reflection_dimension_classifier`、`evidence_consistency_checker`、`problem_priority_ranker`、`explanation_structure_analyzer`、`evidence_chain_validator`、`causal_claim_checker`、`strategy_alignment_checker`、`strategy_risk_checker`、`validation_indicator_builder`、`pre_post_evidence_comparator`、`validation_conclusion_builder`、`validation_retry_counter`、`transfer_condition_checker`、`transfer_performance_analyzer`、`inquiry_conclusion_checker`、`reflection_structure_assessor`、`solo_level_candidate`、`reflection_coverage_checker`、`strategy_effect_summarizer`、`stage_achievement_candidate`、`inquiry_evidence_organizer`

每个工具必须：

- 使用明确的结构化输入；
- 对必填字段和数据类型进行校验；
- 可确定计算的结果不调用大模型；
- 返回 `candidate_only` 或明确的确定性结果标记；
- 不写入正式评价分数；
- 不决定工作流路由；
- 声明权限、超时、重试次数和确定性属性；
- 产生错误时由注册中心归一化处理。

## 4.6 成员6：生成、推荐与服务工具负责人

建议分支：`feat/service-tools`

主要负责模型生成、推荐、检索、读取、存储、外部服务和业务产物构建。合计负责 64 个工具。

### WF1：8个

`learning_context`、`resource_recommender`、`learning_feedback`、`evidence_store`、`strategy_repository`、`learner_profile_repository`、`checkpoint_store`、`audit_outbox`

### WF2：9个

`material_search`、`goal_generator`、`knowledge_retrieval`、`knowledge_organization`、`content_generator`、`strategy_recommender`、`media_recommender`、`exercise_generator`、`personalized_assignment_recommender`

### WF3：24个

`growth_profile_reader`、`practice_history_reader`、`scaffold_history_reader`、`evidence_persistence`、`task_config_reader`、`plan_config_reader`、`student_config_reader`、`event_config_reader`、`speech_recognizer`、`virtual_student_responder`、`classroom_state_updater`、`timeline_recorder`、`training_state_reader`、`judgment_candidate_generator`、`scaffold_recommender`、`execution_controller`、`evidence_replay_reader`、`observation_rubric_reader`、`scaffold_message_generator`、`practice_outcome_builder`、`growth_evidence_builder`、`audit_event_writer`、`checkpoint_writer`、`link_outcome_builder`

### WF4：23个

`reflection_context_reader`、`practice_evidence_reader`、`growth_history_reader`、`evaluation_result_reader`、`scaffold_history_reader`、`attribution_candidate_generator`、`alternative_explanation_generator`、`strategy_candidate_generator`、`strategy_plan_builder`、`strategy_selection_recorder`、`practice_execution_facade`、`transfer_task_generator`、`transfer_evidence_collector`、`transfer_scaffold_recommender`、`inquiry_question_generator`、`inquiry_plan_builder`、`inquiry_cycle_recorder`、`growth_evidence_builder`、`profile_update_candidate`、`audit_event_writer`、`checkpoint_writer`、`human_review_packet_builder`、`formal_evaluation_request_builder`

每个工具必须：

- 通过模型网关调用模型，不在工具内直接创建厂商客户端；
- 外部服务通过 `ToolContext.services` 或明确的 Port 调用；
- 服务不可用时返回 `DEGRADED`，不能伪造成功；
- 生成内容标记为候选结果；
- 返回引用，不在 State 中保存大型正文或二进制内容；
- 不直接提交数据库事务；
- 需要人工确认的结果设置 `requires_review`；
- 写入证据时保留来源、归属和审计信息。

## 4.7 成员7：前端网页与交互负责人

建议分支：`feat/web-workbench`。允许修改 `apps/web/` 与相关前端文档。后端路由、共享契约、模型网关、数据库和部署文件由对应维护者修改。

前端当前沿用原项目的原生 HTML/CSS/JavaScript 方式，不增加打包依赖。应用入口是 `apps/web/index.html`，前端路由为 hash 路由；FastAPI 在 `/` 提供入口，在 `/web` 提供静态资源，API保持 `/api/v1`。

| 文件/目录 | 成员7的职责 |
| --- | --- |
| `src/app/main.js` | 页面导航、表单提交、任务编号保存、结果和人工确认展示 |
| `src/features/workflows.js` | 四条工作流表单定义和输入映射，与工作流负责人核对 |
| `src/services/api.js` | 统一HTTP请求、错误处理、超时；写请求不得自动重试 |
| `src/styles/main.css` | 公共配色、布局、移动端适配与焦点样式 |
| `src/utils/escape-html.js` | 来自旧前端的文本转义工具，保护动态HTML输出 |
| `public/assets/mascots/` | 迁移的吉祥物资源 |
| `pages/`、`components/`、`hooks/`、`stores/`、`types/` | 保留的后续拆分目录，目前未宣称已全部实现 |

具体交付：

1. 首页与四阶段入口，当前任务可查询。
2. 四条工作流的表单字段、必填提示和后端错误展示。
3. 启动后保存任务编号，网络异常后可以查询，不自动重复启动。
4. 人工中断时展示后端请求并用同一线程提交意见。
5. 工具降级、候选证据和正式评价在页面上有明确区分。
6. 支持文档入库，后续按新增接口接入语音和课堂时间线。
7. 综合评价和画像接口缺失时展示真实空状态，不编造分数或趋势。
8. JavaScript、CSS和模块引用使用一致缓存版本。

Codex / Claude Code任务模板：

```text
你负责教师教育智能体的前端。先读取根目录AGENTS.md、apps/web/README.md和本手册第4.7节。
本次任务：【指定一个页面或一项交互】。
允许修改apps/web/，禁止直接修改后端、模型、数据库和LangGraph路由。
阅读对应工作流State和API请求响应，核对字段，不自行猜测接口。
复用现有配色、服务层和转义工具，保持移动端布局、表单标签与键盘可用性。
只展示真实后端数据；接口缺失时给出空状态及待补接口清单。
不在前端保存模型密钥，不决定正式评分、权限或业务路由。
保留原thread_id恢复任务；网络失败不得自动重复提交写请求。
修改资源后更新缓存版本。只做语法、路径和代码静态检查，不启动业务服务或测试。
完成后列出改动、对应API、检查结果和仍需后端支持的部分。
```

成员7不承担正式评价算法或课堂控制权限判断。项目负责人另行指定API维护者，避免前端对接责任被误解为可以随意修改后端契约。

## 5. 工作流负责人向工具负责人提需求

工作流负责人不能只说“需要一个分析工具”，应使用以下格式：

```markdown
## 工具名称
wf3.classroom_event_detector

## 调用节点
WF3-N12 课堂事件检测

## 输入
- transcript_ref: string
- timeline_ref: string
- configured_event_types: list[string]

## 输出
- triggered: boolean
- event_type: string | null
- confidence: number
- evidence_refs: list[string]
- candidate_only: true

## 失败处理
- 输入缺失：VALIDATION_ERROR
- 外部服务不可用：DEGRADED
- 无事件：正常返回 triggered=false

## 路由使用
工作流根据 triggered 和 confidence 进行确定性路由，工具本身不返回下一个节点名称。
```

工具负责人完成后，应向工作流负责人提供：

- 实际工具名称；
- 输入输出模型；
- 成功、降级和失败示例；
- 是否调用外部服务；
- 是否需要人工复核；
- 工具注册位置。

## 6. Git分支和提交规范

### 6.1 第一次克隆

```powershell
git clone https://github.com/Gubeihan111/teacher-education-agent.git
cd teacher-education-agent
git status
```

### 6.2 每次开始工作

```powershell
git switch main
git pull --ff-only origin main
git switch -c feat/wf1-workflow
```

每项任务使用独立分支。分支完成并合并后，新任务重新从最新 `main` 建分支。

### 6.3 提交格式

```text
feat(wf1): implement goal-setting routes
feat(wf3): add classroom event nodes
feat(tools): implement deterministic validators
fix(wf4): bound validation retry loop
docs: update workflow mapping
refactor(tools): split workflow tool catalogs
```

### 6.4 推送并创建PR

```powershell
git status
git diff
git add .
git commit -m "feat(wf1): implement goal-setting routes"
git push -u origin feat/wf1-workflow
```

PR 必须以 `main` 为目标分支，不允许直接推送 `main`。

## 7. 使用Codex开发

### 7.1 打开方式

在 Codex 桌面应用中打开本地仓库目录，或在仓库根目录运行：

```powershell
codex
```

Codex 会读取根目录及相关子目录中的 `AGENTS.md`。开发人员仍应在任务中明确允许修改和禁止修改的范围。

### 7.2 工作流开发提示词

```text
你负责教师教育智能体项目的【WF编号和名称】。

先读取并遵守：
1. 根目录 AGENTS.md
2. docs/workflow-node-tool-route-mapping.md 中本工作流部分
3. 本工作流 specification.md
4. 本工作流 manifest、state、graph、routes、policies
5. 本任务涉及的工具定义

本次任务：
【填写原图节点编号和业务目标】

允许修改：
【填写本人负责的工作流目录和manifest】

禁止修改：
- 其他工作流
- tools目录
- workflows/detailed.py
- workflows/workflow_manifests/shared.py
- pyproject.toml
- compose.yml

实现要求：
- 原图节点必须保持为独立LangGraph节点
- 明确节点输入、输出、工具和条件路由
- State只保存必要数据和引用
- 模型不能决定权限、事务、正式评分和终态
- 循环必须设置次数上限
- 人工确认必须支持interrupt和相同thread_id恢复
- 不运行模型、数据库、Docker、语音或业务测试
- 只检查语法、导入、节点注册、工具名称和路由一致性

完成后报告：
1. 修改文件
2. 原图节点到代码节点的映射
3. 使用工具及输入输出
4. 条件路由
5. 静态检查结果
6. 遗留问题
```

### 7.3 工具开发提示词

```text
你负责教师教育智能体项目的【分析工具/服务工具】。

先读取并遵守：
1. 根目录 AGENTS.md
2. tools/contracts.py
3. tools/registry.py
4. tools/foundation.py
5. 对应工作流的节点对照表
6. 对应工具目录现有实现

本次只实现：
【逐项填写工具名称】

允许修改：
【analysis_tools.py或action_tools.py】

禁止修改：
- workflows目录
- 另一名工具负责人的文件
- 公共契约和注册器
- API、部署和依赖文件

实现要求：
- 每个工具有ToolSpec
- 输入校验明确
- 输出为结构化Mapping
- 声明permission、timeout_seconds、max_retries、deterministic
- 外部服务不可用时返回DEGRADED
- 候选结果标记candidate_only
- 不决定路由、权限、事务、正式评分和终态
- 不运行外部服务和业务测试
- 只做语法、导入、名称唯一性和注册一致性检查

完成后报告每个工具的输入、输出、异常、降级和注册位置。
```

### 7.4 代码审查提示词

```text
请审查当前分支相对main的修改，不新增功能。

检查：
1. 是否超出授权目录
2. 是否违反AGENTS.md
3. Python语法和导入
4. 工具名称是否存在且唯一
5. 节点、路由和终态是否完整
6. 循环是否有上限
7. 模型是否越过权限、事务、正式评分或终态边界
8. State是否保存了不应保存的大对象
9. 是否包含密钥、.env或大型文件

不要运行模型、数据库、Docker、语音识别或业务测试。发现问题直接修复并汇报。
```

## 8. 使用Claude Code开发

如果“CC”指 Claude Code，可在 WSL 或 Git for Windows 环境使用。进入仓库后运行：

```powershell
claude doctor
claude
```

Claude Code 不应被假设自动遵守本项目的 `AGENTS.md`，所以每次任务开头明确写：

```text
请先读取并遵守仓库根目录AGENTS.md。只修改任务明确授权的目录。
```

之后使用与 Codex 相同的工作流提示词或工具提示词。

不要让 Codex 和 Claude Code 同时修改同一个分支。同一成员需要并行时，使用两个独立分支，并保证文件范围不重叠：

```text
feat/wf1-goal-codex
feat/wf1-conflict-claude
```

## 9. Pull Request模板

```markdown
## 任务范围

- 负责人：
- 工作流或工具：
- 原图节点编号：

## 修改内容

- 

## 节点或工具映射

| 原图节点/工具 | 代码位置 | 输入 | 输出 | 路由或调用方 |
| --- | --- | --- | --- | --- |
| | | | | |

## 边界检查

- [ ] 未修改其他成员负责的目录
- [ ] 未提交.env、密钥或大型文件
- [ ] 模型未决定权限、事务、正式评分或终态
- [ ] 循环有明确次数上限
- [ ] 外部服务失败有降级或失败状态

## 静态检查

- [ ] Python语法检查
- [ ] 导入关系检查
- [ ] 节点和工具注册检查
- [ ] 路由与终态一致性检查
- [ ] git diff检查

## 未完成事项

- 
```

## 10. 负责人审查清单

### 工作流PR

- 是否对应原图节点编号；
- 是否真的注册为独立 LangGraph 节点；
- 输入输出是否与 State 一致；
- 工具名称是否存在；
- 路由是否确定且有限；
- 是否存在无限循环；
- 中断后是否使用同一 `thread_id` 恢复；
- 终态是否完整；
- 是否修改了其他工作流；
- 是否同步更新对照表。

### 工具PR

- 工具名称是否唯一；
- 输入输出是否结构化；
- 权限、超时和重试是否配置；
- 确定性工具是否错误调用模型；
- 模型输出是否标记候选；
- 外部服务不可用时是否返回真实状态；
- 是否保留证据来源和归属；
- 是否越过工作流路由和事务边界；
- 是否修改另一名工具负责人的文件。

## 11. 推荐合并顺序

每一轮按以下顺序合并：

1. 工具目录结构拆分 PR；
2. 成员5分析工具 PR；
3. 成员6服务工具 PR；
4. 四名工作流负责人同步最新 `main`；
5. WF1 工作流 PR；
6. WF2 工作流 PR；
7. WF3 工作流 PR；
8. WF4 工作流 PR；
9. 项目负责人统一更新公共注册、API和跨工作流契约。
10. 成员7基于已合并的API契约提交前端PR；纯样式和布局可独立交付。

如果四条工作流没有修改公共文件，它们可以并行审查；一旦修改 `shared.py`、`detailed.py`、`bootstrap.py`、`registry.py`、`pyproject.toml` 或 `compose.yml`，必须由负责人统一处理。

## 12. 完成标准

一项开发任务只有同时满足以下条件才算完成：

1. 代码位于正确目录；
2. 未超出分工范围；
3. 节点或工具名称与对照表一致；
4. 输入输出结构明确；
5. 条件路由和循环边界明确；
6. 错误、超时和降级状态明确；
7. 未提交凭据或大型文件；
8. 完成要求的静态检查；
9. 已提交 Pull Request；
10. 已解决负责人提出的审查意见；
11. 使用 Squash merge 合并；
12. 合并后删除功能分支并同步本地 `main`。

## 13. 同类架构的智能体与框架案例

本节回答“哪些智能体采用类似设计”。对照的是公开实现中的架构模式，不代表全部技术栈、目录布局和业务规则完全一致。核对日期：2026-10-11。

### 13.1 Open Deep Research：具体开源智能体

Open Deep Research 是 LangChain 发布的开源深度研究智能体，使用 LangGraph 运行，可以配置模型供应商、搜索工具及 MCP 服务。它为搜索摘要、研究、结果压缩和最终报告设置不同模型职责。[项目源码与说明](https://github.com/langchain-ai/open_deep_research)

与本项目的共同点是：把长任务组织成多个步骤，分离模型与工具，并为不同处理环节配置模型。它面向研究报告，本项目面向四阶段教师培养，因而业务路由、人工确认和正式评价边界不同。

可借鉴：WF1的资源检索和证据摘要、WF4的教学研究材料整理，以及按任务配置模型。不要直接把研究智能体的自主搜索循环替换成本项目的教学流程。该仓库在核对时已归档，仅作为公开代码参考，不将其描述为持续维护的依赖。

### 13.2 OpenAI Agents SDK教学分流：官方教学示例

官方快速入门定义数学辅导、历史辅导和分流智能体。分流智能体通过 handoff 将问题交给对应专家，Runner 管理执行和交接。这是教学类角色分工示例，不是完整的教师培养平台。[官方教学示例](https://openai.github.io/openai-agents-python/quickstart/)

与本项目相似的是按专业职责拆分能力。差异在于示例允许模型选择交接对象，而本项目要求四条工作流的业务路由由确定性代码控制。

可借鉴：学习教练、教学设计教练和反思教练各自使用聚焦的提示词和明确输入输出。专业角色可以参与节点内部的候选生成，但不能绕过权限、正式评价和人工确认。

Agents SDK还提供工具、状态、护栏、人工复核与运行追踪等能力。它们与本项目存在对应的工程需求，但不证明本项目已经完整实现这些能力。[OpenAI Agents SDK官方介绍](https://developers.openai.com/api/docs/guides/agents/sdk)

### 13.3 Google ADK工作流智能体：顺序、并行和循环

Google ADK提供工作流智能体来组织顺序、并行和循环执行。工作流结构控制执行次序，内部步骤可以使用模型智能体。[官方工作流说明](https://google.github.io/adk-docs/agents/workflow-agents/)

这与本项目“由程序确定流程、由模型辅助部分步骤”的思路相近。可以参考其组合方式理解四阶段顺序衔接、独立证据读取的并行处理和设计修订循环。

本项目仍采用 LangGraph 实现这些需求。仅当输入相互独立、没有共享写入冲突时才考虑并行；修订和验证循环继续遵守次数上限以及人工出口。

### 13.4 Microsoft Agent Framework：企业工作流框架

Microsoft Agent Framework将智能体与普通函数连接为显式工作流，包含模型适配、会话状态和扩展机制。官方建议在步骤明确、需要控制顺序时使用工作流。[框架概览](https://learn.microsoft.com/en-us/agent-framework/overview/)

其检查点机制支持保存和恢复运行状态，人工介入机制可以暂停工作流并等待响应。[检查点说明](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)、[人工介入说明](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)

与本项目相似的是显式执行路径、状态恢复和人工确认；差异在于运行时及存储接口。可参考其请求与响应关联机制，检查本项目人工确认后是否恢复到正确线程和步骤。

AutoGen也是多智能体架构的重要公开参考；Microsoft当前的Agent Framework结合了AutoGen与Semantic Kernel的设计经验。本手册以当前Agent Framework作为微软方向的主要对照，不将AutoGen与本项目描述为完全相同的架构。

### 13.5 对应到本项目目录

| 通用架构概念 | 本项目位置 | 开发人员应关注的问题 |
| --- | --- | --- |
| 工作流编排 | `workflows/`、`orchestration/` | 节点顺序、条件路由和阶段衔接是否明确 |
| 专业智能体角色 | `agents/`、`prompts/` | 角色的输入、职责和输出是否明确；部分目录仍是工程骨架 |
| 工具与工具契约 | `tools/` | 输入校验、超时、错误和候选结果是否完整 |
| 模型供应商适配 | `model_services/` | 业务是否依赖稳定网关而非厂商客户端 |
| 执行状态恢复 | `infrastructure/checkpointer/` | 是否沿用原线程，恢复时是否可能重复产生副作用 |
| 业务数据与证据 | `infrastructure/database/`、`contracts/` | 数据归属、引用和跨工作流协议是否一致 |
| 运行观测 | `observability/`、`core/` | 目录存在不等于监控完成，需补齐真实事件和链路记录 |

上述目录映射是针对本项目作出的设计分析，并非外部框架要求采用相同目录。

### 13.6 架构判断与实施建议

图编排、工具调用、结构化状态、人工复核和模型适配在这些公开项目中有明确依据，因此本项目采用的是常见工程模式。模块化单体和分层目录则是面向当前团队规模的工程选择；没有证据说明所有主流智能体都采用完全相同的 Clean Architecture 或领域驱动目录。

建议保留 LangGraph 作为唯一主编排层，优先补齐工具真实实现、输入输出模型、证据存储和恢复幂等性。七人分工有助于明确责任，但两名工具负责人承担122个工具，应按业务阶段分批交付，不能仅按工具数量判断工作量。

当前仅完成静态检查，不能由“节点已注册”或“工具已有名称”推断系统已经通过端到端验证。生产可用性需在后续获得运行验证授权后另行确认。

ChatGPT、Claude、GitHub Copilot等商业产品未完整公开其内部实现，本手册不将其列为与本项目同架构的已验证案例。
