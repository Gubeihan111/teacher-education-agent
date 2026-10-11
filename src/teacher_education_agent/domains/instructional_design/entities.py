"""instructional_design entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstructionalDesignEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

