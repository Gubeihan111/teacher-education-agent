# 原图节点—LangGraph节点—工具—输入输出—路由对照表

本表由代码清单生成。`diagram`表示原图节点，`supplement`表示为完整运行补充的工程节点。所有路由值均为有限枚举，未识别值走默认路由。

## wf1_cr_sdl_v3

| 来源 | 原图节点编号 | LangGraph节点 | 使用工具 | 输入 | 输出 | 条件路由 |
|---|---|---|---|---|---|---|
| diagram | initialize_session | 初始化学习会话 | 无外部工具 | InputState、RuntimeContext | workflow/session/thread 标识、phase、status、预算计数器 | 顺序进入下一节点 |
| diagram | load_learning_context | 加载学习情境 | wf1.learning_context | task_ref、learner_id、tenant_id | task_snapshot、profile_summary_ref、context_constraints | 顺序进入下一节点 |
| diagram | diagnose_readiness | 诊断学习需要与起点 | wf1.readiness_assessor | task_snapshot、profile_summary_ref、learner_message | learning_need_summary、readiness_snapshot | continue→elicit_goal；request_more→diagnose_readiness；默认→elicit_goal |
| diagram | elicit_goal | 征集初步目标 | 无外部工具 | learning_need_summary | goal_draft_raw、status=waiting | 顺序进入下一节点 |
| diagram | identify_knowledge_object | 识别知识对象 | 无外部工具 | goal_draft_raw、task_snapshot | knowledge_objects、goal_scope | 顺序进入下一节点 |
| diagram | assess_goal_levels | 判断Bloom与SOLO起点 | wf1.goal_level_assessor | knowledge_objects、readiness_snapshot、baseline_evidence_refs | bloom_start、solo_start、level_evidence_refs、confidence | 顺序进入下一节点 |
| diagram | propose_goal_path | 形成二维目标与进阶路径 | 无外部工具 | bloom_start、solo_start、knowledge_objects、goal_draft_raw | bloom_target_proposed、solo_target_proposed、milestones、success_criteria | 顺序进入下一节点 |
| diagram | confirm_goal | 确认目标层级与证据 | 无外部工具 | goal proposal 全部字段 | goal_decision、goal_contract_candidate | approve→persist_goal_contract；revise→elicit_goal；change_level→propose_goal_path；默认→pause_or_manual_help |
| diagram | persist_goal_contract | 固化目标契约 | 无外部工具 | goal_contract_candidate、goal_decision | goal_contract_ref、goal_version、phase=question_planning | 顺序进入下一节点 |
| diagram | elicit_question | 征集核心问题 | 无外部工具 | goal_contract_ref | starting_question_raw、status=waiting | 顺序进入下一节点 |
| diagram | assess_question_quality | 评价问题质量 | wf1.question_assessor | starting_question_raw、goal_contract_ref | question_quality、question_feedback | 顺序进入下一节点 |
| diagram | build_question_tree | 构建问题树 | 无外部工具 | starting_question_raw、goal_contract_ref、question_quality | question_tree_candidate、dependency_edges | 顺序进入下一节点 |
| diagram | confirm_question_tree | 确认问题树 | 无外部工具 | question_tree_candidate、question_quality | question_tree_decision、question_tree_confirmed | approve→plan_learning；revise→build_question_tree；默认→pause_or_manual_help |
| diagram | plan_learning | 制定学习策略与节奏 | 无外部工具 | goal_contract_ref、question_tree_confirmed、readiness_snapshot | strategy_plan、resource_requirements、time_budget | 顺序进入下一节点 |
| diagram | recommend_resources | 推荐候选资源 | wf1.resource_recommender | resource_requirements、goal/query refs | resource_candidates、recommendation_trace | 顺序进入下一节点 |
| diagram | confirm_learning_contract | 确认学习契约 | 无外部工具 | question_tree、strategy_plan、resource_candidates | learning_contract_candidate、contract_decision | approve→persist_learning_contract；revise→plan_learning；默认→pause_or_manual_help |
| diagram | persist_learning_contract | 固化学习契约 | 无外部工具 | learning_contract_candidate、contract_decision | learning_contract_ref、learning_started=true、phase=inquiry | 顺序进入下一节点 |
| diagram | select_subquestion | 选择当前子问题 | 无外部工具 | question_tree、subquestion_statuses、learner_choice | current_subquestion_id、round_index | 顺序进入下一节点 |
| diagram | capture_initial_evidence | 收集先行尝试 | wf1.evidence_store | current_subquestion_id | learner_evidence_ref、status=waiting | 顺序进入下一节点 |
| diagram | validate_evidence | 校验学习证据 | 无外部工具 | learner_evidence_ref、event_type | learner_evidence_valid、evidence_quality | valid→provide_feedback；invalid→capture_initial_evidence；默认→capture_initial_evidence |
| diagram | provide_feedback | 提供材料、案例或不同观点 | wf1.learning_feedback | current_subquestion、valid evidence、strategy_plan | feedback_ref、feedback_type、feedback_claims | 顺序进入下一节点 |
| diagram | capture_analysis_response | 收集比较与核验 | 无外部工具 | learner_evidence_ref、feedback_ref | analysis_evidence_ref、event_type、self_report | eligible→run_conflict_subgraph；not_eligible→collect_self_judgment；默认→collect_self_judgment |
| diagram | run_conflict_subgraph | 调用认知冲突子图 | 无外部工具 | learning_started、valid evidence、analysis evidence、event_type | conflict_summary、regulation_summary、warning_summary | ；默认→detect_conflict |
| diagram | collect_self_judgment | 收集学习者自我判断 | 无外部工具 | analysis_evidence、conflict_summary、success_criteria | self_judgment、confidence_after、next_intent | continue_questioning→elicit_followup；change_strategy→adjust_learning_path；resolved→record_tentative_solution；默认→pause_or_manual_help |
| diagram | elicit_followup | 引导自主追问 | 无外部工具 | self_judgment、question_context、round_index | followup_question、followup_type | 顺序进入下一节点 |
| diagram | adjust_learning_path | 调整策略或资源 | 无外部工具 | progress_snapshot、strategy_plan、warnings | strategy_plan_next、resource_delta、adjust_reason | 顺序进入下一节点 |
| diagram | record_tentative_solution | 记录子问题暂定解 | 无外部工具 | self_judgment、analysis_evidence | tentative_solution_ref、subquestion_status=tentative | remaining→select_subquestion；all_tentative→integrate_viewpoint；默认→select_subquestion |
| diagram | integrate_viewpoint | 整合学习者观点 | 无外部工具 | tentative_solution_refs、question_tree | viewpoint_candidate、open_uncertainties | ；默认→verify_sources |
| diagram | detect_conflict | 识别认知冲突 | wf1.conflict_detector | pre/post learner evidence、feedback claims、context | conflict_detected、detection_confidence、conflict_evidence_spans | 顺序进入下一节点 |
| diagram | classify_conflict | 分类三层八类 | wf1.conflict_classifier | conflict spans、context | conflict_layer、conflict_type、type_confidence | 顺序进入下一节点 |
| diagram | calculate_cci | 计算CCI | wf1.cci_calculator | conflict features、history refs、self report | cci_value、cci_band、cci_delta、overload_streak | 顺序进入下一节点 |
| diagram | select_regulation_strategy | 选择调节策略 | wf1.strategy_repository | conflict type、CCI、goal levels、history | regulation_strategy_id、strategy_reason | 顺序进入下一节点 |
| diagram | generate_scaffold | 生成个性化支架 | 无外部工具 | strategy、evidence、goal levels | scaffold_ref、scaffold_payload | 顺序进入下一节点 |
| diagram | capture_post_regulation | 收集调节后证据 | 无外部工具 | scaffold_payload | post_regulation_evidence_ref、status=waiting | 顺序进入下一节点 |
| diagram | reassess_conflict | 复评冲突与进展 | 无外部工具 | post evidence、prior CCI/conflict | cci_after、conflict_after、progress_after | suitable_or_progress→persist_conflict_episode；still_abnormal_under_limit→select_regulation_strategy；over_limit_or_help→evaluate_warning；默认→evaluate_warning |
| diagram | evaluate_warning | 评估预警 | 无外部工具 | reassessment history、help/safety signals | warning_level、warning_reason、teacher_alert_candidate | 顺序进入下一节点 |
| diagram | persist_conflict_episode | 记录冲突片段 | 无外部工具 | conflict/regulation/warning summaries | conflict_episode_ref | ；默认→collect_self_judgment |
| diagram | verify_sources | 核验事实与来源 | wf1.source_verifier | viewpoint_candidate、source_refs | verification_report、unsupported_claims | 顺序进入下一节点 |
| diagram | request_self_explanation | 请求自我解释 | 无外部工具 | viewpoint_candidate、success_criteria | self_explanation_ref、status=waiting | 顺序进入下一节点 |
| diagram | evaluate_self_explanation | 评价解释证据 | 无外部工具 | self_explanation、goal contract、rubric | bloom_evidence_result、solo_evidence_result、gaps | 顺序进入下一节点 |
| diagram | generate_transfer_task | 生成迁移或变式任务 | 无外部工具 | goal contract、viewpoint、gaps | transfer_task_ref、transfer_rubric | 顺序进入下一节点 |
| diagram | evaluate_transfer | 评价迁移表现 | 无外部工具 | transfer_response_ref、rubric | transfer_result、transfer_evidence_refs | 顺序进入下一节点 |
| diagram | evaluate_stage_goal | 评价阶段目标 | wf1.rubric_evaluator | verification、Bloom/SOLO、transfer | stage_goal_status、stage_gap、recommended_route | not_met→adjust_learning_path；met→collect_reflection；默认→adjust_learning_path |
| diagram | collect_reflection | 收集阶段反思与归因 | 无外部工具 | learning trace summary、goal evaluation | reflection_ref、attribution、learner_strategy_rating | 顺序进入下一节点 |
| diagram | update_self_efficacy | 更新自我效能摘要 | 无外部工具 | reflection、evidence outcomes | self_efficacy_delta、self_efficacy_note | 顺序进入下一节点 |
| diagram | update_learner_profile | 更新长期学习画像 | wf1.learner_profile_repository | reflection、goal outcomes、strategy effects | profile_update_ref、profile_version | 顺序进入下一节点 |
| diagram | evaluate_overall_goal | 评价总体目标 | 无外部工具 | all stage statuses、goal contract、learner decision | overall_goal_status、next_cycle_decision | new_cycle→elicit_goal；revise→elicit_goal；complete→complete_session；默认→pause_or_manual_help |
| diagram | complete_session | 完成会话 | 无外部工具 | overall status、all result refs | OutputState completed、portfolio_ref | ；默认→__end__ |
| diagram | pause_or_manual_help | 暂停与人工帮助 | 无外部工具 | phase、reason、current refs | status=waiting、interrupt payload、help_ticket_ref? | 顺序进入下一节点 |
| diagram | finalize_cancelled | 取消会话 | 无外部工具 | cancel decision、side_effect_refs | status=cancelled、OutputState | ；默认→__end__ |
| diagram | finalize_expired | 处理等待过期 | 无外部工具 | interrupt_created_at、expiry_policy | status=expired、next_action | ；默认→__end__ |
| diagram | finalize_failed | 稳定失败终结 | 无外部工具 | error_code、error_ref、phase | status=failed、recoverable、support_ref | ；默认→__end__ |

## wf2_instructional_design_v1

| 来源 | 原图节点编号 | LangGraph节点 | 使用工具 | 输入 | 输出 | 条件路由 |
|---|---|---|---|---|---|---|
| diagram | N1 | 学习需要分析 | wf2.needs_analysis、wf2.material_search | 课程标准、知识图谱、现实问题 | 教学需求 | 顺序进入下一节点 |
| diagram | N2 | 学习者分析 | wf2.learning_data_analysis、wf2.learner_diagnosis | 学习者认知结构、动机水平、认知风格、兴趣等画像数据 | 学习者画像/状态 | 顺序进入下一节点 |
| diagram | N3 | 学习目标制定 | wf2.goal_generator | 教学需求、学习者画像/状态 | 学习目标 | 顺序进入下一节点 |
| diagram | N4 | 学习目标判断 | wf2.goal_validator | 学习目标、学习者画像、课程要求 | 目标合理性判断 | yes→N5；no→N3；默认→N3 |
| diagram | N5 | 学习内容制定 | wf2.knowledge_retrieval、wf2.knowledge_organization、wf2.content_generator | 学习目标、课程资源、知识图谱 | 教学内容/知识结构 | 顺序进入下一节点 |
| diagram | N6 | 教学内容判断 | 无外部工具 | 教学内容、学习目标、知识结构 | 内容适切性判断 | yes→N7；no→N5；默认→N5 |
| diagram | N7 | 教学策略制定 | wf2.strategy_recommender | 教学目标、内容、学习者状态 | 教学策略/方案 | 顺序进入下一节点 |
| diagram | N7-1 | 教学方法确定 | 无外部工具 | 教学目标、内容、学习者状态 | 教学方法设计方案 | 顺序进入下一节点 |
| diagram | N7-2 | 教学媒体选择 | wf2.media_recommender | 教学目标、内容、学习者状态 | 教学媒体、教学行为设计方案 | 顺序进入下一节点 |
| diagram | N7-3 | 教学过程实施 | 无外部工具 | 教学目标、内容、学习者状态、授课类型 | 教学实施方案 | 顺序进入下一节点 |
| diagram | N8 | 授课类型判断 | 无外部工具 | 授课类型、教学目标、教学内容 | 新授课或复习课路由 | new_lesson→N7-3-1；review_lesson→N7-3-3；默认→N7-3-3 |
| diagram | N7-3-1 | 导入新课 | 无外部工具 | 教学目标、内容、方法、媒体、学习者状态 | 导入新课的行为 | ；默认→N7-3-2 |
| diagram | N7-3-2 | 讲授新课 | 无外部工具 | 教学目标、内容、方法、媒体、学习者状态 | 讲授新课的行为 | ；默认→N7-3-4 |
| diagram | N7-3-3 | 复习总结 | wf2.review_summarizer | 教学内容、学习过程 | 复习材料/知识结构 | ；默认→N7-3-4 |
| diagram | N7-3-4 | 练习作业 | wf2.exercise_generator、wf2.personalized_assignment_recommender | 学习目标、教学内容、学习者状态 | 练习/作业 | 顺序进入下一节点 |
| diagram | N9 | 作业正确率判断 | 无外部工具 | 练习作业结果、正确率阈值 | 作业达标判断 | pass→N10；fail→N7-3-2；默认→N7-3-2 |
| diagram | N10 | 教学评价（形成性/总结性评价） | wf2.automatic_evaluator、wf2.design_effect_analyzer | 学生的过程性学习表现、作业练习结果 | 评价结果 | 顺序进入下一节点 |
| diagram | N11 | 修订改进 | wf2.alignment_validator | 评价结果 | 修订后的教学方案 | ；默认→__end__ |
| supplement | X2.HUMAN_REVIEW | 人工复核 | 无外部工具 | state | X2.HUMAN_REVIEW_result | ；默认→__end__ |
| supplement | X2.CANCELLED | 取消终态 | 无外部工具 | state | X2.CANCELLED_result | ；默认→__end__ |
| supplement | X2.EXPIRED | 过期终态 | 无外部工具 | state | X2.EXPIRED_result | ；默认→__end__ |
| supplement | X2.FAILED | 失败终态 | 无外部工具 | state | X2.FAILED_result | ；默认→__end__ |

## wf3_teaching_implementation_judgment_v1

| 来源 | 原图节点编号 | LangGraph节点 | 使用工具 | 输入 | 输出 | 条件路由 |
|---|---|---|---|---|---|---|
| diagram | N3.1.01 | 获取成长起点 | wf3.growth_profile_reader、wf3.practice_history_reader | 确认目标和已有能力 | PracticeBaseline | 顺序进入下一节点 |
| diagram | N3.1.02 | 生成训练任务 | wf3.task_config_reader | 确认或修订任务 | PracticeTaskConfig | READY→N3.2.01；NEEDS_REVISION→N3.1.02；WAITING_FOR_REVIEW→X3.HUMAN_REVIEW；默认→N3.1.02 |
| diagram | N3.2.01 | 建立GOAL_BASELINE | 无外部工具 | 确认目标与预期学生表现 | GoalBaseline | 顺序进入下一节点 |
| diagram | N3.2.02 | 生成情境与班级 | wf3.scenario_complexity_calculator、wf3.student_config_reader | 查看学生画像与约束 | ScenarioConfig | RUNNABLE→N3.3.01；TOO_COMPLEX→N3.2.02；INSUFFICIENT_CONFIG→N3.1.02；默认→N3.2.02 |
| diagram | N3.3.01 | 开始课堂交互 | wf3.speech_recognizer、wf3.teacher_action_recognizer | 讲解、提问、追问、反馈、等待、调整 | TeachingActionTrace | 顺序进入下一节点 |
| diagram | N3.3.02 | 采集学生响应 | wf3.virtual_student_responder | 与学生互动 | StudentResponseChain | 顺序进入下一节点 |
| diagram | N3.3.03 | 识别教学阶段 | wf3.phase_classifier | 无 | TeachingPhaseRecord | 顺序进入下一节点 |
| diagram | N3.3.04 | 提取观察证据 | wf3.rubric_evidence_mapper | 无 | RubricObservationEvidence | EVENT→N3.6.01；NO_EVENT→N3.4.01；AMBIGUOUS→N3.4.01；默认→N3.4.01 |
| diagram | N3.4.01 | 汇聚状态证据 | 无外部工具 | 无 | StateEvidence | SUFFICIENT→N3.4.02；INSUFFICIENT→N3.3.04；CONFLICTING→N3.4.03；默认→N3.3.04 |
| diagram | N3.4.02 | 识别当前成长状态 | wf3.student_state_estimator | 继续教学或响应提示 | TrainingState | UNDER_CHALLENGED→N3.5.01；OPTIMAL→N3.5.01；AT_RISK→N3.5.01；OVERLOADED→N3.5.01；UNCERTAIN→N3.4.03；默认→N3.4.03 |
| diagram | N3.4.03 | 预测临界趋势 | wf3.classroom_event_detector | 无 | StateTrendWarning | 顺序进入下一节点 |
| diagram | N3.5.01 | 确定干预方向 | wf3.scaffold_recommender | 接受或拒绝提示 | InterventionDecision | ESCALATE→N3.5.02；MAINTAIN→N3.5.02；FADE→N3.5.03；HOLD→N3.5.03；默认→N3.5.03 |
| diagram | N3.5.02 | 执行局部支架 | wf3.scaffold_message_generator | 利用提示继续教学 | ScaffoldRecord | 顺序进入下一节点 |
| diagram | N3.5.03 | 调整控制权 | 无外部工具 | 自主处理 | ControlTransferRecord | 顺序进入下一节点 |
| diagram | N3.6.01 | 捕捉关键课堂事件 | wf3.classroom_event_detector | 注意、解释事件 | CriticalEvent | 顺序进入下一节点 |
| diagram | N3.6.02 | J1关键事件感知 | 无外部工具 | 指出关键事件 | JudgmentPerception | 顺序进入下一节点 |
| diagram | N3.6.03 | J2专业解释与推理 | wf3.judgment_candidate_generator | 说明学生、内容、情境与理由 | JudgmentReasoning | 顺序进入下一节点 |
| diagram | N3.6.04 | J3判断行动选择 | 无外部工具 | 选择并实施行动 | JudgmentAction | 顺序进入下一节点 |
| diagram | N3.6.05 | J4结果追踪 | 无外部工具 | 关注学生与课堂变化 | JudgmentOutcome | JUDGMENT_COMPLETE→N3.7.01；PARTIAL→N3.6.02；NOT_OBSERVED→N3.3.01；默认→N3.7.01 |
| diagram | N3.7.01 | 定位关键回放片段 | wf3.key_timeline_extractor | 观看片段 | ReplaySegment | 顺序进入下一节点 |
| diagram | N3.7.02 | 证据核实与改进目标 | 无外部工具 | 自我解释何处及为何需要调整 | ImmediateImprovementTarget | RETEACH→N3.8.01；NO_RETEACH→X3.COMPLETE；NEEDS_REVIEW→X3.HUMAN_REVIEW；默认→N3.8.03 |
| diagram | N3.8.01 | 生成再教学任务 | 无外部工具 | 准备同情境或近变式再教学 | RetryTask | 顺序进入下一节点 |
| diagram | N3.8.02 | 执行再教学 | 无外部工具 | 再次教学 | RetryTrace | 顺序进入下一节点 |
| diagram | N3.8.03 | 稳定性验证 | wf3.pre_post_comparator | 在较低支持下完成 | StabilityEvidence | STABLE→X3.COMPLETE；PARTIAL→N3.8.01；UNSTABLE→N3.5.01；INSUFFICIENT_EVIDENCE→N3.3.04；默认→X3.HUMAN_REVIEW |
| supplement | X3.COMPLETE | 完成阶段三并输出证据包 | 无外部工具 | state | X3.COMPLETE_result | ；默认→__end__ |
| supplement | X3.HUMAN_REVIEW | 人工复核 | 无外部工具 | state | X3.HUMAN_REVIEW_result | ；默认→__end__ |
| supplement | X3.CANCELLED | 取消终态 | 无外部工具 | state | X3.CANCELLED_result | ；默认→__end__ |
| supplement | X3.EXPIRED | 过期终态 | 无外部工具 | state | X3.EXPIRED_result | ；默认→__end__ |
| supplement | X3.FAILED | 失败终态 | 无外部工具 | state | X3.FAILED_result | ；默认→__end__ |

## wf4_reflection_transfer_v1

| 来源 | 原图节点编号 | LangGraph节点 | 使用工具 | 输入 | 输出 | 条件路由 |
|---|---|---|---|---|---|---|
| diagram | N4.1.01 | 读取成长目标 | wf4.reflection_context_reader、wf4.growth_history_reader | 查看当前成长目标 | reflection_goal | 顺序进入下一节点 |
| diagram | N4.1.02 | 汇聚成长证据 | wf4.practice_evidence_reader | 无 | raw_reflection_evidence | 顺序进入下一节点 |
| diagram | N4.1.03 | 证据校验 | 无外部工具 | 无 | evidence_quality | 顺序进入下一节点 |
| diagram | N4.1.04 | 确定反思对象 | 无外部工具 | 查看证据范围 | ReflectionTask | SUFFICIENT→N4.2.01；INSUFFICIENT→N4.1.02；CONFLICTING→N4.1.02；默认→N4.1.02 |
| diagram | N4.2.01 | 描述关键事实 | 无外部工具 | 描述发生了什么 | describing_evidence | 顺序进入下一节点 |
| diagram | N4.2.02 | 教学评价 | 无外部工具 | 判断何处值得关注 | evaluating_evidence | 顺序进入下一节点 |
| diagram | N4.2.03 | 自主问题发现 | wf4.problem_candidate_detector | 提出关键实践问题 | ProblemStatement | 顺序进入下一节点 |
| diagram | N4.2.04 | 问题证据绑定 | wf4.evidence_consistency_checker | 指出支持问题的证据 | problem_evidence | IDENTIFIED→N4.3.01；PARTIALLY_IDENTIFIED→N4.2.03；NOT_IDENTIFIED→N4.2.01；默认→N4.2.03 |
| diagram | N4.3.01 | 初步专业解释 | wf4.attribution_candidate_generator | 提出可能原因/专业解释 | initial_explanation | 顺序进入下一节点 |
| diagram | N4.3.02 | 证据核验 | wf4.evidence_chain_validator | 引用证据 | supporting_evidence | SUPPORTED→N4.3.03；PARTIAL→N4.3.01；UNSUPPORTED→N4.3.01；UNCERTAIN→N4.3.02；默认→N4.3.01 |
| diagram | N4.3.03 | 竞争性解释 | wf4.alternative_explanation_generator | 先尝试提出其他解释 | competing_explanations | YES→N4.3.04；NO→N4.3.04；UNCERTAIN→N4.3.02；默认→N4.3.04 |
| diagram | N4.3.04 | 自我关联 | 无外部工具 | 联系自身行为、习惯、判断 | self_reference | 顺序进入下一节点 |
| diagram | N4.3.05 | 形成专业解释 | 无外部工具 | 比较并修正解释 | AttributionResult | ；默认→N4.4.01 |
| diagram | N4.4.01 | 自主提出替代行动 | wf4.strategy_candidate_generator | 提出多个可能行动 | alternative_actions | YES→N4.4.02；NO→N4.4.01；PARTIAL→N4.4.02；默认→N4.4.01 |
| diagram | N4.4.02 | 策略比较 | wf4.strategy_alignment_checker | 比较不同策略 | strategy_comparison | 顺序进入下一节点 |
| diagram | N4.4.03 | 选择改进策略 | 无外部工具 | 自主选择并说明理由 | selected_strategy | 顺序进入下一节点 |
| diagram | N4.4.04 | 定义验证证据 | 无外部工具 | 说明预期结果和需采证据 | evidence_to_collect | CONSISTENT→N4.5.01；PARTIAL→N4.4.02；INCONSISTENT→N4.4.01；默认→N4.4.02 |
| diagram | N4.5.01 | 生成验证任务 | 无外部工具 | 准备实施 | validation_task | 顺序进入下一节点 |
| diagram | N4.5.02 | 调用实践执行 | wf4.practice_execution_facade | 实际实施策略 | new_practice_trace | 顺序进入下一节点 |
| diagram | N4.5.03 | 前后证据比较 | wf4.pre_post_evidence_comparator | 无 | StrategyValidationResult | SUPPORTED→N4.6.01；PARTIALLY_SUPPORTED→N4.5.04；NOT_SUPPORTED→N4.5.04；INSUFFICIENT_EVIDENCE→N4.5.02；默认→N4.5.02 |
| diagram | N4.5.04 | 修正策略/解释 | 无外部工具 | 修正解释或策略 | revised_result | EXPLANATION→N4.3.01；STRATEGY→N4.4.01；TASK_MISMATCH→N4.5.01；UNCERTAIN→X4.HUMAN_REVIEW；默认→X4.HUMAN_REVIEW |
| diagram | N4.6.01 | 提取策略核心原则 | 无外部工具 | 说明策略为何有效 | transfer_principle | 顺序进入下一节点 |
| diagram | N4.6.02 | 构建迁移距离画像 | 无外部工具 | 无 | transfer_profile | T1→N4.6.03；T2→N4.6.03；T3→N4.6.03；默认→N4.6.03 |
| diagram | N4.6.03 | 生成迁移任务 | wf4.transfer_task_generator | 接受新挑战 | transfer_task | 顺序进入下一节点 |
| diagram | N4.6.04 | 独立迁移执行 | 无外部工具 | 判断、调整、实施 | transfer_trace | 顺序进入下一节点 |
| diagram | N4.6.05 | 迁移表现分析 | wf4.transfer_performance_analyzer、wf4.transfer_scaffold_recommender | 解释为何这样调整 | TransferResult | SUCCESS→X4.INQUIRY_DECISION；PARTIAL→N4.6.06；FAILED→N4.6.03；INSUFFICIENT_EVIDENCE→N4.6.04；默认→N4.6.06 |
| diagram | N4.6.06 | 实践问题转探究问题 | wf4.inquiry_question_generator | 提出可探究问题 | inquiry_question | PRINCIPLE_NOT_UNDERSTOOD→N4.3.01；STRATEGY_RIGID→N4.4.01；CONTEXT_MISREAD→N4.6.03；DISTANCE_TOO_HIGH→N4.6.02；UNCERTAIN→X4.HUMAN_REVIEW；默认→N4.6.03 |
| supplement | X4.INQUIRY_DECISION | 是否进入初步教学探究路径 | 无外部工具 | state | X4.INQUIRY_DECISION_result | YES→N4.6.07；NO→N4.7.01；默认→N4.7.01 |
| diagram | N4.6.07 | 基本证据计划 | wf4.inquiry_plan_builder | 说明采什么、怎么看 | evidence_plan | 顺序进入下一节点 |
| diagram | N4.6.08 | 实践解释与下一问题 | wf4.inquiry_evidence_organizer | 解释发现并提出下一问题 | TeachingInquiryRecord | 顺序进入下一节点 |
| diagram | N4.7.01 | 汇聚阶段证据 | 无外部工具 | 无 | stage_evidence | 顺序进入下一节点 |
| diagram | N4.7.02 | 反思维度覆盖与适切性 | wf4.reflection_coverage_checker | 无 | reflection_coverage | 顺序进入下一节点 |
| diagram | N4.7.03 | 自主性分析 | 无外部工具 | 无 | autonomy_evidence | 顺序进入下一节点 |
| diagram | N4.7.04 | 迁移达成分析 | 无外部工具 | 无 | transfer_evidence | 顺序进入下一节点 |
| diagram | N4.7.05 | 初步探究能力判断 | 无外部工具 | 无 | inquiry_evidence | 顺序进入下一节点 |
| diagram | N4.7.06 | 阶段达成判定 | wf4.stage_achievement_candidate | 无 | stage_status | ACHIEVED→N4.7.07；PARTIALLY_ACHIEVED→N4.7.07；INSUFFICIENT_EVIDENCE→N4.7.01；默认→N4.7.01 |
| diagram | N4.7.07 | 下一成长建议 | 无外部工具 | 查看/选择建议 | next_growth_proposal | ；默认→X4.COMPLETE |
| supplement | X4.COMPLETE | 完成阶段四并提交公共评价 | 无外部工具 | state | X4.COMPLETE_result | ；默认→__end__ |
| supplement | X4.HUMAN_REVIEW | 人工复核 | 无外部工具 | state | X4.HUMAN_REVIEW_result | ；默认→__end__ |
| supplement | X4.CANCELLED | 取消终态 | 无外部工具 | state | X4.CANCELLED_result | ；默认→__end__ |
| supplement | X4.EXPIRED | 过期终态 | 无外部工具 | state | X4.EXPIRED_result | ；默认→__end__ |
| supplement | X4.FAILED | 失败终态 | 无外部工具 | state | X4.FAILED_result | ；默认→__end__ |
