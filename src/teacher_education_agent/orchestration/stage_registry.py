"""Registry of the four finite teacher-growth stages."""

from enum import StrEnum


class GrowthStage(StrEnum):
    LEARNING = "wf1_cr_sdl_v3"
    INSTRUCTIONAL_DESIGN = "wf2_instructional_design_v1"
    IMPLEMENTATION_JUDGMENT = "wf3_teaching_implementation_judgment_v1"
    REFLECTION_TRANSFER = "wf4_reflection_transfer_v1"

