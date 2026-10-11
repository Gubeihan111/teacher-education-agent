"""notification repository ports."""

from typing import Protocol


class NotificationRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

