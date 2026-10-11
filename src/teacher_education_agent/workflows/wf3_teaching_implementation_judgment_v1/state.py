"""Minimal internal WF3 state; never exported to WF4."""

from typing import Any, NotRequired, TypedDict


class WF3State(TypedDict):
    thread_id: str
    status: str
    current_stage: str
    stage_index: int
    current_subgraph: str
    cycle_count: int
    pending_interrupt: NotRequired[str | None]
    owner_id: str
    design_ref: str
    task_config: dict[str, Any]
    scenario_config: dict[str, Any]
    classroom_state: dict[str, Any]
    timeline_ref: NotRequired[str]
    detected_events: list[dict[str, Any]]
    judgment_candidates: list[dict[str, Any]]
    scaffold_history: list[dict[str, Any]]
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
