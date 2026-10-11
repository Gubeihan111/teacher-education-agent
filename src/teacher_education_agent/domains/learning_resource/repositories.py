"""learning_resource repository ports."""

from typing import Protocol


class LearningResourceRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

