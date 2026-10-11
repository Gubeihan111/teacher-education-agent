"""Finite WF4 vocabulary."""

from enum import StrEnum


class ReflectionScaffold(StrEnum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"


class ReflectionDimension(StrEnum):
    DESCRIPTION = "description"
    EVALUATION = "evaluation"
    ARGUMENTATION = "argumentation"
    ALTERNATIVE = "alternative"
    SELF_CONNECTION = "self_connection"


class TransferLevel(StrEnum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"

