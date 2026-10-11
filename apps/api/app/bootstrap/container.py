"""Application composition root."""
from dataclasses import dataclass
from teacher_education_agent.core.config import Settings, get_settings
from teacher_education_agent.infrastructure.database.session import build_session_factory
from teacher_education_agent.infrastructure.vector_store import PgVectorStore
from teacher_education_agent.model_services.gateway import ModelGateway
from teacher_education_agent.model_services.speech import FunASRClient
from teacher_education_agent.tools import build_default_tool_registry
from teacher_education_agent.workflows.registry import WORKFLOW_FACTORIES
from teacher_education_agent.application.services.tool_services import build_tool_services
from teacher_education_agent.knowledge.ingestion import KnowledgeIngestor
@dataclass(slots=True)
class Container:
    settings: Settings; tools: object; models: ModelGateway; speech: FunASRClient; vector_store: PgVectorStore; sessions: object; workflows: dict; services: dict; ingestor: KnowledgeIngestor; checkpointer: object | None = None
def build_container() -> Container:
    settings=get_settings()
    models=ModelGateway(settings); speech=FunASRClient(settings); vector=PgVectorStore(); sessions=build_session_factory(settings)
    services=build_tool_services(models=models,speech=speech,vector_store=vector,sessions=sessions)
    return Container(settings, build_default_tool_registry(), models, speech, vector, sessions, dict(WORKFLOW_FACTORIES), services, KnowledgeIngestor(models,sessions,vector_dimension=settings.vector_dimension))
