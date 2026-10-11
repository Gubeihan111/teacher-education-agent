"""Composition root for all workflow tools."""
from dataclasses import replace
from .registry import ToolRegistry
from .registry import RegisteredTool
from .wf1_learning import build_wf1_tools
from .wf2_design import build_wf2_tools
from .wf3_implementation import build_wf3_tools
from .wf4_reflection import build_wf4_tools

def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for scope, factory in (("wf1", build_wf1_tools), ("wf2", build_wf2_tools),
                           ("wf3", build_wf3_tools), ("wf4", build_wf4_tools)):
        for tool in factory():
            registry.register(RegisteredTool(replace(tool.spec, name=f"{scope}.{tool.spec.name}"), tool.handler))
    return registry
