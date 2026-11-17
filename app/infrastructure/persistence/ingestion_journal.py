
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.infrastructure.persistence.json_storage import JSONStorage


class JSONIngestionJournal:
    """Tracks ingestion operations and their recovery status."""

    FILE_NAME = "ingestion_journal.json"

    def __init__(self, storage: JSONStorage):
        self.storage = storage

    def start(
        self,
        source_id: UUID,
        knowledge_item_id: UUID,
        chunk_ids: list[UUID],
    ) -> str:
        ingestion_id = str(uuid4())

        record = {
            "ingestion_id": ingestion_id,
            "source_id": str(source_id),
            "knowledge_item_id": str(knowledge_item_id),
            "chunk_ids": [str(chunk_id) for chunk_id in chunk_ids],
            "stage": "started",
            "status": "in_progress",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "error": None,
        }

        records = self.storage.read(self.FILE_NAME)
        records.append(record)
        self.storage.write(self.FILE_NAME, records)

        return ingestion_id

    def update_stage(
        self,
        ingestion_id: str,
        stage: str,
    ) -> None:
        self._update(
            ingestion_id,
            stage=stage,
            status="in_progress",
        )

    def complete(self, ingestion_id: str) -> None:
        self._update(
            ingestion_id,
            stage="completed",
            status="completed",
            error=None,
        )

    def fail(
        self,
        ingestion_id: str,
        error: str,
    ) -> None:
        self._update(
            ingestion_id,
            stage="failed",
            status="failed",
            error=error,
        )

    def get_incomplete(self) -> list[dict]:
        return [
            record
            for record in self.storage.read(self.FILE_NAME)
            if record["status"] in ("in_progress", "failed")
        ]

    def get_by_id(self, ingestion_id: str) -> dict | None:
        for record in self.storage.read(self.FILE_NAME):
            if record["ingestion_id"] == ingestion_id:
                return record
        return None

    def recovered(self, ingestion_id: str) -> None:
        self._update(
            ingestion_id,
            stage="recovered",
            status="recovered",
            error=None,
        )

    def _update(self, ingestion_id: str, **changes) -> None:
        records = self.storage.read(self.FILE_NAME)

        for record in records:
            if record["ingestion_id"] == ingestion_id:
                record.update(changes)
                record["updated_at"] = datetime.now(
                    timezone.utc
                ).isoformat()
                self.storage.write(self.FILE_NAME, records)
                return

        raise ValueError(
            f"Ingestion journal entry not found: {ingestion_id}"
        )
