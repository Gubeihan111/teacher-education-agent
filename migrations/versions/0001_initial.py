"""Initial workflow, evidence and vector schema."""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
revision="0001_initial"; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table("workflow_runs", sa.Column("id",sa.Uuid(),primary_key=True), sa.Column("thread_id",sa.String(128),nullable=False,unique=True), sa.Column("workflow_name",sa.String(80),nullable=False), sa.Column("status",sa.String(32),nullable=False), sa.Column("state_summary",sa.JSON(),nullable=False), sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now()))
    op.create_table("evidence", sa.Column("id",sa.Uuid(),primary_key=True), sa.Column("run_id",sa.Uuid(),sa.ForeignKey("workflow_runs.id")), sa.Column("source_type",sa.String(32),nullable=False), sa.Column("content",sa.Text(),nullable=False), sa.Column("metadata_json",sa.JSON(),nullable=False))
    op.create_table("knowledge_chunks", sa.Column("id",sa.Uuid(),primary_key=True), sa.Column("source_ref",sa.String(512),nullable=False), sa.Column("content",sa.Text(),nullable=False), sa.Column("metadata_json",sa.JSON(),nullable=False), sa.Column("embedding",Vector(1024),nullable=False))
    op.execute("CREATE INDEX knowledge_chunks_embedding_hnsw ON knowledge_chunks USING hnsw (embedding vector_cosine_ops)")
    op.create_table("learner_profiles",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("learner_id",sa.String(128),unique=True,nullable=False),sa.Column("version",sa.Integer(),nullable=False),sa.Column("profile_data",sa.JSON(),nullable=False))
    op.create_table("instructional_designs",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("owner_id",sa.String(128),nullable=False),sa.Column("title",sa.String(255),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("design_data",sa.JSON(),nullable=False))
    op.create_table("practice_records",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("owner_id",sa.String(128),nullable=False),sa.Column("design_id",sa.Uuid(),sa.ForeignKey("instructional_designs.id")),sa.Column("evidence_refs",sa.JSON(),nullable=False),sa.Column("outcome_data",sa.JSON(),nullable=False))
    op.create_table("reflection_records",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("owner_id",sa.String(128),nullable=False),sa.Column("practice_id",sa.Uuid(),sa.ForeignKey("practice_records.id")),sa.Column("reflection_data",sa.JSON(),nullable=False),sa.Column("evidence_refs",sa.JSON(),nullable=False))
    op.create_table("audit_events",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("actor_id",sa.String(128),nullable=False),sa.Column("event_type",sa.String(80),nullable=False),sa.Column("aggregate_ref",sa.String(160),nullable=False),sa.Column("payload",sa.JSON(),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now()))
def downgrade():
    op.drop_table("audit_events"); op.drop_table("reflection_records"); op.drop_table("practice_records"); op.drop_table("instructional_designs"); op.drop_table("learner_profiles"); op.drop_table("knowledge_chunks"); op.drop_table("evidence"); op.drop_table("workflow_runs")
