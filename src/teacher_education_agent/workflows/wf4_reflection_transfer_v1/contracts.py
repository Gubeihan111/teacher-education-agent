"""WF4 stable contract placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WF4Input:
    teaching_judgment_evidence_package_ref: str


@dataclass(frozen=True, slots=True)
class ReflectionTransferEvidencePackage:
    package_id: str


@dataclass(frozen=True, slots=True)
class NextGrowthProposal:
    proposal_id: str

