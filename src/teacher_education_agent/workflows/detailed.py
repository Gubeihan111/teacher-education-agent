"""Detailed graph builder: every source-diagram node is a distinct LangGraph node."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping
from teacher_education_agent.tools import ToolContext, ToolRegistry

@dataclass(frozen=True, slots=True)
class NodeSpec:
    source_id: str
    name: str
    tools: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    source: str = "diagram"

@dataclass(frozen=True, slots=True)
class RouteSpec:
    source: str
    outcomes: Mapping[str, str]
    default: str
    decision_key: str = "route_decisions"

@dataclass(frozen=True, slots=True)
class DetailedDefinition:
    name: str
    nodes: tuple[NodeSpec, ...]
    routes: tuple[RouteSpec, ...] = ()
    max_visits: int = 4
    extra_edges: tuple[tuple[str, str], ...] = ()
    global_routes: Mapping[str, str] = field(default_factory=dict)
    def validate(self) -> None:
        ids=[n.source_id for n in self.nodes]
        if len(ids)!=len(set(ids)): raise ValueError(f"{self.name}: duplicate node")
        known=set(ids)
        for route in self.routes:
            targets=set(route.outcomes.values())|{route.default}
            if route.source not in known or not targets.issubset(known|{"__end__"}): raise ValueError(f"{self.name}: invalid route {route.source}")
        if not set(self.global_routes.values()).issubset(known): raise ValueError(f"{self.name}: invalid global route")

def build_detailed_graph(definition: DetailedDefinition, *, state_schema: type, tools: ToolRegistry | None=None,
                         context: ToolContext | None=None, checkpointer: object | None=None) -> object:
    definition.validate()
    try:
        from langgraph.graph import END, START, StateGraph
        from langgraph.types import interrupt
    except ImportError as exc: raise RuntimeError("langgraph is required") from exc
    graph=StateGraph(state_schema); route_sources={r.source for r in definition.routes}
    def make_node(spec: NodeSpec):
        async def node(state: Mapping[str, Any]):
            visits=dict(state.get("node_visits",{})); visits[spec.source_id]=visits.get(spec.source_id,0)+1
            if visits[spec.source_id]>definition.max_visits:
                decision=interrupt({"reason":"node_visit_limit","node":spec.source_id})
                return {"pending_interrupt":None,"human_decision":decision,"node_visits":visits}
            artifacts=dict(state.get("artifacts",{}))
            if spec.source_id.endswith("HUMAN_REVIEW") or spec.source_id=="pause_or_manual_help":
                decision=interrupt({"reason":"human_review","node":spec.source_id,"thread_id":state.get("thread_id")})
                artifacts[f"{spec.source_id}:decision"]=decision
            if tools and context:
                for tool_name in spec.tools:
                    result=await tools.invoke(tool_name,state,context)
                    artifacts[f"{spec.source_id}:{tool_name}"]={"status":result.status.value,"data":dict(result.data),"warnings":list(result.warnings)}
            return {"current_node":spec.source_id,"current_stage":spec.source_id,"node_visits":visits,"artifacts":artifacts}
        return node
    for spec in definition.nodes: graph.add_node(spec.source_id,make_node(spec))
    graph.add_edge(START,definition.nodes[0].source_id)
    route_map={r.source:r for r in definition.routes}
    for left,right in zip(definition.nodes,definition.nodes[1:]):
        if left.source_id in route_sources:
            route=route_map[left.source_id]
            def choose(state, route=route):
                event=str(state.get("global_event", ""))
                if event in definition.global_routes: return f"__global__:{event}"
                decisions=state.get(route.decision_key,{})
                value=str(decisions.get(route.source,"")) if isinstance(decisions,Mapping) else ""
                return value if value in route.outcomes else "__default__"
            destinations={key:(END if target=="__end__" else target) for key,target in route.outcomes.items()}
            destinations["__default__"]=END if route.default=="__end__" else route.default
            destinations.update({f"__global__:{key}":value for key,value in definition.global_routes.items()})
            graph.add_conditional_edges(left.source_id,choose,destinations)
        elif definition.global_routes:
            def choose_global(state, next_id=right.source_id):
                event=str(state.get("global_event", "")); return f"__global__:{event}" if event in definition.global_routes else "__next__"
            graph.add_conditional_edges(left.source_id,choose_global,{"__next__":right.source_id,**{f"__global__:{key}":value for key,value in definition.global_routes.items()}})
        else: graph.add_edge(left.source_id,right.source_id)
    for left,right in definition.extra_edges: graph.add_edge(left,right)
    if definition.nodes[-1].source_id not in route_sources: graph.add_edge(definition.nodes[-1].source_id,END)
    return graph.compile(checkpointer=checkpointer)
