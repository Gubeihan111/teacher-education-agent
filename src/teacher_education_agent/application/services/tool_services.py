"""Adapters that bind workflow tools to real infrastructure ports."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from teacher_education_agent.infrastructure.database.models import Evidence
from teacher_education_agent.model_services.contracts import ModelRequest

def build_tool_services(*, models, speech, vector_store, sessions) -> dict[str, Any]:
    async def evidence_store(payload: Mapping[str, Any], context):
        async with sessions() as session:
            row=Evidence(source_type=str(payload.get("source_type","learner")),content=str(payload["content"]),metadata_json={"actor_id":context.actor_id,"correlation_id":context.correlation_id})
            session.add(row); await session.commit(); await session.refresh(row)
            return {"evidence_ref":str(row.id),"persisted":True,"_evidence_refs":(str(row.id),)}
    async def resource_recommender(payload: Mapping[str, Any], context):
        query=str(payload.get("query") or payload.get("goal") or payload.get("text") or "").strip()
        if not query: raise ValueError("query is required")
        vector=(await models.embed([query]))[0]
        async with sessions() as session: candidates=await vector_store.search(session,vector,int(payload.get("limit",8)))
        return {"candidates":candidates,"allow_self_selection":True}
    async def model_candidate(payload: Mapping[str, Any], context):
        response=await models.complete(ModelRequest([{"role":"system","content":"返回JSON候选建议，不决定权限、评分、路由或终态。"},{"role":"user","content":str(dict(payload))}],str(payload.get("task_type","dialogue"))))
        return {"candidate":dict(response.parsed or {}),"provider":response.provider,"model":response.model,"candidate_only":True}
    async def speech_recognizer(payload: Mapping[str, Any], context):
        from pathlib import Path
        return await speech.transcribe(Path(str(payload.get("audio_path",""))))
    services={"evidence_store":evidence_store,"resource_recommender":resource_recommender,"speech_recognizer":speech_recognizer}
    for name in ("learning_feedback","virtual_student_responder","judgment_candidate_generator","scaffold_message_generator","strategy_candidate_generator","transfer_task_generator","inquiry_question_generator"):
        services[name]=model_candidate
    return services
