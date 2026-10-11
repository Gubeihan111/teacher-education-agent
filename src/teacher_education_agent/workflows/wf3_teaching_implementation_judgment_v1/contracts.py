"""WF3 boundary contract placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WF3Input:
    teaching_design_package_ref: str


@dataclass(frozen=True, slots=True)
class TeachingJudgmentEvidencePackage:
    package_id: str


@dataclass(frozen=True, slots=True)
class ImmediateImprovementTarget:
    target_id: str


@dataclass(frozen=True, slots=True)
class RetryResult:
    result_id: str


@dataclass(frozen=True, slots=True)
class NextStageRecommendation:
    recommendation: str

