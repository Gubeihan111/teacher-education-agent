"""professional_judgment entity placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfessionalJudgmentEntity:
    """Identity-only placeholder; business fields are pending domain review."""

    id: str

