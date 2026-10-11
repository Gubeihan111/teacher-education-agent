"""WF2 source-diagram manifest."""
from ..detailed import DetailedDefinition, RouteSpec
from .shared import nodes

ROWS="""
N1|学习需要分析
N2|学习者分析
N3|学习目标制定
N4|学习目标判断
N5|学习内容制定
N6|教学内容判断
N7|教学策略制定
N7-1|教学方法确定
N7-2|教学媒体选择
N7-3|教学过程实施
N8|授课类型判断
N7-3-1|导入新课
N7-3-2|讲授新课
N7-3-3|复习总结
N7-3-4|练习作业
N9|作业正确率判断
N10|教学评价（形成性/总结性评价）
N11|修订改进
X2.HUMAN_REVIEW|人工复核
X2.CANCELLED|取消终态
X2.EXPIRED|过期终态
X2.FAILED|失败终态
"""
TOOLS={"N1":("wf2.needs_analysis","wf2.material_search"),"N2":("wf2.learning_data_analysis","wf2.learner_diagnosis"),"N3":("wf2.goal_generator",),"N4":("wf2.goal_validator",),"N5":("wf2.knowledge_retrieval","wf2.knowledge_organization","wf2.content_generator"),"N7":("wf2.strategy_recommender",),"N7-2":("wf2.media_recommender",),"N7-3-3":("wf2.review_summarizer",),"N7-3-4":("wf2.exercise_generator","wf2.personalized_assignment_recommender"),"N10":("wf2.automatic_evaluator","wf2.design_effect_analyzer"),"N11":("wf2.alignment_validator",)}
WF2=DetailedDefinition("wf2_instructional_design_v1",nodes(ROWS,TOOLS),(
 RouteSpec("N4",{"yes":"N5","no":"N3"},"N3"),RouteSpec("N6",{"yes":"N7","no":"N5"},"N5"),
 RouteSpec("N8",{"new_lesson":"N7-3-1","review_lesson":"N7-3-3"},"N7-3-3"),RouteSpec("N7-3-1",{},"N7-3-2"),RouteSpec("N7-3-2",{},"N7-3-4"),RouteSpec("N7-3-3",{},"N7-3-4"),
 RouteSpec("N9",{"pass":"N10","fail":"N7-3-2"},"N7-3-2"),RouteSpec("N11",{},"__end__"),
 RouteSpec("X2.HUMAN_REVIEW",{},"__end__"),RouteSpec("X2.CANCELLED",{},"__end__"),RouteSpec("X2.EXPIRED",{},"__end__"),RouteSpec("X2.FAILED",{},"__end__"),
),3,global_routes={"cancel":"X2.CANCELLED","expired":"X2.EXPIRED","fatal":"X2.FAILED","help":"X2.HUMAN_REVIEW"})
