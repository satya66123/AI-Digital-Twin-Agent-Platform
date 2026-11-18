
from dataclasses import dataclass

from app.application.services.knowledge_retrieval_service import (
    KnowledgeRetrievalService,
)
from app.application.services.memory_service import MemoryService
from app.domain.entities.memory import Memory


@dataclass(frozen=True)
class IntelligenceContext:
    query: str
    knowledge_context: str
    memory_context: str
    memories: tuple[Memory, ...]
    total_memories: int


class IntelligenceContextBuilder:
    """Combines retrieved knowledge and memories into AI context."""

    def __init__(
        self,
        knowledge_retrieval_service: KnowledgeRetrievalService,
        memory_service: MemoryService,
    ) -> None:
        self.knowledge_retrieval_service = knowledge_retrieval_service
        self.memory_service = memory_service

    def build(
        self,
        query: str,
        knowledge_limit: int = 5,
    ) -> IntelligenceContext:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Context query cannot be empty.")

        if not isinstance(knowledge_limit, int) or knowledge_limit <= 0:
            raise ValueError("Knowledge limit must be positive.")

        normalized_query = query.strip()

        knowledge_results = self.knowledge_retrieval_service.search(
            normalized_query,
            limit=knowledge_limit,
        )

        memories = self.memory_service.search_memories(
            normalized_query
        )

        knowledge_context = "\n\n".join(
            result.content for result in knowledge_results
        )

        memory_context = "\n\n".join(
            memory.content for memory in memories
        )

        return IntelligenceContext(
            query=normalized_query,
            knowledge_context=knowledge_context,
            memory_context=memory_context,
            memories=tuple(memories),
            total_memories=len(memories),
        )

    @staticmethod
    def format_context(context: IntelligenceContext) -> str:
        if not isinstance(context, IntelligenceContext):
            raise ValueError("A valid intelligence context is required.")

        return (
            f"User Query:\n{context.query}\n\n"
            f"Relevant Knowledge:\n{context.knowledge_context}\n\n"
            f"Relevant Memories:\n{context.memory_context}"
        )
