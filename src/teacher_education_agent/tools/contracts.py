"""Stable contracts shared by every workflow tool.

Tools produce structured candidate evidence or execute an explicitly supplied
port. They never decide workflow routes, permissions, transactions, terminal
states, or formal scores.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Awaitable, Callable, Mapping, Protocol


class ToolStatus(StrEnum):
    SUCCESS = "success"
    DEGRADED = "degraded"
    REJECTED = "rejected"
    FAILED = "failed"


class ToolErrorKind(StrEnum):
    INVALID_INPUT = "invalid_input"
    FORBIDDEN = "forbidden"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    TIMEOUT = "timeout"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    version: str
    description: str
    permission: str | None = None
    timeout_seconds: float = 5.0
    max_retries: int = 0
    deterministic: bool = True
    output_schema: str = "CandidateEvidence"


@dataclass(frozen=True, slots=True)
class ToolContext:
    tenant_id: str
    actor_id: str
    correlation_id: str
    permissions: frozenset[str] = frozenset()
    services: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolError:
    code: str
    kind: ToolErrorKind
    message: str
    retryable: bool = False


@dataclass(frozen=True, slots=True)
class ToolResult:
    tool_name: str
    tool_version: str
    status: ToolStatus
    data: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    error: ToolError | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status in {ToolStatus.SUCCESS, ToolStatus.DEGRADED}


ToolHandler = Callable[
    [Mapping[str, Any], ToolContext],
    Mapping[str, Any] | Awaitable[Mapping[str, Any]],
]


class ToolPort(Protocol):
    spec: ToolSpec

    async def invoke(self, payload: Mapping[str, Any], context: ToolContext) -> ToolResult:
        """Execute one bounded tool call and return a serializable result."""

