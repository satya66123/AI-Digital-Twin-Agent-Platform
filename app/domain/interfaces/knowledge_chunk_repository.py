from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.knowledge_chunk import KnowledgeChunk


class KnowledgeChunkRepository(ABC):

    @abstractmethod
    def save(self, chunk: KnowledgeChunk) -> KnowledgeChunk:
        ...

    @abstractmethod
    def get(self, chunk_id: UUID) -> KnowledgeChunk | None:
        ...

    @abstractmethod
    def get_by_item(self, knowledge_item_id: UUID) -> list[KnowledgeChunk]:
        ...

    @abstractmethod
    def get_all(self) -> list[KnowledgeChunk]:
        ...

    @abstractmethod
    def delete(self, chunk_id: UUID) -> bool:
        ...