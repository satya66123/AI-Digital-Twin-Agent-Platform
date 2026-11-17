
from uuid import UUID

from app.domain.entities.knowledge_chunk import KnowledgeChunk
from app.domain.interfaces.knowledge_chunk_repository import (
    KnowledgeChunkRepository,
)
from app.infrastructure.persistence.json_storage import JSONStorage


class JSONKnowledgeChunkRepository(KnowledgeChunkRepository):

    FILE_NAME = "chunks.json"

    def __init__(self, storage: JSONStorage | None = None):
        self.storage = storage or JSONStorage()

    def save(self, chunk: KnowledgeChunk) -> None:
        records = self.storage.read(self.FILE_NAME)
        chunk_id = str(chunk.chunk_id)

        record = {
            "chunk_id": chunk_id,
            "knowledge_item_id": str(chunk.knowledge_item_id),
            "content": chunk.content,
            "chunk_index": chunk.chunk_index,
            "start_position": chunk.start_position,
            "end_position": chunk.end_position,
            "metadata": chunk.metadata,
        }

        for index, existing in enumerate(records):
            if existing["chunk_id"] == chunk_id:
                records[index] = record
                break
        else:
            records.append(record)

        self.storage.write(self.FILE_NAME, records)

    def get_by_id(self, chunk_id: UUID) -> KnowledgeChunk | None:
        for record in self.storage.read(self.FILE_NAME):
            if record["chunk_id"] == str(chunk_id):
                return self._deserialize(record)

        return None

    def get_by_knowledge_item_id(
        self,
        knowledge_item_id: UUID,
    ) -> list[KnowledgeChunk]:
        records = [
            record
            for record in self.storage.read(self.FILE_NAME)
            if record["knowledge_item_id"] == str(knowledge_item_id)
        ]

        return [
            self._deserialize(record)
            for record in sorted(
                records,
                key=lambda item: item["chunk_index"],
            )
        ]

    def get_all(self) -> list[KnowledgeChunk]:
        return [
            self._deserialize(record)
            for record in self.storage.read(self.FILE_NAME)
        ]

    def delete(self, chunk_id: UUID) -> bool:
        records = self.storage.read(self.FILE_NAME)
        updated = [
            record for record in records
            if record["chunk_id"] != str(chunk_id)
        ]

        if len(updated) == len(records):
            return False

        self.storage.write(self.FILE_NAME, updated)
        return True

    @staticmethod
    def _deserialize(record: dict) -> KnowledgeChunk:
        return KnowledgeChunk(
            knowledge_item_id=UUID(record["knowledge_item_id"]),
            content=record["content"],
            chunk_index=record["chunk_index"],
            start_position=record["start_position"],
            end_position=record["end_position"],
            metadata=record["metadata"],
            chunk_id=UUID(record["chunk_id"]),
        )

    def get(self, chunk_id: UUID) -> KnowledgeChunk | None:
        return self.get_by_id(chunk_id)

    def get_by_item(
            self,
            knowledge_item_id: UUID,
    ) -> list[KnowledgeChunk]:
        return self.get_by_knowledge_item_id(knowledge_item_id)
