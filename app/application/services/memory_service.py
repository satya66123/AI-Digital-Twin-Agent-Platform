
from uuid import UUID

from app.domain.entities.memory import Memory
from app.domain.entities.memory_type import MemoryType
from app.infrastructure.persistence.repositories.json_memory_repository import (
    JSONMemoryRepository,
)


class MemoryService:
    """Manages Digital Twin memory operations."""

    def __init__(
        self,
        repository: JSONMemoryRepository | None = None,
    ) -> None:
        self.repository = repository or JSONMemoryRepository()

    def create_memory(
        self,
        content: str,
        memory_type: MemoryType,
        metadata: dict[str, str] | None = None,
    ) -> Memory:
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Memory content cannot be empty.")

        if not isinstance(memory_type, MemoryType):
            raise ValueError("A valid memory type is required.")

        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValueError("Memory metadata must be a dictionary.")

            for key, value in metadata.items():
                if not isinstance(key, str) or not key.strip():
                    raise ValueError("Metadata keys must be non-empty strings.")
                if not isinstance(value, str):
                    raise ValueError("Metadata values must be strings.")

        memory = Memory(
            content=content.strip(),
            memory_type=memory_type,
            metadata=metadata or {},
        )

        return self.repository.save(memory)

    def get_memory(self, memory_id: UUID) -> Memory | None:
        if not isinstance(memory_id, UUID):
            raise ValueError("A valid memory ID is required.")

        return self.repository.get_by_id(memory_id)

    def get_all_memories(self) -> list[Memory]:
        return self.repository.get_all()

    def get_memories_by_type(
        self,
        memory_type: MemoryType,
    ) -> list[Memory]:
        if not isinstance(memory_type, MemoryType):
            raise ValueError("A valid memory type is required.")

        return self.repository.get_by_type(memory_type)

    def update_memory(self, memory: Memory) -> Memory:
        if not isinstance(memory, Memory):
            raise ValueError("A valid Memory object is required.")

        existing = self.repository.get_by_id(memory.memory_id)

        if existing is None:
            raise ValueError("Memory not found.")

        return self.repository.save(memory)

    def delete_memory(self, memory_id: UUID) -> bool:
        if not isinstance(memory_id, UUID):
            raise ValueError("A valid memory ID is required.")

        return self.repository.delete(memory_id)

    def count_memories(self) -> int:
        return len(self.repository.get_all())



    def create_short_term_memory(
        self,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> Memory:
        return self.create_memory(
            content=content,
            memory_type=MemoryType.SHORT_TERM,
            metadata=metadata,
        )

    def create_long_term_memory(
        self,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> Memory:
        return self.create_memory(
            content=content,
            memory_type=MemoryType.LONG_TERM,
            metadata=metadata,
        )

    def get_short_term_memories(self) -> list[Memory]:
        return self.get_memories_by_type(MemoryType.SHORT_TERM)

    def get_long_term_memories(self) -> list[Memory]:
        return self.get_memories_by_type(MemoryType.LONG_TERM)

    def clear_short_term_memories(self) -> int:
        memories = self.get_short_term_memories()
        deleted_count = 0

        for memory in memories:
            if self.delete_memory(memory.memory_id):
                deleted_count += 1

        return deleted_count


    def search_memories(self, query: str) -> list[Memory]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        query_words = set(query.lower().split())

        memories = self.get_all_memories()

        scored_memories = []

        for memory in memories:
            content_words = set(memory.content.lower().split())
            score = len(query_words.intersection(content_words))

            if score > 0:
                scored_memories.append((score, memory))

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory for _, memory in scored_memories
        ]

    def consolidate_short_term_memories(self) -> int:
        short_term_memories = self.get_short_term_memories()
        consolidated_count = 0

        for memory in short_term_memories:
            long_term_memory = Memory(
                content=memory.content,
                memory_type=MemoryType.LONG_TERM,
                metadata={
                    **memory.metadata,
                    "consolidated_from": str(memory.memory_id),
                },
            )

            self.repository.save(long_term_memory)

            if self.delete_memory(memory.memory_id):
                consolidated_count += 1

        return consolidated_count


