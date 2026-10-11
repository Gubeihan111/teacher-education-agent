"""Finite WF2 vocabulary."""

from enum import StrEnum


class DesignStage(StrEnum):
    NEEDS_ANALYSIS = "needs_analysis"
    LEARNER_ANALYSIS = "learner_analysis"
    GOAL_DESIGN = "goal_design"
    CONTENT_DESIGN = "content_design"
    STRATEGY_DESIGN = "strategy_design"
    METHOD_DESIGN = "method_design"
    MEDIA_DESIGN = "media_design"
    TEACHING_PROCESS_DESIGN = "teaching_process_design"
    ASSESSMENT_DESIGN = "assessment_design"
    ALIGNMENT_CHECK = "alignment_check"
    REVISION = "revision"

