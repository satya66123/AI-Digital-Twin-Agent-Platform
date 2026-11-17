
from datetime import datetime
from uuid import UUID

from app.domain.entities.knowledge_source import KnowledgeSource
from app.domain.entities.knowledge_type import KnowledgeType
from app.domain.interfaces.knowledge_source_repository import (
    KnowledgeSourceRepository,
)
from app.infrastructure.persistence.json_storage import JSONStorage


class JSONKnowledgeSourceRepository(KnowledgeSourceRepository):
    """JSON-backed repository for knowledge sources."""

    FILE_NAME = "sources.json"

    def __init__(self, storage: JSONStorage | None = None):
        self.storage = storage or JSONStorage()

    def save(self, source: KnowledgeSource) -> None:
        records = self.storage.read(self.FILE_NAME)
        source_id = str(source.source_id)

        record = {
            "source_id": source_id,
            "name": source.name,
            "source_type": source.source_type.value,
            "location": source.location,
            "created_at": source.created_at.isoformat(),
        }

        for index, item in enumerate(records):
            if item["source_id"] == source_id:
                records[index] = record
                break
        else:
            records.append(record)

        self.storage.write(self.FILE_NAME, records)

    def get_by_id(self, source_id: UUID) -> KnowledgeSource | None:
        for record in self.storage.read(self.FILE_NAME):
            if record["source_id"] == str(source_id):
                return self._deserialize(record)

        return None

    def get_all(self) -> list[KnowledgeSource]:
        return [
            self._deserialize(record)
            for record in self.storage.read(self.FILE_NAME)
        ]

    def get(self, source_id: UUID) -> KnowledgeSource | None:
        return self.get_by_id(source_id)

    def delete(self, source_id: UUID) -> bool:
        records = self.storage.read(self.FILE_NAME)

        updated = [
            record
            for record in records
            if record["source_id"] != str(source_id)
        ]

        if len(updated) == len(records):
            return False

        self.storage.write(self.FILE_NAME, updated)
        return True

    @staticmethod
    def _deserialize(record: dict) -> KnowledgeSource:
        return KnowledgeSource(
            name=record["name"],
            source_type=KnowledgeType(record["source_type"]),
            location=record["location"],
            source_id=UUID(record["source_id"]),
            created_at=datetime.fromisoformat(record["created_at"]),
        )
