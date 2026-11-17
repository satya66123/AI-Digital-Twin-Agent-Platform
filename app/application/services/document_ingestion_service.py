
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.domain.entities.knowledge_source import KnowledgeSource
from app.domain.entities.knowledge_type import KnowledgeType
from app.infrastructure.storage.document_storage import DocumentStorage


@dataclass(frozen=True)
class DocumentIngestionResult:
    source: KnowledgeSource
    original_filename: str
    stored_path: str
    file_size: int
    ingested_at: datetime


class DocumentIngestionService:

    def __init__(
        self,
        storage: DocumentStorage | None = None,
    ) -> None:
        self.storage = storage or DocumentStorage()

    def ingest(
        self,
        filename: str,
        content: bytes,
    ) -> DocumentIngestionResult:

        if not isinstance(filename, str) or not filename.strip():
            raise ValueError("Document filename is required.")

        if not isinstance(content, bytes):
            raise ValueError("Document content must be bytes.")

        self.storage.validate(filename, len(content))

        stored_path = self.storage.save(filename, content)

        original_filename = Path(
            filename.replace("\\", "/")
        ).name

        source = KnowledgeSource(
            name=original_filename,
            source_type=KnowledgeType.DOCUMENT,
            location=stored_path,
        )

        return DocumentIngestionResult(
            source=source,
            original_filename=original_filename,
            stored_path=stored_path,
            file_size=len(content),
            ingested_at=datetime.now(timezone.utc),
        )
