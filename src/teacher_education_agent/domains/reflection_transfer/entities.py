"""reflection_transfer entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReflectionTransferEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

