"""teaching_practice entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TeachingPracticeEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

