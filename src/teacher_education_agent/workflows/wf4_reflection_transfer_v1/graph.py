"""WF4 detailed reflection, validation, transfer and inquiry graph."""
from ..detailed import build_detailed_graph
from ..manifests import WF4 as DEFINITION
from .state import WF4State
def build_graph(**kwargs: object) -> object: return build_detailed_graph(DEFINITION,state_schema=WF4State,**kwargs)
