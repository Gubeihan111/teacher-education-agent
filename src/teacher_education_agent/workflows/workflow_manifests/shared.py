"""Shared manifest construction helpers."""
from ..detailed import NodeSpec

def nodes(text: str, tools: dict[str, tuple[str, ...]] | None = None) -> tuple[NodeSpec, ...]:
    tools=tools or {}; result=[]
    for row in text.strip().splitlines():
        source_id,name=(part.strip() for part in row.split("|",1))
        source="supplement" if source_id.startswith("X") else "diagram"
        result.append(NodeSpec(source_id,name,tools.get(source_id,()),("state",),(f"{source_id}_result",),source))
    return tuple(result)
