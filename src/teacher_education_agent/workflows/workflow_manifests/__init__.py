"""Per-workflow manifests for parallel team development."""
from .wf1_manifest import WF1
from .wf2_manifest import WF2
from .wf3_manifest import WF3
from .wf4_manifest import WF4
DETAILED_WORKFLOWS={item.name:item for item in (WF1,WF2,WF3,WF4)}
__all__=["WF1","WF2","WF3","WF4","DETAILED_WORKFLOWS"]
