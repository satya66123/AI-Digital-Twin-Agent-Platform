from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.knowledge_source import KnowledgeSource


class KnowledgeSourceRepository(ABC):

    @abstractmethod
    def save(self, source: KnowledgeSource) -> KnowledgeSource:
        ...

    @abstractmethod
    def get(self, source_id: UUID) -> KnowledgeSource | None:
        ...

    @abstractmethod
    def get_all(self) -> list[KnowledgeSource]:
        ...

    @abstractmethod
    def delete(self, source_id: UUID) -> bool:
        ...