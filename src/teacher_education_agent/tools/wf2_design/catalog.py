"""WF2 instructional-design tools. Generators return candidates for teacher review."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..contracts import ToolContext, ToolSpec, ToolStatus
from ..foundation import clamp, overlap_score, require_text, stable_ref
from ..registry import RegisteredTool


def _service(name: str, payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any] | None:
    service = context.services.get(name)
    return service(payload, context) if service is not None else None


def _handler(name: str):
    def run(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
        external = _service(name, payload, context)
        if external is not None:
            return external
        text = str(payload.get("text") or payload.get("goal") or payload.get("content") or "").strip()
        if name in {"material_search", "knowledge_retrieval"}:
            return {"candidates": [], "query": text, "_status": ToolStatus.DEGRADED,
                    "_warnings": (f"{name}_service_unavailable",)}
        if name == "learner_diagnosis":
            require_text(payload, "text")
            return {"diagnosis": {"prior_knowledge": clamp(len(text) / 400),
                    "support_needed": any(k in text for k in ("困难", "不会", "薄弱"))}, "candidate_only": True}
        if name == "goal_validator":
            goal = require_text(payload, "goal")
            observable = any(k in goal for k in ("说明", "分析", "设计", "评价", "运用", "完成"))
            return {"valid": observable and len(goal) >= 8, "observable": observable,
                    "measurable": any(k in goal for k in ("依据", "标准", "至少", "%")), "candidate_only": True}
        if name in {"automatic_evaluator", "alignment_validator", "design_effect_analyzer"}:
            goal = str(payload.get("goal", "")); content = str(payload.get("content", text))
            score = overlap_score(goal, content)
            return {"alignment_score": score, "passed": score >= .2,
                    "issues": [] if score >= .2 else ["目标与内容的关键词证据不足"], "candidate_only": True}
        if name == "media_recommender":
            return {"candidates": [{"media": "diagram", "reason": "呈现概念关系"},
                    {"media": "case", "reason": "支持情境化判断"}], "candidate_only": True}
        if name in {"exercise_generator", "personalized_assignment_recommender"}:
            goal = require_text(payload, "goal")
            return {"items": [{"prompt": f"请用证据完成并解释：{goal}", "type": "constructed_response"}],
                    "answer_withheld": True, "candidate_only": True}
        if name == "needs_analysis":
            require_text(payload, "text")
            return {"needs": [s.strip() for s in text.replace("；", "。").split("。") if s.strip()][:8],
                    "candidate_only": True}
        if name == "learning_data_analysis":
            return {"signals": dict(payload.get("signals", {})) if isinstance(payload.get("signals"), Mapping) else {},
                    "candidate_only": True}
        if name == "goal_generator":
            require_text(payload, "text")
            return {"goals": [f"学习者能够分析{text[:80]}并以证据说明判断"], "candidate_only": True}
        if name in {"knowledge_organization", "content_generator", "review_summarizer"}:
            require_text(payload, "text")
            return {"outline": [s.strip() for s in text.splitlines() if s.strip()][:12], "candidate_only": True}
        if name == "strategy_recommender":
            return {"candidates": ["案例比较", "证据提问", "同伴互评"], "candidate_only": True}
        return {"result_ref": stable_ref(name, context.tenant_id, text), "candidate_only": True}
    return run


_NAMES = (
    "needs_analysis", "material_search", "learning_data_analysis", "learner_diagnosis",
    "goal_generator", "goal_validator", "knowledge_retrieval", "knowledge_organization",
    "content_generator", "strategy_recommender", "media_recommender", "review_summarizer",
    "exercise_generator", "personalized_assignment_recommender", "automatic_evaluator",
    "design_effect_analyzer", "alignment_validator",
)


def build_wf2_tools() -> tuple[RegisteredTool, ...]:
    return tuple(RegisteredTool(ToolSpec(name=n, version="1.0.0", description=f"WF2 {n}",
        permission="design:assist", timeout_seconds=8, max_retries=1,
        deterministic=n not in {"goal_generator", "content_generator", "exercise_generator"}), _handler(n)) for n in _NAMES)
