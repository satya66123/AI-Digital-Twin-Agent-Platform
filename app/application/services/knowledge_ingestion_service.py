
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.application.services.document_ingestion_service import (
    DocumentIngestionService,
)
from app.application.services.file_processing_service import (
    FileProcessingService,
)
from app.application.services.knowledge_chunking_service import (
    KnowledgeChunkingService,
)
from app.application.services.knowledge_metadata_service import (
    KnowledgeMetadataService,
)
from app.domain.entities.knowledge_item import KnowledgeItem
from app.domain.entities.knowledge_type import KnowledgeType
from app.domain.entities.knowledge_chunk import KnowledgeChunk
from app.infrastructure.extraction import DocumentExtractor
from app.infrastructure.logging import KnowledgeLogger
from app.infrastructure.persistence import JSONStorage
from app.infrastructure.persistence.ingestion_journal import (
    JSONIngestionJournal,
)
from app.infrastructure.persistence.repositories import (
    JSONKnowledgeSourceRepository,
    JSONKnowledgeRepository,
    JSONKnowledgeChunkRepository,
)


@dataclass(frozen=True)
class KnowledgeIngestionResult:
    source_id: str
    knowledge_item_id: str
    filename: str
    file_size: int
    chunk_count: int
    extracted_character_count: int
    ingested_at: datetime


class KnowledgeIngestionService:
    """Coordinates document ingestion with JSON-based recovery."""

    def __init__(
        self,
        document_ingestion_service: DocumentIngestionService | None = None,
        file_processing_service: FileProcessingService | None = None,
        document_extractor: DocumentExtractor | None = None,
        chunking_service: KnowledgeChunkingService | None = None,
        metadata_service: KnowledgeMetadataService | None = None,
        source_repository=None,
        knowledge_repository=None,
        chunk_repository=None,
        knowledge_logger: KnowledgeLogger | None = None,
        json_storage: JSONStorage | None = None,
        ingestion_journal: JSONIngestionJournal | None = None,
    ) -> None:
        self.json_storage = json_storage or JSONStorage()

        self.document_ingestion_service = (
            document_ingestion_service or DocumentIngestionService()
        )
        self.file_processing_service = (
            file_processing_service or FileProcessingService()
        )
        self.document_extractor = (
            document_extractor or DocumentExtractor()
        )
        self.chunking_service = (
            chunking_service or KnowledgeChunkingService()
        )
        self.metadata_service = (
            metadata_service or KnowledgeMetadataService()
        )

        self.source_repository = (
            source_repository
            or JSONKnowledgeSourceRepository(self.json_storage)
        )
        self.knowledge_repository = (
            knowledge_repository
            or JSONKnowledgeRepository(self.json_storage)
        )
        self.chunk_repository = (
            chunk_repository
            or JSONKnowledgeChunkRepository(self.json_storage)
        )

        self.journal = (
            ingestion_journal
            or JSONIngestionJournal(self.json_storage)
        )

        self.logger = knowledge_logger or KnowledgeLogger()

    def ingest_document(
        self,
        filename: str,
        content: bytes,
        author: str = "",
        source_url: str = "",
    ) -> KnowledgeIngestionResult:

        ingestion = None
        journal_id = None
        source_id = None
        item_id = None
        chunk_ids = []
        persistence_started = False

        self.logger.ingestion_started(filename)

        try:
            # 1. Store the uploaded document.
            ingestion = self.document_ingestion_service.ingest(
                filename=filename,
                content=content,
            )

            # 2. Validate and calculate file information.
            processing = self.file_processing_service.process(
                ingestion.stored_path
            )

            self.logger.file_processing_completed(
                filename=processing.filename,
                file_size=processing.file_size,
                checksum=processing.checksum,
            )

            # 3. Extract text.
            extracted_text = self.document_extractor.read(
                ingestion.stored_path
            )

            self.logger.extraction_completed(
                filename=processing.filename,
                character_count=len(extracted_text),
            )

            if not extracted_text.strip():
                raise ValueError(
                    "No readable text was extracted from the document."
                )

            # 4. Create the knowledge item.
            knowledge_item = KnowledgeItem(
                title=Path(filename.replace("\\", "/")).name,
                content=extracted_text,
                source_id=ingestion.source.source_id,
                knowledge_type=KnowledgeType.DOCUMENT,
            )

            # 5. Build metadata.
            metadata = self.metadata_service.build(
                file_path=ingestion.stored_path,
                author=author,
                source_url=source_url,
                extracted_text=extracted_text,
                checksum=processing.checksum,
            )

            # 6. Generate chunks.
            chunks = self.chunking_service.chunk(
                knowledge_item_id=knowledge_item.item_id,
                text=extracted_text,
            )

            enriched_chunks = [
                KnowledgeChunk(
                    knowledge_item_id=chunk.knowledge_item_id,
                    content=chunk.content,
                    chunk_index=chunk.chunk_index,
                    start_position=chunk.start_position,
                    end_position=chunk.end_position,
                    metadata={
                        **chunk.metadata,
                        "filename": metadata.filename,
                        "file_type": metadata.file_type,
                        "checksum": processing.checksum,
                    },
                    chunk_id=chunk.chunk_id,
                )
                for chunk in chunks
            ]

            # 7. Create journal entry before persistence begins.
            source_id = ingestion.source.source_id
            item_id = knowledge_item.item_id
            chunk_ids = [
                chunk.chunk_id for chunk in enriched_chunks
            ]

            journal_id = self.journal.start(
                source_id=source_id,
                knowledge_item_id=item_id,
                chunk_ids=chunk_ids,
            )

            self.journal.update_stage(
                journal_id,
                "document_processed",
            )

            # 8. Persist the source.
            persistence_started = True
            self.source_repository.save(ingestion.source)

            self.journal.update_stage(
                journal_id,
                "source_saved",
            )

            # 9. Persist the knowledge item.
            self.knowledge_repository.save(knowledge_item)

            self.journal.update_stage(
                journal_id,
                "knowledge_item_saved",
            )

            # 10. Persist chunks.
            for chunk in enriched_chunks:
                self.chunk_repository.save(chunk)

            self.journal.update_stage(
                journal_id,
                "chunks_saved",
            )

            # 11. Mark ingestion complete.
            self.journal.complete(journal_id)

            self.logger.chunking_completed(
                item_id=str(item_id),
                chunk_count=len(enriched_chunks),
            )

            self.logger.storage_completed(
                entity_type="knowledge_source",
                entity_id=str(source_id),
            )

            self.logger.storage_completed(
                entity_type="knowledge_item",
                entity_id=str(item_id),
            )

            self.logger.ingestion_completed(
                filename=processing.filename,
                source_id=str(source_id),
                item_id=str(item_id),
                chunk_count=len(enriched_chunks),
            )

            return KnowledgeIngestionResult(
                source_id=str(source_id),
                knowledge_item_id=str(item_id),
                filename=processing.filename,
                file_size=processing.file_size,
                chunk_count=len(enriched_chunks),
                extracted_character_count=len(extracted_text),
                ingested_at=datetime.now(timezone.utc),
            )

        except Exception as exc:
            # Record the failure before attempting cleanup.
            if journal_id is not None:
                try:
                    self.journal.fail(journal_id, str(exc))
                except Exception:
                    pass

            # Roll back partial repository writes.
            cleanup_succeeded = True

            if persistence_started:
                try:
                    for chunk_id in chunk_ids:
                        self.chunk_repository.delete(chunk_id)

                    if item_id is not None:
                        self.knowledge_repository.delete(item_id)

                    if source_id is not None:
                        self.source_repository.delete(source_id)

                except Exception:
                    cleanup_succeeded = False

            # Remove the uploaded file after a failed ingestion.
            if ingestion is not None:
                try:
                    Path(ingestion.stored_path).unlink(
                        missing_ok=True
                    )
                except OSError:
                    cleanup_succeeded = False

            # Mark cleanup completion in the journal.
            if journal_id is not None and cleanup_succeeded:
                try:
                    self.journal.recovered(journal_id)
                except Exception:
                    pass

            try:
                self.logger.ingestion_failed(
                    filename=filename,
                    error=str(exc),
                )
            except Exception:
                pass

            raise
