
from datetime import datetime
from uuid import UUID

from app.domain.entities.knowledge_item import KnowledgeItem
from app.domain.entities.knowledge_type import KnowledgeType
from app.domain.interfaces.knowledge_repository import KnowledgeRepository
from app.infrastructure.persistence.json_storage import JSONStorage


class JSONKnowledgeRepository(KnowledgeRepository):

    FILE_NAME = "knowledge_items.json"

    def __init__(self, storage: JSONStorage | None = None):
        self.storage = storage or JSONStorage()

    def save(self, item: KnowledgeItem) -> None:
        records = self.storage.read(self.FILE_NAME)
        item_id = str(item.item_id)

        record = {
            "item_id": item_id,
            "title": item.title,
            "content": item.content,
            "source_id": str(item.source_id),
            "knowledge_type": item.knowledge_type.value,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }

        for index, existing in enumerate(records):
            if existing["item_id"] == item_id:
                records[index] = record
                break
        else:
            records.append(record)

        self.storage.write(self.FILE_NAME, records)

    def get_by_id(self, item_id: UUID) -> KnowledgeItem | None:
        for record in self.storage.read(self.FILE_NAME):
            if record["item_id"] == str(item_id):
                return self._deserialize(record)

        return None

    def get_by_source_id(self, source_id: UUID) -> list[KnowledgeItem]:
        return [
            self._deserialize(record)
            for record in self.storage.read(self.FILE_NAME)
            if record["source_id"] == str(source_id)
        ]

    def get_all(self) -> list[KnowledgeItem]:
        return [
            self._deserialize(record)
            for record in self.storage.read(self.FILE_NAME)
        ]

    def delete(self, item_id: UUID) -> bool:
        records = self.storage.read(self.FILE_NAME)
        updated = [
            record for record in records
            if record["item_id"] != str(item_id)
        ]

        if len(updated) == len(records):
            return False

        self.storage.write(self.FILE_NAME, updated)
        return True

    @staticmethod
    def _deserialize(record: dict) -> KnowledgeItem:
        return KnowledgeItem(
            title=record["title"],
            content=record["content"],
            source_id=UUID(record["source_id"]),
            knowledge_type=KnowledgeType(record["knowledge_type"]),
            item_id=UUID(record["item_id"]),
            created_at=datetime.fromisoformat(record["created_at"]),
            updated_at=datetime.fromisoformat(record["updated_at"]),
        )

    def get(self, item_id: UUID) -> KnowledgeItem | None:
        return self.get_by_id(item_id)

    def get_by_source(self, source_id: UUID) -> list[KnowledgeItem]:
        return self.get_by_source_id(source_id)
