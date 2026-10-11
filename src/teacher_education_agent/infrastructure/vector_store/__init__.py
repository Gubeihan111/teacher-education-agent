"""vector_store infrastructure adapter placeholder."""
"""pgvector-backed semantic retrieval."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from teacher_education_agent.infrastructure.database.models import KnowledgeChunk
class PgVectorStore:
    async def search(self, session: AsyncSession, embedding: list[float], limit: int = 8):
        distance = KnowledgeChunk.embedding.cosine_distance(embedding)
        rows = await session.execute(select(KnowledgeChunk, distance.label("distance")).order_by(distance).limit(limit))
        return [{"id": str(chunk.id), "content": chunk.content, "metadata": chunk.metadata_json, "distance": float(dist)} for chunk, dist in rows]
