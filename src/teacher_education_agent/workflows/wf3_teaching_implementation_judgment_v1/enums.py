"""Finite WF3 state, scaffold, control and judgment vocabulary."""

from enum import StrEnum


class GrowthState(StrEnum):
    UNDER_CHALLENGED = "UNDER_CHALLENGED"
    OPTIMAL = "OPTIMAL"
    AT_RISK = "AT_RISK"
    OVERLOADED = "OVERLOADED"
    UNCERTAIN = "UNCERTAIN"


class ImmediateScaffoldLevel(StrEnum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class ControlState(StrEnum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"


class JudgmentStep(StrEnum):
    J1 = "J1"
    J2 = "J2"
    J3 = "J3"
    J4 = "J4"

