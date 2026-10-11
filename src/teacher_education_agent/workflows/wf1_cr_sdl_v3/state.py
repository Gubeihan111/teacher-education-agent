"""Minimal internal state for WF1; never shared across workflows."""

from typing import Any, NotRequired, TypedDict


class WF1State(TypedDict):
    thread_id: str
    status: str
    stage_index: int
    session_status: str
    current_stage: str
    iteration_count: int
    pending_interrupt: NotRequired[str | None]
    learner_id: str
    learning_task_ref: str
    learner_statement: str
    baseline_evidence_refs: list[str]
    goal: NotRequired[str]
    bloom_target: NotRequired[str]
    solo_target: NotRequired[str]
    question: NotRequired[str]
    conflict_type: NotRequired[str]
    cci: NotRequired[float]
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
