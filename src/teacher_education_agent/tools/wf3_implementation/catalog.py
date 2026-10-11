"""WF3 teaching implementation and professional-judgment tools."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..contracts import ToolContext, ToolSpec, ToolStatus
from ..foundation import clamp, keyword_score, require_text, stable_ref
from ..registry import RegisteredTool

WF3_TOOL_NAMES = (
 "growth_profile_reader", "practice_history_reader", "scaffold_history_reader", "evidence_persistence",
 "task_config_reader", "plan_config_reader", "student_config_reader", "event_config_reader", "scenario_complexity_calculator",
 "speech_recognizer", "teacher_action_recognizer", "virtual_student_responder", "classroom_state_updater", "timeline_recorder",
 "question_feature_extractor", "wait_time_calculator", "follow_up_feature_extractor", "feedback_feature_extractor", "participation_feature_extractor",
 "training_state_reader", "classroom_event_detector", "judgment_candidate_generator", "scaffold_recommender", "execution_controller",
 "evidence_replay_reader", "retry_counter", "observation_rubric_reader", "phase_classifier", "rubric_evidence_mapper",
 "interaction_quality_analyzer", "student_state_estimator", "event_trigger_evaluator", "judgment_evidence_validator", "scaffold_message_generator",
 "control_command_validator", "pre_post_comparator", "key_timeline_extractor", "observation_evidence_validator", "practice_outcome_builder",
 "growth_evidence_builder", "audit_event_writer", "checkpoint_writer",
 "link_outcome_builder",
)

_SERVICE_TOOLS = {"growth_profile_reader", "practice_history_reader", "scaffold_history_reader", "evidence_persistence",
 "task_config_reader", "plan_config_reader", "student_config_reader", "event_config_reader", "speech_recognizer",
 "virtual_student_responder", "timeline_recorder", "training_state_reader", "evidence_replay_reader", "observation_rubric_reader",
 "audit_event_writer", "checkpoint_writer"}

def _handler(name: str):
 def run(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
  service = context.services.get(name)
  if service is not None: return service(payload, context)
  if name in _SERVICE_TOOLS:
   return {"available": False, "executed": False, "_status": ToolStatus.DEGRADED, "_warnings": (f"{name}_unavailable",)}
  text = str(payload.get("transcript") or payload.get("text") or "")
  if name == "scenario_complexity_calculator":
   factors = payload.get("factors", {}); vals = [clamp(float(v)) for v in factors.values()] if isinstance(factors, Mapping) else []
   score = round(sum(vals) / max(len(vals), 1), 4); return {"complexity": score, "band": "high" if score > .66 else "medium" if score > .33 else "low"}
  if name == "wait_time_calculator":
   pauses = payload.get("pause_seconds", []); pauses = [float(x) for x in pauses] if isinstance(pauses, list) else []
   return {"average_seconds": round(sum(pauses)/max(len(pauses),1), 3), "sample_count": len(pauses)}
  if name.endswith("feature_extractor") or name in {"teacher_action_recognizer", "interaction_quality_analyzer"}:
   require_text({"text": text}, "text"); return {"features": {"question": text.count("？") + text.count("?"),
    "evidence_prompt": keyword_score(text, ("依据", "证据", "为什么")), "feedback": keyword_score(text, ("反馈", "很好", "再想"))}, "candidate_only": True}
  if name in {"classroom_event_detector", "event_trigger_evaluator"}:
   score = keyword_score(text, ("沉默", "争论", "错误", "偏离", "困惑")); return {"triggered": score > 0, "confidence": score, "candidate_only": True}
  if name in {"judgment_candidate_generator", "student_state_estimator", "phase_classifier"}:
   return {"label": str(payload.get("candidate", "needs_evidence")), "confidence": .5, "candidate_only": True}
  if name in {"judgment_evidence_validator", "observation_evidence_validator", "control_command_validator"}:
   refs = payload.get("evidence_refs", []); return {"valid": isinstance(refs, list) and bool(refs), "reason": "evidence_required" if not refs else "ok"}
  if name == "retry_counter":
   count = int(payload.get("count", 0)) + 1; limit = int(payload.get("limit", 3)); return {"count": count, "limit": limit, "exhausted": count >= limit}
  if name in {"scaffold_recommender", "scaffold_message_generator"}:
   return {"scaffold": "请先描述观察到的事实，再说明判断依据。", "candidate_only": True}
  if name == "execution_controller": return {"command": str(payload.get("command", "continue")), "requires_authorization": True, "executed": False}
  if name == "pre_post_comparator":
   return {"delta": round(float(payload.get("post",0))-float(payload.get("pre",0)),4)}
  return {"result_ref": stable_ref(name, context.tenant_id, text, payload), "candidate_only": True}
 return run

def build_wf3_tools() -> tuple[RegisteredTool, ...]:
 return tuple(RegisteredTool(ToolSpec(name=n, version="1.0.0", description=f"WF3 {n}", permission="practice:assist",
  timeout_seconds=8, max_retries=1, deterministic=n not in {"virtual_student_responder", "judgment_candidate_generator", "scaffold_message_generator"}), _handler(n)) for n in WF3_TOOL_NAMES)
