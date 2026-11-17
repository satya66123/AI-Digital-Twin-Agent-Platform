
from uuid import UUID

from app.infrastructure.persistence.ingestion_journal import (
    JSONIngestionJournal,
)


class KnowledgeIngestionRecoveryService:
    """Cleans up incomplete knowledge ingestion operations."""

    def __init__(
        self,
        journal: JSONIngestionJournal,
        source_repository,
        knowledge_repository,
        chunk_repository,
    ):
        self.journal = journal
        self.source_repository = source_repository
        self.knowledge_repository = knowledge_repository
        self.chunk_repository = chunk_repository

    def recover_incomplete_ingestions(self) -> dict:
        recovered = []
        failed = []

        for record in self.journal.get_incomplete():
            ingestion_id = record["ingestion_id"]

            try:
                for chunk_id in record["chunk_ids"]:
                    self.chunk_repository.delete(UUID(chunk_id))

                self.knowledge_repository.delete(
                    UUID(record["knowledge_item_id"])
                )

                self.source_repository.delete(
                    UUID(record["source_id"])
                )

                self.journal.recovered(ingestion_id)
                recovered.append(ingestion_id)

            except Exception as exc:
                self.journal.fail(ingestion_id, str(exc))
                failed.append({
                    "ingestion_id": ingestion_id,
                    "error": str(exc),
                })

        return {
            "recovered_count": len(recovered),
            "failed_count": len(failed),
            "recovered": recovered,
            "failed": failed,
        }
