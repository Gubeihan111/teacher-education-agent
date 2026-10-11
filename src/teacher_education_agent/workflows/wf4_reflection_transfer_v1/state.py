"""Minimal internal WF4 state; never reads WF3 internal State."""

from typing import Any, NotRequired, TypedDict


class WF4State(TypedDict):
    thread_id: str
    status: str
    current_stage: str
    stage_index: int
    evidence_package_ref: str
    current_subgraph: str
    iteration_count: int
    pending_interrupt: NotRequired[str | None]
    owner_id: str
    practice_record_ref: str
    reflection_text: str
    problem_candidates: list[dict[str, Any]]
    attribution_candidates: list[dict[str, Any]]
    selected_strategy: NotRequired[dict[str, Any]]
    validation_evidence_refs: list[str]
    transfer_task_ref: NotRequired[str]
    transfer_evidence_refs: list[str]
    inquiry_cycle_refs: list[str]
    stage_achievement_candidate: NotRequired[dict[str, Any]]
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
