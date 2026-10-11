"""growth_profile entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GrowthProfileEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

