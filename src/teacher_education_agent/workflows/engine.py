"""Small LangGraph assembly layer with bounded, deterministic routing."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, TypedDict
from teacher_education_agent.tools.contracts import ToolContext
from teacher_education_agent.tools.registry import ToolRegistry

class WorkflowState(TypedDict, total=False):
    thread_id: str
    status: str
    current_stage: str
    stage_index: int
    loop_count: int
    loop_limit: int
    needs_revision: bool
    needs_human_review: bool
    pending_interrupt: str | None
    artifacts: dict[str, Any]

@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    name: str
    stages: tuple[str, ...]
    review_after: frozenset[str] = frozenset()
    loop_limit: int = 3
    tool_plan: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.stages or len(set(self.stages)) != len(self.stages):
            raise ValueError(f"{self.name}: stages must be non-empty and unique")
        if not self.review_after.issubset(self.stages):
            raise ValueError(f"{self.name}: review stage is unknown")
        if self.loop_limit < 0: raise ValueError("loop_limit must be non-negative")
        if not set(self.tool_plan).issubset(self.stages): raise ValueError(f"{self.name}: tool plan contains unknown stage")

def _node(stage: str, tool_names: tuple[str, ...], tools: ToolRegistry | None,
          context: ToolContext | None) -> Callable[[Mapping[str, Any]], Any]:
    async def run(state: Mapping[str, Any]) -> dict[str, Any]:
        requested = bool(state.get("needs_revision", False))
        count = int(state.get("loop_count", 0)) + (1 if requested else 0)
        artifacts = dict(state.get("artifacts", {}))
        if tools is not None and context is not None:
            for tool_name in tool_names:
                result = await tools.invoke(tool_name, state, context)
                artifacts[tool_name] = {"status": result.status.value, "data": dict(result.data),
                    "evidence_refs": list(result.evidence_refs), "warnings": list(result.warnings)}
        return {"current_stage": stage, "stage_index": int(state.get("stage_index", -1)) + 1,
                "status": "running", "loop_count": count,
                "loop_limit": int(state.get("loop_limit", 3)), "artifacts": artifacts}
    return run

def _review_route(state: Mapping[str, Any]) -> str:
    if bool(state.get("needs_human_review", False)):
        return "human_review"
    if bool(state.get("needs_revision", False)) and int(state.get("loop_count", 0)) < int(state.get("loop_limit", 3)):
        return "retry"
    return "continue"

def _human_review(state: Mapping[str, Any]) -> dict[str, Any]:
    from langgraph.types import interrupt
    reason = str(state.get("pending_interrupt") or "human_review_required")
    decision = interrupt({"reason": reason, "current_stage": state.get("current_stage")})
    return {"status": "running", "pending_interrupt": None,
            "artifacts": {**dict(state.get("artifacts", {})), "human_review": decision}}

def build_langgraph(definition: WorkflowDefinition, *, tools: ToolRegistry | None = None,
                    context: ToolContext | None = None, checkpointer: object | None = None,
                    state_schema: type = WorkflowState) -> object:
    """Build a graph lazily so importing the package does not require LangGraph."""
    definition.validate()
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:
        raise RuntimeError("langgraph is required to compile workflow graphs") from exc
    graph = StateGraph(state_schema)
    for stage in definition.stages: graph.add_node(stage, _node(stage, definition.tool_plan.get(stage, ()), tools, context))
    graph.add_node("human_review", _human_review)
    graph.add_edge(START, definition.stages[0])
    for left, right in zip(definition.stages, definition.stages[1:]):
        if left in definition.review_after:
            graph.add_conditional_edges(left, _review_route, {"retry": left, "continue": right, "human_review": "human_review"})
        else:
            graph.add_edge(left, right)
    graph.add_edge("human_review", END)
    graph.add_edge(definition.stages[-1], END)
    return graph.compile(checkpointer=checkpointer)
