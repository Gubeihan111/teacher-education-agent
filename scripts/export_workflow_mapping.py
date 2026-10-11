"""Export the auditable source-diagram to LangGraph mapping."""
from pathlib import Path
from teacher_education_agent.workflows.manifests import DETAILED_WORKFLOWS

TARGET=Path(__file__).resolve().parents[1]/"docs"/"workflow-node-tool-route-mapping.md"
EXTRACTS=TARGET.parent/"source_extracts"

def source_io() -> dict[str, tuple[str,str]]:
    result={}
    wf1=next(EXTRACTS.glob("*LangGraph*.txt")); lines=wf1.read_text(encoding="utf-8").splitlines()
    current=None
    for line in lines:
        if line.startswith("Node ID / 名称 | "): current=line.split("|",1)[1].split("/",1)[0].strip()
        elif current and line.startswith("输入 State 键 | "):
            result[current]=(line.split("|",1)[1].strip(),result.get(current,("",""))[1])
        elif current and line.startswith("输出 State 键 | "):
            result[current]=(result.get(current,("",""))[0],line.split("|",1)[1].strip())
    for keyword,prefix,input_index in (("任务2","N",3),("任务3","N3.",3),("任务4","N4.",2)):
        source=next(p for p in EXTRACTS.glob("*.txt") if keyword in p.name and "工作流图" not in p.name)
        for line in source.read_text(encoding="utf-8").splitlines():
            parts=[part.strip() for part in line.split("|")]
            first=parts[0].split() if parts else []
            source_id=first[0] if first else ""
            if len(parts)>=5 and source_id.startswith(prefix) and any(ch.isdigit() for ch in source_id):
                result[source_id]=(parts[input_index] or "当前工作流状态",parts[-2] if keyword=="任务2" and len(parts)>=7 else parts[-1])
    result.update({
        "N4":("学习目标、学习者画像、课程要求","目标合理性判断"),
        "N6":("教学内容、学习目标、知识结构","内容适切性判断"),
        "N8":("授课类型、教学目标、教学内容","新授课或复习课路由"),
        "N9":("练习作业结果、正确率阈值","作业达标判断"),
    })
    return result

IO=source_io()
lines=["# 原图节点—LangGraph节点—工具—输入输出—路由对照表","",
"本表由代码清单生成。`diagram`表示原图节点，`supplement`表示为完整运行补充的工程节点。所有路由值均为有限枚举，未识别值走默认路由。",""]
for workflow,definition in DETAILED_WORKFLOWS.items():
    routes={route.source:route for route in definition.routes}
    lines.extend([f"## {workflow}","","| 来源 | 原图节点编号 | LangGraph节点 | 使用工具 | 输入 | 输出 | 条件路由 |","|---|---|---|---|---|---|---|"])
    for node in definition.nodes:
        route=routes.get(node.source_id)
        route_text="；".join(f"{key}→{value}" for key,value in route.outcomes.items()) if route else "顺序进入下一节点"
        if route: route_text += f"；默认→{route.default}"
        inputs,outputs=IO.get(node.source_id,("、".join(node.inputs),"、".join(node.outputs)))
        lines.append("| " + " | ".join((node.source,node.source_id,node.name,"、".join(node.tools) or "无外部工具",inputs,outputs,route_text)) + " |")
    lines.append("")
TARGET.write_text("\n".join(lines),encoding="utf-8")
print(TARGET)
