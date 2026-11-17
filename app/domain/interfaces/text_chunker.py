
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.knowledge_chunk import KnowledgeChunk


class TextChunker(ABC):

    @abstractmethod
    def chunk(
        self,
        knowledge_item_id: UUID,
        text: str,
    ) -> list[KnowledgeChunk]:
        raise NotImplementedError
