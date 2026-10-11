# WF1和WF2工具开发任务分配

## 1 任务目标

本轮由两名开发者分别完成 WF1 会学习和 WF2 会设计所需工具的契约、实现、Fake、测试和接入说明。两人只开发工具及其端口适配，不实现 LangGraph 节点、图路由、正式评价工作流或成长画像更新工作流。

工具只能返回结构化候选结果或候选证据。权限、事务、路由、CCI 数值、终态、正式评分和版本迁移必须由确定性业务代码控制。

## 2 共同约束

1. 先冻结工具契约和错误码，再写实现；不得先写 Prompt。
2. 所有输入输出使用明确的 Pydantic Schema，并包含 `schema_version` 和 `tool_version`。
3. 统一返回成功结果、可恢复错误、不可恢复错误、降级结果和审计元数据。
4. 每个工具声明超时、有限重试、最小权限、幂等要求和降级策略。
5. 模型输出必须先做 Schema 校验，再做业务不变量校验。
6. 大对象写入对象存储或业务存储，工具结果只返回引用和小型摘要。
7. 外部依赖必须提供 Fake，单元测试不得依赖真实模型、数据库或网络。
8. 工具不得决定下一工作流节点，也不得直接修改其他工作流的内部 State。
9. WF2 一律使用 `teaching_process_design`，不得建立课堂执行或虚拟学生能力。
10. WF2 的自动评价只生成候选诊断和证据，正式 Rubric 评分由公共多源评价工作流负责。

## 3 开发者A任务包

### 3.1 主责范围

负责 WF1 基于认知冲突动态调节的自我导向学习工具流，代码主目录：

- `src/teacher_education_agent/tools/wf1_learning`
- `tests/unit/tools/wf1_learning`
- WF1 所需的工具契约和适配器

### 3.2 工具清单

| 编号 | 工具 | 职责 | 输出 | 超时和重试 | 降级 |
|---|---|---|---|---|---|
| A01 | `learning_context` | 读取任务、学习情境和画像摘要 | `ContextSnapshot` | 5秒，重试2次 | 返回空画像摘要 |
| A02 | `readiness_assessor` | 诊断学习需要和真实起点 | `NeedAssessment` | 6秒，重试1次 | 规则问卷 |
| A03 | `goal_level_assessor` | 分别评价 Bloom 和 SOLO 起点 | `BloomSoloAssessment` | 8秒，重试1次 | unknown 加学习者自评 |
| A04 | `question_assessor` | 评价问题质量和可探究性 | `QuestionQuality` | 6秒，重试1次 | 确定性规则检查 |
| A05 | `resource_recommender` | 调用公共资源推荐能力 | `ResourceCandidate[]` | 8秒，重试1次 | 自选、跳过或人工 |
| A06 | `learning_feedback` | 生成不代写的探究反馈候选 | `FeedbackEnvelope` | 12秒，重试1次 | 静态支架 |
| A07 | `evidence_store` | 保存证据、归属和引用 | `EvidenceRecord` | 5秒，重试2次 | 暂停并返回可恢复错误 |
| A08 | `conflict_detector` | 认知冲突二分类 | `ConflictDetection` | 3秒，重试1次 | unknown 并继续学习 |
| A09 | `conflict_classifier` | 三层八类冲突分类 | `ConflictClassification` | 3秒，重试1次 | unknown 加通用支架 |
| A10 | `cci_calculator` | 使用确定性代码计算 CCI 与区间 | `CCIResult` | 1秒，不重试 | unknown 加通用支架 |
| A11 | `strategy_repository` | 检索支架策略并记录版本 | `StrategyRecord` | 3秒，重试2次 | 内置安全策略 |
| A12 | `source_verifier` | 核验主张、来源和支持关系 | `VerificationReport` | 10秒，重试1次 | 标记 unsupported |
| A13 | `rubric_evaluator` | 分别形成 Bloom、SOLO 和迁移候选评价 | `LevelEvidenceResult` | 8秒，重试1次 | 待人工复核 |
| A14 | `learner_profile_repository` | 读取和写入画像版本 | `ProfileVersion` | 3秒，重试2次 | warning，不阻断完成 |
| A15 | `checkpoint_store` | 保存和恢复执行位置 | `CheckpointRef` | 5秒，重试2次 | fail closed |
| A16 | `audit_outbox` | 写入审计和可靠事件 | `EventRef` | 5秒，重试2次 | 进入重试队列 |

### 3.3 必须实现的业务不变量

- Bloom 和 SOLO 分别存储、分别评价，不生成合并总分。
- 冲突检测仅接收已经通过资格门控的有效学习者证据；工具自身仍需拒绝缺少门控字段的调用。
- `cci_calculator` 不调用 LLM，边界严格为小于 2.5、2.5 至 3.5、大于 3.5。
- 同一证据事件最多返回 3 次调节记录；过载只返回调节建议和复评要求，不直接对外发送教师预警。
- AI 生成内容、外部材料和学习者原始证据必须明确标注来源，不得冒充学习者证据。
- `checkpoint_store` 只保存工作流执行状态，不承担业务数据库职责。

### 3.4 测试任务

- 为 16 个工具分别覆盖正常、非法输入、权限不足、超时、重试耗尽和降级路径。
- 对 `cci_calculator` 做 2.5、3.5、空值、越界值和舍入边界测试。
- 对冲突检测与分类做低置信度、服务不可用和模型输出 Schema 非法测试。
- 对证据、画像、Checkpoint 和 Outbox 做幂等、并发冲突和重放测试。
- 提供端到端 Fake 链路：有效证据到冲突检测、分类、CCI、策略检索、复评结果。

### 3.5 交付物

- 工具 Schema、Protocol 和错误码。
- 16 个工具实现或稳定适配器。
- Fake 实现和测试夹具。
- 完整自动化测试。
- `docs/workflows/wf1_tool_catalog.md`，记录版本、权限、超时、重试、降级和示例。

## 4 开发者B任务包

### 4.1 主责范围

负责 WF2 教学系统设计工具流，代码主目录：

- `src/teacher_education_agent/tools/wf2_design`
- `tests/unit/tools/wf2_design`
- WF2 所需的工具契约和适配器

### 4.2 模块和专家工具映射

| 工程模块 | 专家工具 | 主要职责 | 结构化输出 |
|---|---|---|---|
| `needs_analysis` | T1 资料检索、T2 数据分析 | 解析课程标准、教学任务、现实问题和已有数据，形成教学需要 | `TeachingNeedAnalysis` |
| `learner_diagnosis` | T2 数据分析、T3 学习者诊断 | 分析知识、思维、动机、兴趣和认知风格 | `LearnerDiagnosis` |
| `goal_validation` | T5 目标生成、T6 目标校验 | 生成目标候选并检查可观察、可测量和可评价性 | `GoalDesignResult`、`GoalValidationResult` |
| `content_organization` | T7 知识检索、T8 知识组织、T9 内容生成 | 提取、筛选和组织教学内容，建立知识关联 | `ContentOrganizationResult` |
| `strategy_recommendation` | T10 教学策略推荐 | 推荐教学方法和策略候选并说明依据 | `StrategyRecommendation` |
| `media_recommendation` | T12 教学媒体和教学行为推荐 | 选择媒体与设计阶段行为，不运行真实课堂 | `MediaDesignRecommendation` |
| `exercise_generation` | T13 复习总结、T14 练习生成、T15 个性化作业 | 生成复习提纲、练习题和作业候选 | `ExercisePackage` |
| `alignment_validation` | T16 自动评价、T18 教学效果分析 | 检查目标、活动、内容、媒体、练习和评价的一致性 | `DesignAlignmentReport` |

### 4.3 必须补齐的设计工具

专家工具表未单列下列能力，但业务要求明确，开发者 B 必须在上述模块中补齐：

- 教学目标合理性和可评价性检查。
- 学习内容与目标匹配检查。
- 提问设计质量检查。
- 教学方法与学习者状态适配检查。
- 教学媒体与目标、内容、方法适配检查。
- `teaching_process_design` 中导入、讲授、复习总结和练习作业的设计检查。
- 目标、活动、评价一致性检查。
- 问题定位和修订建议生成。
- `TeachingDesignPackage` 组装前的完整性检查。

### 4.4 明确边界

- N7-3 在工程中解释为教学过程设计，禁止命名为教学过程执行。
- 不开发虚拟学生、课堂事件、现场判断、课堂运行和系统性反思迁移。
- 不使用“作业正确率”作为唯一达成依据，应返回多源学习证据和目标达成候选判断。
- 自动评价工具不输出正式评分，只输出设计诊断、候选证据和待复核项。
- 所有生成工具必须附来源、设计依据、不确定性和可编辑字段。

### 4.5 测试任务

- 为 8 个工程模块覆盖正常、缺失数据、相互冲突信息、空检索结果、超时和降级路径。
- 目标校验覆盖不可观察、不可测量、超出学习者水平和无法评价等情况。
- 内容组织覆盖目标不匹配、范围过宽、关键知识缺失和知识关系冲突。
- 一致性检查覆盖目标无活动、活动无评价、评价不对应目标、媒体无依据和练习难度失配。
- 练习生成覆盖答案可验证性、难度分层、重复题和不安全内容。
- 提供完整 Fake 链路：需要分析到 `TeachingDesignPackage` 候选组装。

### 4.6 交付物

- 8 个模块下的工具 Schema、Protocol 和实现。
- 15 个专家工具能力的映射说明。
- Fake 实现和测试夹具。
- 完整自动化测试。
- `docs/workflows/wf2_tool_catalog.md`，记录节点映射、版本、降级和示例。

## 5 公共能力所有权

为避免重复实现，公共能力采用单一所有者：

| 公共能力 | 主责 | 协作规则 |
|---|---|---|
| `tools/contracts.py` 通用调用信封、错误和审计字段 | 开发者A | 开发者B评审后共同冻结 |
| `common/knowledge_retrieval` | 开发者B | WF1 通过接口复用，不复制检索实现 |
| `common/resource_search` | 开发者B | WF1 的资源推荐只写适配器 |
| `common/evidence` | 开发者A | WF2 复用候选证据写入接口 |
| `common/content_safety` | 开发者A | 两条工具流统一调用 |
| 画像读取契约 | 开发者A | WF2 只读复用，写入仍走独立成长画像工作流 |
| 正式多源评价接口 | 暂不由两人实现 | 两人只提交候选证据契约 |

任一公共契约变更必须由另一名开发者评审，并同步更新双方契约测试。

## 6 合并顺序

1. 两人共同冻结通用 Tool 调用信封、错误码、版本字段和 Fake 规范。
2. 开发者 A 提交公共契约、证据和安全基础能力；开发者 B 同步提交知识检索和资源检索能力。
3. 两人分别完成各自工具 Schema、Protocol、Fake 和单元测试。
4. 先合并确定性工具，再合并外部服务和模型适配器。
5. 完成跨工具链契约测试后，才允许工作流节点接入。

## 7 完成定义

每名开发者的任务只有在以下条件全部满足时才算完成：

- 工具清单全部有稳定输入输出契约。
- 每个工具有超时、重试、权限、降级和错误码定义。
- 正常和异常路径均有自动化测试。
- Fake 链路可在无模型、无数据库和无网络环境下运行。
- 没有工具拥有工作流路由权或正式评分权。
- 没有把大对象、密钥或敏感原文写入 State 或日志。
- 文档、示例和契约测试与实现同步。
- 双方公共契约测试全部通过。

## 
