"""Top-level composition without sharing workflow-internal State."""
from dataclasses import dataclass
from collections.abc import Callable
from teacher_education_agent.tools import ToolRegistry, build_default_tool_registry
from .registry import WORKFLOW_FACTORIES
@dataclass(frozen=True, slots=True)
class WorkflowApplication:
    tools: ToolRegistry
    workflow_factories: dict[str, Callable[..., object]]
def build_application() -> WorkflowApplication:
    return WorkflowApplication(build_default_tool_registry(), dict(WORKFLOW_FACTORIES))
