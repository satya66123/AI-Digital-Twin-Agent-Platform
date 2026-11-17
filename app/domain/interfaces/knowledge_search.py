from abc import ABC, abstractmethod

from app.domain.entities.knowledge_chunk import KnowledgeChunk


class KnowledgeSearch(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[KnowledgeChunk]:
        ...