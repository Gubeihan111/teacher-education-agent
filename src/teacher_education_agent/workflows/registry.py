"""Workflow factories exposed through stable names."""
from collections.abc import Callable
from .wf1_cr_sdl_v3.graph import build_graph as build_wf1
from .wf2_instructional_design_v1.graph import build_graph as build_wf2
from .wf3_teaching_implementation_judgment_v1.graph import build_graph as build_wf3
from .wf4_reflection_transfer_v1.graph import build_graph as build_wf4
WORKFLOW_FACTORIES: dict[str, Callable[..., object]] = {"wf1_cr_sdl_v3": build_wf1, "wf2_instructional_design_v1": build_wf2, "wf3_teaching_implementation_judgment_v1": build_wf3, "wf4_reflection_transfer_v1": build_wf4}
def get_workflow_factory(name: str) -> Callable[..., object]:
    try: return WORKFLOW_FACTORIES[name]
    except KeyError as exc: raise KeyError(f"unknown workflow: {name}") from exc
