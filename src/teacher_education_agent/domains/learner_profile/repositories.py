"""learner_profile repository ports."""

from typing import Protocol


class LearnerProfileRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

