"""WF4 evidence reflection, strategy validation, transfer and inquiry tools."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from ..contracts import ToolContext, ToolSpec, ToolStatus
from ..foundation import keyword_score, overlap_score, stable_ref
from ..registry import RegisteredTool

WF4_TOOL_NAMES = (
 "reflection_context_reader", "practice_evidence_reader", "growth_history_reader", "evaluation_result_reader", "scaffold_history_reader",
 "reflection_evidence_organizer", "problem_candidate_detector", "reflection_dimension_classifier", "evidence_consistency_checker", "problem_priority_ranker",
 "explanation_structure_analyzer", "attribution_candidate_generator", "evidence_chain_validator", "alternative_explanation_generator", "causal_claim_checker",
 "strategy_candidate_generator", "strategy_alignment_checker", "strategy_risk_checker", "strategy_plan_builder", "strategy_selection_recorder",
 "practice_execution_facade", "validation_indicator_builder", "pre_post_evidence_comparator", "validation_conclusion_builder", "validation_retry_counter",
 "transfer_task_generator", "transfer_condition_checker", "transfer_evidence_collector", "transfer_performance_analyzer", "transfer_scaffold_recommender",
 "inquiry_question_generator", "inquiry_plan_builder", "inquiry_evidence_organizer", "inquiry_conclusion_checker", "inquiry_cycle_recorder",
 "reflection_structure_assessor", "solo_level_candidate", "reflection_coverage_checker", "strategy_effect_summarizer", "stage_achievement_candidate",
 "growth_evidence_builder", "profile_update_candidate", "audit_event_writer", "checkpoint_writer", "human_review_packet_builder", "formal_evaluation_request_builder",
)
_PORTS = {"reflection_context_reader", "practice_evidence_reader", "growth_history_reader", "evaluation_result_reader", "scaffold_history_reader",
 "practice_execution_facade", "strategy_selection_recorder", "inquiry_cycle_recorder", "audit_event_writer", "checkpoint_writer"}

def _handler(name: str):
 def run(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
  service = context.services.get(name)
  if service is not None: return service(payload, context)
  if name in _PORTS: return {"available": False, "executed": False, "_status": ToolStatus.DEGRADED, "_warnings": (f"{name}_unavailable",)}
  text = str(payload.get("reflection") or payload.get("text") or payload.get("evidence") or "")
  if name in {"evidence_consistency_checker", "evidence_chain_validator", "causal_claim_checker", "inquiry_conclusion_checker"}:
   refs=payload.get("evidence_refs", []); return {"valid": isinstance(refs,list) and bool(refs), "evidence_count": len(refs) if isinstance(refs,list) else 0, "candidate_only": True}
  if name in {"reflection_dimension_classifier", "problem_candidate_detector", "attribution_candidate_generator", "stage_achievement_candidate", "solo_level_candidate"}:
   score=keyword_score(text,("证据","原因","策略","结果","迁移")); return {"candidate": "evidence_based" if score else "insufficient_evidence", "confidence": score, "candidate_only": True}
  if name in {"strategy_alignment_checker", "pre_post_evidence_comparator", "transfer_performance_analyzer"}:
   return {"score": overlap_score(str(payload.get("goal","")), text), "candidate_only": True}
  if name == "validation_retry_counter":
   count=int(payload.get("count",0))+1; limit=int(payload.get("limit",2)); return {"count":count,"limit":limit,"exhausted":count>=limit}
  if name in {"strategy_risk_checker", "transfer_condition_checker", "reflection_coverage_checker"}:
   return {"passed": bool(text or payload.get("evidence_refs")), "candidate_only": True}
  if name.endswith("generator") or name.endswith("builder") or name.endswith("recommender"):
   return {"candidate_ref": stable_ref(name, context.tenant_id, text, payload), "candidate_only": True, "requires_review": True}
  return {"result_ref": stable_ref(name, context.tenant_id, text, payload), "candidate_only": True}
 return run

def build_wf4_tools() -> tuple[RegisteredTool, ...]:
 return tuple(RegisteredTool(ToolSpec(name=n, version="1.0.0", description=f"WF4 {n}", permission="reflection:assist",
  timeout_seconds=8, max_retries=1, deterministic=not (n.endswith("generator") or n.endswith("builder"))), _handler(n)) for n in WF4_TOOL_NAMES)
