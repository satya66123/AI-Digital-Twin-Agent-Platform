
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
    conversation_context: str = ""
    total_knowledge_chunks: int = 0
    total_conversation_messages: int = 0


class IntelligenceContextBuilder:
    """Builds optimized knowledge, memory and conversation context."""

    def __init__(
        self,
        knowledge_retrieval_service: KnowledgeRetrievalService,
        memory_service: MemoryService,
        memory_limit: int = 5,
    ) -> None:

        if (
            not isinstance(memory_limit, int)
            or isinstance(memory_limit, bool)
            or memory_limit <= 0
        ):
            raise ValueError("Memory limit must be positive.")

        self.knowledge_retrieval_service = knowledge_retrieval_service
        self.memory_service = memory_service
        self.memory_limit = memory_limit

    def build(
        self,
        query: str,
        knowledge_limit: int = 5,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> IntelligenceContext:

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Context query cannot be empty.")

        if (
            not isinstance(knowledge_limit, int)
            or isinstance(knowledge_limit, bool)
            or knowledge_limit <= 0
        ):
            raise ValueError("Knowledge limit must be positive.")

        if conversation_history is None:
            conversation_history = []

        if not isinstance(conversation_history, list):
            raise ValueError("Conversation history must be a list.")

        normalized_query = query.strip()

        # ----------------------------------
        # Knowledge Retrieval
        # ----------------------------------

        knowledge_results = self.knowledge_retrieval_service.search(
            normalized_query,
            limit=knowledge_limit,
        )

        knowledge_context = "\n\n".join(
            result.content for result in knowledge_results
        )

        # ----------------------------------
        # Advanced Memory Retrieval
        # ----------------------------------

        memories = self.memory_service.search_memories(
            query=normalized_query,
            limit=self.memory_limit,
        )

        memory_context = "\n\n".join(
            memory.content for memory in memories
        )

        # ----------------------------------
        # Conversation Context
        # ----------------------------------

        normalized_history = []

        for item in conversation_history:

            if not isinstance(item, dict):
                raise ValueError(
                    "Each conversation history item must be a dictionary."
                )

            role = item.get("role")
            content = item.get("content")

            if role not in ("user", "assistant", "system"):
                raise ValueError("Invalid conversation message role.")

            if not isinstance(content, str) or not content.strip():
                raise ValueError(
                    "Conversation message content cannot be empty."
                )

            normalized_history.append(
                {
                    "role": role,
                    "content": content.strip(),
                }
            )

        conversation_context = "\n\n".join(
            f"{item['role'].upper()}: {item['content']}"
            for item in normalized_history
        )

        # ----------------------------------
        # Build Final Intelligence Context
        # ----------------------------------

        return IntelligenceContext(
            query=normalized_query,
            knowledge_context=knowledge_context,
            memory_context=memory_context,
            memories=tuple(memories),
            total_memories=len(memories),
            conversation_context=conversation_context,
            total_knowledge_chunks=len(knowledge_results),
            total_conversation_messages=len(normalized_history),
        )

    @staticmethod
    def format_context(context: IntelligenceContext) -> str:

        if not isinstance(context, IntelligenceContext):
            raise ValueError("A valid intelligence context is required.")

        return (
            f"User Query:\n{context.query}\n\n"
            f"Relevant Knowledge:\n"
            f"{context.knowledge_context or 'No relevant knowledge found.'}\n\n"
            f"Relevant Memories:\n"
            f"{context.memory_context or 'No relevant memories found.'}\n\n"
            f"Recent Conversation:\n"
            f"{context.conversation_context or 'No previous conversation.'}"
        )
