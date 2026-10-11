"""learning_goal entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningGoalEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

