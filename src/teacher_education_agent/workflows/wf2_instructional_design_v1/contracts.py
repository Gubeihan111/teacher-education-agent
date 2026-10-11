"""WF2 input/output contract placeholders."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WF2Input:
    learning_outcome_ref: str


@dataclass(frozen=True, slots=True)
class TeachingDesignPackage:
    package_id: str
    schema_version: str = "pending"

