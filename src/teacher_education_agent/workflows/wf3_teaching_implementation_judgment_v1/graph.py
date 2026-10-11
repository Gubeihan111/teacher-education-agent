"""WF3 detailed teaching implementation and judgment graph."""
from ..detailed import build_detailed_graph
from ..manifests import WF3 as DEFINITION
from .state import WF3State
def build_graph(**kwargs: object) -> object: return build_detailed_graph(DEFINITION,state_schema=WF3State,**kwargs)
