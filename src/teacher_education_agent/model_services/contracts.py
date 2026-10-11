"""Provider-neutral model contracts."""
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

@dataclass(frozen=True, slots=True)
class ModelRequest:
    messages: Sequence[Mapping[str, str]]
    task_type: str
    require_json: bool = True
    temperature: float = 0.0

@dataclass(frozen=True, slots=True)
class ModelResponse:
    provider: str
    model: str
    content: str
    parsed: Mapping[str, Any] | None = None


class ModelService(Protocol):
    async def complete(self, request: ModelRequest) -> ModelResponse: ...
