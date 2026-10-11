"""learning_session entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningSessionEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

