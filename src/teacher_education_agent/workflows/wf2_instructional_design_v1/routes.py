"""Deterministic WF2 routes."""

from enum import StrEnum


class WF2Route(StrEnum):
    CONTINUE = "continue"
    REVISE = "revise"
    INTERRUPT = "interrupt"
    HUMAN_REVIEW = "human_review"
    COMPLETE = "complete"
    TIMEOUT = "timeout"

