"""WF2 detailed instructional-design graph."""
from ..detailed import build_detailed_graph
from ..manifests import WF2 as DEFINITION
from .state import WF2State
def build_graph(**kwargs: object) -> object: return build_detailed_graph(DEFINITION,state_schema=WF2State,**kwargs)
