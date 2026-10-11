"""Deterministic WF3 routes."""

from enum import StrEnum


class WF3Route(StrEnum):
    CONTINUE = "continue"
    ADJUST_SCAFFOLD = "adjust_scaffold"
    REPLAY = "replay"
    RETEACH = "reteach"
    INTERRUPT = "interrupt"
    HUMAN_REVIEW = "human_review"
    COMPLETE = "complete"
    TIMEOUT = "timeout"

