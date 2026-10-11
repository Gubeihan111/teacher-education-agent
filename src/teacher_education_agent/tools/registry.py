"""Version-aware tool registry and bounded invocation wrapper."""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass
from typing import Iterable, Mapping

from .contracts import (
    ToolContext,
    ToolError,
    ToolErrorKind,
    ToolHandler,
    ToolPort,
    ToolResult,
    ToolSpec,
    ToolStatus,
)


@dataclass(slots=True)
class RegisteredTool:
    spec: ToolSpec
    handler: ToolHandler

    async def invoke(self, payload: Mapping[str, object], context: ToolContext) -> ToolResult:
        if self.spec.permission and self.spec.permission not in context.permissions:
            return ToolResult(
                tool_name=self.spec.name,
                tool_version=self.spec.version,
                status=ToolStatus.REJECTED,
                error=ToolError(
                    code="tool_permission_denied",
                    kind=ToolErrorKind.FORBIDDEN,
                    message=f"missing permission: {self.spec.permission}",
                ),
            )

        attempts = self.spec.max_retries + 1
        for attempt in range(1, attempts + 1):
            try:
                value = self.handler(payload, context)
                if inspect.isawaitable(value):
                    value = await asyncio.wait_for(value, timeout=self.spec.timeout_seconds)
                if not isinstance(value, Mapping):
                    raise TypeError("tool handler must return a mapping")
                status = ToolStatus(str(value.get("_status", ToolStatus.SUCCESS)))
                data = {key: item for key, item in value.items() if not key.startswith("_")}
                return ToolResult(
                    tool_name=self.spec.name,
                    tool_version=self.spec.version,
                    status=status,
                    data=data,
                    evidence_refs=tuple(value.get("_evidence_refs", ())),
                    warnings=tuple(value.get("_warnings", ())),
                    metadata={"attempt": attempt, "correlation_id": context.correlation_id},
                )
            except asyncio.TimeoutError:
                if attempt == attempts:
                    return self._failure("tool_timeout", ToolErrorKind.TIMEOUT, True, attempt)
            except (KeyError, TypeError, ValueError) as exc:
                return self._failure(
                    "tool_invalid_input", ToolErrorKind.INVALID_INPUT, False, attempt, str(exc)
                )
            except Exception:
                if attempt == attempts:
                    return self._failure(
                        "tool_dependency_failed",
                        ToolErrorKind.DEPENDENCY_UNAVAILABLE,
                        True,
                        attempt,
                    )
        raise RuntimeError("unreachable tool invocation state")

    def _failure(
        self,
        code: str,
        kind: ToolErrorKind,
        retryable: bool,
        attempt: int,
        message: str | None = None,
    ) -> ToolResult:
        return ToolResult(
            tool_name=self.spec.name,
            tool_version=self.spec.version,
            status=ToolStatus.FAILED,
            error=ToolError(
                code=code,
                kind=kind,
                message=message or code,
                retryable=retryable,
            ),
            metadata={"attempt": attempt},
        )


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolPort] = {}

    def register(self, tool: ToolPort, *, replace: bool = False) -> None:
        if tool.spec.name in self._tools and not replace:
            raise ValueError(f"tool already registered: {tool.spec.name}")
        self._tools[tool.spec.name] = tool

    def register_many(self, tools: Iterable[ToolPort], *, replace: bool = False) -> None:
        for tool in tools:
            self.register(tool, replace=replace)

    def get(self, name: str) -> ToolPort:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    async def invoke(
        self,
        name: str,
        payload: Mapping[str, object],
        context: ToolContext,
    ) -> ToolResult:
        return await self.get(name).invoke(payload, context)

    def specs(self) -> tuple[ToolSpec, ...]:
        return tuple(tool.spec for tool in self._tools.values())

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)

