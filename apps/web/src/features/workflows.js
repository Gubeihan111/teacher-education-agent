export const workflows = [
  {id: 'learning', name: 'wf1_cr_sdl_v3', title: '会学习', subtitle: '明确目标，带着问题探究', fields: [
    ['learning_task_ref', '学习任务编号', '例如 learning-001'],
    ['learner_statement', '学习需要', '你希望解决什么问题？'],
    ['goal', '学习目标', '描述本轮可检验的目标'],
    ['question', '探究问题', '你打算从哪个问题开始？']
  ]},
  {id: 'design', name: 'wf2_instructional_design_v1', title: '会设计', subtitle: '形成有依据的教学方案', fields: [
    ['needs_statement', '教学需求', '填写教学主题、学生特点和预期目标']
  ]},
  {id: 'practice', name: 'wf3_teaching_implementation_judgment_v1', title: '会实施与判断', subtitle: '在课堂情境中练习专业判断', fields: [
    ['design_ref', '教学方案引用', '填写已有教学方案编号']
  ]},
  {id: 'reflection', name: 'wf4_reflection_transfer_v1', title: '会反思与迁移', subtitle: '从证据中改进，在新情境中应用', fields: [
    ['practice_record_ref', '实践记录引用', '填写已有课堂实践记录编号'],
    ['evidence_package_ref', '证据包引用', '填写已生成的证据包编号'],
    ['reflection_text', '反思记录', '描述事实、原因、改进策略与预期结果']
  ]}
];

export function initialState(id, form) {
  const state = {stage_index: 0, evidence_refs: [], loop_limit: 3, needs_revision: false,
    needs_human_review: false, node_visits: {}, route_decisions: {}};
  const definition = workflows.find(item => item.id === id);
  for (const [key] of definition.fields) state[key] = String(form.get(key) || '').trim();
  if (id === 'learning') Object.assign(state, {session_status: 'active', iteration_count: 0,
    learner_id: 'api-user', baseline_evidence_refs: []});
  if (id === 'design') Object.assign(state, {owner_id: 'api-user', revision_count: 0, goals: [],
    content_outline: [], strategies: [], media_plan: [], teaching_process: [], assessment_plan: [], alignment_issues: []});
  if (id === 'practice') Object.assign(state, {owner_id: 'api-user', cycle_count: 0, task_config: {},
    scenario_config: {}, classroom_state: {}, detected_events: [], judgment_candidates: [], scaffold_history: []});
  if (id === 'reflection') Object.assign(state, {owner_id: 'api-user', iteration_count: 0,
    problem_candidates: [], attribution_candidates: [], validation_evidence_refs: [], transfer_evidence_refs: [], inquiry_cycle_refs: []});
  return state;
}
