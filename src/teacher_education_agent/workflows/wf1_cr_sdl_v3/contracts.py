"""WF1 boundary contract placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WF1Input:
    learner_id: str


@dataclass(frozen=True, slots=True)
class WF1Output:
    evidence_package_ref: str

