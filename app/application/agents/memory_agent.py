
from uuid import UUID

from app.application.services.memory_service import MemoryService
from app.application.services.intelligence_service import (
    IntelligenceService,
    IntelligenceResponse,
)
from app.domain.entities.memory import Memory
from app.domain.entities.memory_type import MemoryType


class MemoryAgent:
    """Coordinates memory operations and AI intelligence."""

    def __init__(
        self,
        memory_service: MemoryService,
        intelligence_service: IntelligenceService,
    ) -> None:
        self.memory_service = memory_service
        self.intelligence_service = intelligence_service

    def remember(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        metadata: dict[str, str] | None = None,
    ) -> Memory:
        return self.memory_service.create_memory(
            content=content,
            memory_type=memory_type,
            metadata=metadata,
        )

    def recall(self, query: str) -> list[Memory]:
        return self.memory_service.search_memories(query)

    def retrieve_memory(self, memory_id: UUID) -> Memory | None:
        return self.memory_service.get_memory(memory_id)

    def forget(self, memory_id: UUID) -> bool:
        return self.memory_service.delete_memory(memory_id)

    def answer(
        self,
        query: str,
        model: str,
    ) -> IntelligenceResponse:
        return self.intelligence_service.generate_response(
            query=query,
            model=model,
        )

    def consolidate_memories(self) -> int:
        return self.memory_service.consolidate_short_term_memories()
