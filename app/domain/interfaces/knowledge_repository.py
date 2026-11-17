from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.knowledge_item import KnowledgeItem


class KnowledgeRepository(ABC):

    @abstractmethod
    def save(self, item: KnowledgeItem) -> KnowledgeItem:
        ...

    @abstractmethod
    def get(self, item_id: UUID) -> KnowledgeItem | None:
        ...

    @abstractmethod
    def get_by_source(self, source_id: UUID) -> list[KnowledgeItem]:
        ...

    @abstractmethod
    def get_all(self) -> list[KnowledgeItem]:
        ...

    @abstractmethod
    def delete(self, item_id: UUID) -> bool:
        ...