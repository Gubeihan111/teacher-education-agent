"""learning_session repository ports."""

from typing import Protocol


class LearningSessionRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

