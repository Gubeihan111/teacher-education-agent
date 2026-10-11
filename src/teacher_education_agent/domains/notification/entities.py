"""notification entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotificationEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

