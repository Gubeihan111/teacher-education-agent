"""Deterministic WF4 routes."""

from enum import StrEnum


class WF4Route(StrEnum):
    CONTINUE = "continue"
    VERIFY_PRACTICE = "verify_practice"
    RETRY = "retry"
    INTERRUPT = "interrupt"
    HUMAN_REVIEW = "human_review"
    COMPLETE = "complete"
    TIMEOUT = "timeout"

