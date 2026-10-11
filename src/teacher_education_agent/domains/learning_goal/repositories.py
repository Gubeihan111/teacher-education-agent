"""learning_goal repository ports."""

from typing import Protocol


class LearningGoalRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

