"""Minimal internal WF2 state; not a cross-workflow contract."""

from typing import Any, NotRequired, TypedDict


class WF2State(TypedDict):
    thread_id: str
    status: str
    stage_index: int
    current_stage: str
    revision_count: int
    pending_interrupt: NotRequired[str | None]
    owner_id: str
    needs_statement: str
    learner_profile_ref: NotRequired[str]
    goals: list[dict[str, Any]]
    content_outline: list[dict[str, Any]]
    strategies: list[dict[str, Any]]
    media_plan: list[dict[str, Any]]
    teaching_process: list[dict[str, Any]]
    assessment_plan: list[dict[str, Any]]
    alignment_issues: list[str]
    evidence_refs: list[str]
    loop_count: int
    loop_limit: int
    needs_revision: bool
    needs_human_review: bool
    artifacts: dict[str, Any]
    current_node: str
    node_visits: dict[str, int]
    route_decisions: dict[str, str]
    global_event: NotRequired[str]
    human_decision: NotRequired[Any]
