"""database/models infrastructure adapter placeholder."""
"""Business records; LangGraph checkpoints remain a separate concern."""
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
class Base(DeclarativeBase): pass
class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    thread_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    workflow_name: Mapped[str] = mapped_column(String(80)); status: Mapped[str] = mapped_column(String(32))
    state_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("workflow_runs.id"))
    source_type: Mapped[str] = mapped_column(String(32)); content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_ref: Mapped[str] = mapped_column(String(512), index=True); content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict); embedding: Mapped[list[float]] = mapped_column(Vector(1024))
class LearnerProfile(Base):
    __tablename__="learner_profiles"; id: Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    learner_id: Mapped[str]=mapped_column(String(128),unique=True,index=True); version: Mapped[int]=mapped_column(default=1); profile_data: Mapped[dict]=mapped_column(JSON,default=dict)
class InstructionalDesign(Base):
    __tablename__="instructional_designs"; id: Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    owner_id: Mapped[str]=mapped_column(String(128),index=True); title: Mapped[str]=mapped_column(String(255)); status: Mapped[str]=mapped_column(String(32),default="draft"); design_data: Mapped[dict]=mapped_column(JSON,default=dict)
class PracticeRecord(Base):
    __tablename__="practice_records"; id: Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    owner_id: Mapped[str]=mapped_column(String(128),index=True); design_id: Mapped[uuid.UUID | None]=mapped_column(ForeignKey("instructional_designs.id")); evidence_refs: Mapped[list]=mapped_column(JSON,default=list); outcome_data: Mapped[dict]=mapped_column(JSON,default=dict)
class ReflectionRecord(Base):
    __tablename__="reflection_records"; id: Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    owner_id: Mapped[str]=mapped_column(String(128),index=True); practice_id: Mapped[uuid.UUID | None]=mapped_column(ForeignKey("practice_records.id")); reflection_data: Mapped[dict]=mapped_column(JSON,default=dict); evidence_refs: Mapped[list]=mapped_column(JSON,default=list)
class AuditEvent(Base):
    __tablename__="audit_events"; id: Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    actor_id: Mapped[str]=mapped_column(String(128),index=True); event_type: Mapped[str]=mapped_column(String(80),index=True); aggregate_ref: Mapped[str]=mapped_column(String(160)); payload: Mapped[dict]=mapped_column(JSON,default=dict); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
