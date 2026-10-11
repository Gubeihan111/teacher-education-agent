"""WF1 CR-SDL v3 detailed graph: 52 source nodes."""
from ..detailed import build_detailed_graph
from ..manifests import WF1 as DEFINITION
from .state import WF1State
def build_graph(**kwargs: object) -> object: return build_detailed_graph(DEFINITION,state_schema=WF1State,**kwargs)
