"""Finite WF1 vocabulary."""

from enum import StrEnum


class BloomLevel(StrEnum):
    B1 = "remember"
    B2 = "understand"
    B3 = "apply"
    B4 = "analyze"
    B5 = "evaluate"
    B6 = "create"


class SoloLevel(StrEnum):
    S0 = "prestructural"
    S1 = "unistructural"
    S2 = "multistructural"
    S3 = "relational"
    S4 = "extended_abstract"


class ConflictBand(StrEnum):
    INSUFFICIENT = "insufficient"
    OPTIMAL = "optimal"
    OVERLOADED = "overloaded"

