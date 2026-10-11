"""Deterministic route vocabulary for WF1."""

from enum import StrEnum


class WF1Route(StrEnum):
    CONTINUE = "continue"
    REGULATE = "regulate"
    REASSESS = "reassess"
    INTERRUPT = "interrupt"
    HUMAN_REVIEW = "human_review"
    COMPLETE = "complete"
    TIMEOUT = "timeout"

