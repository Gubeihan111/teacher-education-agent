"""Agent protocol placeholders."""

from typing import Protocol


class AgentPort(Protocol):
    """May propose candidate evidence but cannot own workflow routing."""

    ...

