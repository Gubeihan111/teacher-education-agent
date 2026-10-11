"""identity repository ports."""

from typing import Protocol


class IdentityRepository(Protocol):
    """Persistence port; concrete storage belongs to infrastructure."""

    # TODO: define operations from approved use cases.
    ...

