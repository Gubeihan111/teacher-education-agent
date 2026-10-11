"""WF1 tool implementations derived from the CR-SDL v3 specification."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..contracts import ToolContext, ToolSpec, ToolStatus
from ..foundation import clamp, keyword_score, overlap_score, require_text, stable_ref
from ..registry import RegisteredTool


CONFLICT_TYPES: dict[str, tuple[str, tuple[str, ...]]] = {
    "fact_conflict": ("knowledge", ("事实", "数据", "与资料不符", "记错")),
    "concept_conflict": ("knowledge", ("概念", "定义", "混淆", "边界")),
    "collaboration_conflict": ("reasoning", ("同伴", "协作", "分歧", "合作")),
    "reasoning_conflict": ("reasoning", ("推理", "因此", "矛盾", "依据")),
    "control_conflict": ("reasoning", ("控制", "选择", "依赖", "替我")),
    "meta_knowledge_conflict": ("metacognition", ("我知道", "我不懂", "知识缺口")),
    "meta_experience_conflict": ("metacognition", ("困惑", "焦虑", "意外", "不确定")),
    "meta_monitoring_conflict": ("metacognition", ("检查", "监控", "反思", "调整")),
}


def _service_or_degraded(
    name: str,
    payload: Mapping[str, Any],
    context: ToolContext,
    *,
    fallback: Mapping[str, Any],
) -> Mapping[str, Any]:
    service = context.services.get(name)
    if service is None:
        return {**fallback, "_status": ToolStatus.DEGRADED, "_warnings": (f"{name}_unavailable",)}
    return service(payload, context)


def _learning_context(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    return _service_or_degraded(
        "learning_context",
        payload,
        context,
        fallback={
            "task_ref": str(payload.get("task_ref", "")),
            "profile_summary": {},
            "context_complete": bool(payload.get("task_ref")),
        },
    )


def _readiness(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    statement = require_text(payload, "learner_statement")
    evidence = str(payload.get("baseline_evidence", "")).strip()
    dimensions = {
        "need_clarity": clamp(len(statement) / 120),
        "prior_evidence": 1.0 if evidence else 0.0,
        "motivation_signal": keyword_score(statement, ("想", "需要", "目标", "希望")),
        "condition_awareness": keyword_score(statement, ("时间", "资源", "困难", "限制")),
    }
    score = round(sum(dimensions.values()) / len(dimensions), 4)
    return {
        "readiness_score": score,
        "dimensions": dimensions,
        "needs_more_evidence": not evidence or score < 0.45,
        "candidate_questions": ["请补充一项可验证的起点作品或作答。"] if not evidence else [],
    }


def _goal_levels(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    goal = require_text(payload, "goal")
    bloom_rules = (
        ("B6", ("创造", "设计", "创新", "生成")),
        ("B5", ("评价", "判断", "论证", "批判")),
        ("B4", ("分析", "比较", "归因", "区分")),
        ("B3", ("应用", "解决", "运用", "实践")),
        ("B2", ("理解", "解释", "概括", "说明")),
        ("B1", ("记忆", "列举", "识别", "了解")),
    )
    solo_rules = (
        ("S4", ("迁移", "抽象", "新情境", "创新")),
        ("S3", ("关联", "整合", "关系", "整体")),
        ("S2", ("多个", "多方面", "列出", "比较")),
        ("S1", ("一个", "单一", "识别")),
    )
    bloom = next((level for level, words in bloom_rules if any(w in goal for w in words)), "unknown")
    solo = next((level for level, words in solo_rules if any(w in goal for w in words)), "unknown")
    return {
        "bloom_level": bloom,
        "solo_level": solo,
        "confidence": 0.72 if bloom != "unknown" and solo != "unknown" else 0.35,
        "requires_learner_confirmation": True,
    }


def _question(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    question = require_text(payload, "question")
    scores = {
        "specificity": clamp(len(question) / 80),
        "open_endedness": 1.0 if any(word in question for word in ("为什么", "如何", "怎样")) else 0.4,
        "goal_alignment": overlap_score(question, str(payload.get("goal", ""))),
        "evidence_orientation": keyword_score(question, ("依据", "证据", "验证", "比较")),
    }
    return {
        "quality_score": round(sum(scores.values()) / len(scores), 4),
        "dimensions": scores,
        "revision_needed": min(scores.values()) < 0.25,
    }


def _resources(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    return _service_or_degraded(
        "resource_recommender",
        payload,
        context,
        fallback={"candidates": [], "allow_self_selection": True},
    )


def _feedback(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    response = require_text(payload, "learner_response")
    goal = str(payload.get("goal", ""))
    return {
        "feedback_type": "questioning",
        "message": "请指出你的结论所依据的证据，并说明它与目标的关系。",
        "goal_overlap": overlap_score(response, goal),
        "contains_direct_answer": False,
    }


def _evidence_store(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    content = require_text(payload, "content")
    source_type = str(payload.get("source_type", "learner"))
    if source_type not in {"learner", "ai", "external", "system"}:
        raise ValueError("unsupported source_type")
    ref = stable_ref("evidence", context.tenant_id, context.actor_id, content, source_type)
    service = context.services.get("evidence_store")
    if service is not None:
        return service({**payload, "evidence_ref": ref}, context)
    return {
        "evidence_ref": ref,
        "source_type": source_type,
        "ownership_valid": source_type == "learner",
        "persisted": False,
        "_status": ToolStatus.DEGRADED,
        "_evidence_refs": (ref,),
        "_warnings": ("evidence_store_unavailable",),
    }


def _detect_conflict(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    text = require_text(payload, "learner_evidence")
    signals = ("不确定", "不明白", "矛盾", "不对", "错了", "为什么", "没有头绪", "困惑")
    score = keyword_score(text, signals)
    return {
        "detected": score >= 0.125,
        "confidence": round(max(0.25, min(0.9, 0.3 + score)), 4),
        "signal_count": sum(1 for signal in signals if signal in text),
        "candidate_only": True,
    }


def _classify_conflict(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    text = require_text(payload, "learner_evidence")
    ranked = sorted(
        ((keyword_score(text, words), name, layer) for name, (layer, words) in CONFLICT_TYPES.items()),
        reverse=True,
    )
    score, conflict_type, layer = ranked[0]
    return {
        "conflict_type": conflict_type if score else "unknown",
        "conflict_layer": layer if score else "unknown",
        "confidence": round(score, 4),
        "candidate_only": True,
    }


def _calculate_cci(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    components = payload.get("components")
    if not isinstance(components, Mapping):
        raise ValueError("components must be an object")
    weights = {"cognitive": 0.25, "behavioral": 0.20, "persistence": 0.20, "uncertainty": 0.20, "tension": 0.15}
    values = {name: max(0.0, min(5.0, float(components.get(name, 0.0)))) for name in weights}
    score = round(sum(values[name] * weight for name, weight in weights.items()), 3)
    band = "insufficient" if score < 2.5 else "optimal" if score <= 3.5 else "overloaded"
    return {"cci": score, "band": band, "target": 3.0, "components": values, "formula_version": "cci-v1"}


def _strategy(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    band = str(payload.get("band", "unknown"))
    conflict_type = str(payload.get("conflict_type", "unknown"))
    service = context.services.get("strategy_repository")
    if service is not None:
        return service(payload, context)
    fallback = {
        "insufficient": "increase_challenge",
        "optimal": "maintain_minimal_scaffold",
        "overloaded": "reduce_load_then_reassess",
    }.get(band, "generic_evidence_prompt")
    return {
        "strategy_id": fallback,
        "conflict_type": conflict_type,
        "requires_reassessment": band == "overloaded",
        "_status": ToolStatus.DEGRADED,
        "_warnings": ("strategy_repository_unavailable",),
    }


def _source_verify(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    claim = require_text(payload, "claim")
    sources = payload.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    support = max((overlap_score(claim, str(item.get("text", ""))) for item in sources if isinstance(item, Mapping)), default=0.0)
    return {"support_score": support, "decision": "supported" if support >= 0.25 else "unsupported", "source_count": len(sources)}


def _rubric(payload: Mapping[str, Any], _: ToolContext) -> Mapping[str, Any]:
    evidence = require_text(payload, "evidence")
    return {
        "bloom_candidate": str(payload.get("bloom_target", "unknown")),
        "solo_candidate": str(payload.get("solo_target", "unknown")),
        "evidence_strength": round(clamp(len(evidence) / 500), 4),
        "candidate_only": True,
        "requires_formal_evaluation": True,
    }


def _profile(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    return _service_or_degraded(
        "learner_profile_repository",
        payload,
        context,
        fallback={"profile_version": None, "profile_summary": {}, "persisted": False},
    )


def _checkpoint(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    return _service_or_degraded(
        "checkpoint_store",
        payload,
        context,
        fallback={"checkpoint_ref": None, "persisted": False, "fail_closed": True},
    )


def _audit(payload: Mapping[str, Any], context: ToolContext) -> Mapping[str, Any]:
    return _service_or_degraded(
        "audit_outbox",
        payload,
        context,
        fallback={"event_ref": None, "queued": False},
    )


_DEFINITIONS = (
    ("learning_context", "读取情境、任务和画像", "context:read", 5, 2, _learning_context),
    ("readiness_assessor", "诊断学习需要与起点", "assessment:run", 6, 1, _readiness),
    ("goal_level_assessor", "分别评价Bloom与SOLO起点", "assessment:run", 8, 1, _goal_levels),
    ("question_assessor", "评价问题质量", "assessment:run", 6, 1, _question),
    ("resource_recommender", "获得资源候选", "resource:read", 8, 1, _resources),
    ("learning_feedback", "生成不代写的反馈候选", "learning:assist", 12, 1, _feedback),
    ("evidence_store", "保存证据及其归属", "evidence:write", 5, 2, _evidence_store),
    ("conflict_detector", "检测认知冲突候选", "conflict:run", 3, 1, _detect_conflict),
    ("conflict_classifier", "分类三层八类冲突", "conflict:run", 3, 1, _classify_conflict),
    ("cci_calculator", "确定性计算CCI", "conflict:run", 1, 0, _calculate_cci),
    ("strategy_repository", "检索支架策略", "strategy:read", 3, 2, _strategy),
    ("source_verifier", "核验主张与来源", "verification:run", 10, 1, _source_verify),
    ("rubric_evaluator", "形成Bloom和SOLO候选评价", "assessment:run", 8, 1, _rubric),
    ("learner_profile_repository", "访问画像版本", "profile:write", 3, 2, _profile),
    ("checkpoint_store", "保存或恢复执行位置", "checkpoint:write", 5, 2, _checkpoint),
    ("audit_outbox", "写入审计与可靠事件", "audit:write", 5, 2, _audit),
)


def build_wf1_tools() -> tuple[RegisteredTool, ...]:
    tools: list[RegisteredTool] = []
    for name, description, permission, timeout, retries, handler in _DEFINITIONS:
        tools.append(
            RegisteredTool(
                ToolSpec(
                    name=name,
                    version="1.0.0",
                    description=description,
                    permission=permission,
                    timeout_seconds=timeout,
                    max_retries=retries,
                    deterministic=name not in {"goal_level_assessor", "learning_feedback", "rubric_evaluator"},
                ),
                handler,
            )
        )
    return tuple(tools)

