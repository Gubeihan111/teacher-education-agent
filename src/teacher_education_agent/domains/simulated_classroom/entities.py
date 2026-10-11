"""simulated_classroom entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulatedClassroomEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

