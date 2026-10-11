"""Versioned API router."""
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from pathlib import Path
import re
from pydantic import BaseModel, Field
from teacher_education_agent.tools import ToolContext
router=APIRouter(prefix="/api/v1")
class StartWorkflowRequest(BaseModel):
    thread_id: str = Field(min_length=1,max_length=128); state: dict = Field(default_factory=dict)
class ResumeWorkflowRequest(BaseModel):
    thread_id: str = Field(min_length=1,max_length=128); decision: dict
def workflow_permissions(name: str) -> frozenset[str]:
    if name == "wf1_cr_sdl_v3": return frozenset({"context:read","assessment:run","resource:read","learning:assist","evidence:write","conflict:run","strategy:read","verification:run","profile:write","checkpoint:write","audit:write"})
    if name == "wf2_instructional_design_v1": return frozenset({"design:assist"})
    if name == "wf3_teaching_implementation_judgment_v1": return frozenset({"practice:assist"})
    if name == "wf4_reflection_transfer_v1": return frozenset({"reflection:assist"})
    return frozenset()
@router.get("/health")
async def health(request: Request):
    return {"status":"ok","workflows":sorted(request.app.state.container.workflows)}
@router.post("/knowledge/ingest")
async def ingest_knowledge(request: Request, file: UploadFile=File(...)):
    filename=re.sub(r"[^0-9A-Za-z._\-\u4e00-\u9fff]","_",file.filename or "source")
    suffix=Path(filename).suffix.lower()
    if suffix not in {".docx",".pdf",".vsdx",".txt",".md"}: raise HTTPException(415,"unsupported source type")
    target=Path("data/knowledge/sources")/filename; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(await file.read())
    return await request.app.state.container.ingestor.ingest(target,{"uploaded_filename":filename})
@router.post("/workflows/{workflow_name}/start")
async def start_workflow(workflow_name: str, body: StartWorkflowRequest, request: Request):
    container=request.app.state.container
    factory=container.workflows.get(workflow_name)
    if factory is None: raise HTTPException(404,"unknown workflow")
    context=ToolContext("default", "api-user", body.thread_id, workflow_permissions(workflow_name), container.services)
    graph=factory(tools=container.tools, context=context, checkpointer=container.checkpointer)
    state={**body.state,"thread_id":body.thread_id,"status":"created","loop_count":0,"artifacts":{}}
    return await graph.ainvoke(state, config={"configurable":{"thread_id":body.thread_id}})
@router.post("/workflows/{workflow_name}/resume")
async def resume_workflow(workflow_name: str, body: ResumeWorkflowRequest, request: Request):
    from langgraph.types import Command
    container=request.app.state.container; factory=container.workflows.get(workflow_name)
    if factory is None: raise HTTPException(404,"unknown workflow")
    context=ToolContext("default","api-user",body.thread_id,workflow_permissions(workflow_name),container.services)
    graph=factory(tools=container.tools,context=context,checkpointer=container.checkpointer)
    return await graph.ainvoke(Command(resume=body.decision),config={"configurable":{"thread_id":body.thread_id}})
@router.get("/workflows/{workflow_name}/{thread_id}")
async def workflow_status(workflow_name: str, thread_id: str, request: Request):
    container=request.app.state.container; factory=container.workflows.get(workflow_name)
    if factory is None: raise HTTPException(404,"unknown workflow")
    graph=factory(checkpointer=container.checkpointer)
    snapshot=await graph.aget_state({"configurable":{"thread_id":thread_id}})
    return {"values":snapshot.values,"next":list(snapshot.next)}
