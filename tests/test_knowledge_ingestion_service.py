
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.services.knowledge_ingestion_service import (
    KnowledgeIngestionService,
)
from app.domain.entities.knowledge_chunk import KnowledgeChunk
from app.domain.entities.knowledge_source import KnowledgeSource
from app.domain.entities.knowledge_type import KnowledgeType

@pytest.fixture
def ingestion_setup(tmp_path):
    """Create a KnowledgeIngestionService with mocked dependencies."""

    stored_file = tmp_path / "test.txt"
    stored_file.write_text("Sample knowledge content", encoding="utf-8")

    source = KnowledgeSource(
        name="test.txt",
        source_type=KnowledgeType.DOCUMENT,
        location=str(stored_file),
    )

    ingestion_result = SimpleNamespace(
        source=source,
        stored_path=str(stored_file),
    )

    processing_result = SimpleNamespace(
        filename="test.txt",
        file_size=25,
        checksum="test-checksum",
    )

    chunk = KnowledgeChunk(
        knowledge_item_id=uuid4(),
        content="Sample knowledge content",
        chunk_index=0,
        start_position=0,
        end_position=24,
        metadata={},
    )

    document_ingestion = MagicMock()
    document_ingestion.ingest.return_value = ingestion_result

    file_processing = MagicMock()
    file_processing.process.return_value = processing_result

    extractor = MagicMock()
    extractor.read.return_value = "Sample knowledge content"

    chunking = MagicMock()
    chunking.chunk.return_value = [chunk]

    metadata_service = MagicMock()
    metadata_service.build.return_value = SimpleNamespace(
        filename="test.txt",
        file_type=".txt",
    )

    source_repository = MagicMock()
    knowledge_repository = MagicMock()
    chunk_repository = MagicMock()

    journal = MagicMock()
    journal.start.return_value = "test-ingestion-id"

    logger = MagicMock()

    service = KnowledgeIngestionService(
        document_ingestion_service=document_ingestion,
        file_processing_service=file_processing,
        document_extractor=extractor,
        chunking_service=chunking,
        metadata_service=metadata_service,
        source_repository=source_repository,
        knowledge_repository=knowledge_repository,
        chunk_repository=chunk_repository,
        knowledge_logger=logger,
        ingestion_journal=journal,
    )

    return {
        "service": service,
        "source": source,
        "stored_file": stored_file,
        "document_ingestion": document_ingestion,
        "file_processing": file_processing,
        "extractor": extractor,
        "chunking": chunking,
        "metadata_service": metadata_service,
        "source_repository": source_repository,
        "knowledge_repository": knowledge_repository,
        "chunk_repository": chunk_repository,
        "journal": journal,
        "logger": logger,
    }

def test_successful_document_ingestion(ingestion_setup):
    """Verify the complete successful ingestion workflow."""

    components = ingestion_setup
    service = components["service"]

    result = service.ingest_document(
        filename="test.txt",
        content=b"Sample knowledge content",
        author="Test Author",
        source_url="https://example.com",
    )

    assert result.filename == "test.txt"
    assert result.file_size == 25
    assert result.chunk_count == 1
    assert result.extracted_character_count == 24
    assert result.source_id == str(components["source"].source_id)

    components["source_repository"].save.assert_called_once()
    components["knowledge_repository"].save.assert_called_once()
    components["chunk_repository"].save.assert_called_once()

    components["journal"].complete.assert_called_once_with(
        "test-ingestion-id"
    )

    components["logger"].ingestion_completed.assert_called_once()

def test_empty_extracted_text_raises_value_error(ingestion_setup):
    """Verify that empty extracted text is rejected."""

    components = ingestion_setup
    components["extractor"].read.return_value = "   "

    with pytest.raises(
        ValueError,
        match="No readable text was extracted",
    ):
        components["service"].ingest_document(
            filename="empty.txt",
            content=b" ",
        )

    components["source_repository"].save.assert_not_called()
    components["knowledge_repository"].save.assert_not_called()
    components["chunk_repository"].save.assert_not_called()

    assert not components["stored_file"].exists()

def test_file_processing_failure(ingestion_setup):
    """Verify cleanup when file processing fails."""

    components = ingestion_setup

    components["file_processing"].process.side_effect = OSError(
        "File processing failed"
    )

    with pytest.raises(OSError, match="File processing failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["extractor"].read.assert_not_called()
    components["source_repository"].save.assert_not_called()

    assert not components["stored_file"].exists()

def test_text_extraction_failure(ingestion_setup):
    """Verify cleanup when document extraction fails."""

    components = ingestion_setup

    components["extractor"].read.side_effect = ValueError(
        "Extraction failed"
    )

    with pytest.raises(ValueError, match="Extraction failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].save.assert_not_called()
    components["knowledge_repository"].save.assert_not_called()

    assert not components["stored_file"].exists()

def test_source_repository_failure_triggers_cleanup(ingestion_setup):
    """Verify cleanup when source persistence fails."""

    components = ingestion_setup

    components["source_repository"].save.side_effect = OSError(
        "Source save failed"
    )

    with pytest.raises(OSError, match="Source save failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].delete.assert_called_once()
    components["knowledge_repository"].delete.assert_called_once()
    components["chunk_repository"].delete.assert_called_once()

    components["journal"].fail.assert_called_once()
    components["journal"].recovered.assert_called_once()

    assert not components["stored_file"].exists()

def test_knowledge_repository_failure_triggers_cleanup(ingestion_setup):
    """Verify cleanup when knowledge item persistence fails."""

    components = ingestion_setup

    components["knowledge_repository"].save.side_effect = OSError(
        "Knowledge save failed"
    )

    with pytest.raises(OSError, match="Knowledge save failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].delete.assert_called_once()
    components["knowledge_repository"].delete.assert_called_once()
    components["chunk_repository"].delete.assert_called_once()

    assert not components["stored_file"].exists()

def test_chunk_repository_failure_triggers_cleanup(ingestion_setup):
    """Verify cleanup when chunk persistence fails."""

    components = ingestion_setup

    components["chunk_repository"].save.side_effect = OSError(
        "Chunk save failed"
    )

    with pytest.raises(OSError, match="Chunk save failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].delete.assert_called_once()
    components["knowledge_repository"].delete.assert_called_once()
    components["chunk_repository"].delete.assert_called_once()

    components["journal"].fail.assert_called_once()

    assert not components["stored_file"].exists()

def test_journal_start_failure_prevents_repository_persistence(
    ingestion_setup,
):
    """Verify that journal failure prevents repository writes."""

    components = ingestion_setup

    components["journal"].start.side_effect = OSError(
        "Journal unavailable"
    )

    with pytest.raises(OSError, match="Journal unavailable"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].save.assert_not_called()
    components["knowledge_repository"].save.assert_not_called()
    components["chunk_repository"].save.assert_not_called()

    assert not components["stored_file"].exists()

def test_journal_completion_failure_triggers_cleanup(ingestion_setup):
    """Verify cleanup if journal completion fails."""

    components = ingestion_setup

    components["journal"].complete.side_effect = OSError(
        "Journal completion failed"
    )

    with pytest.raises(OSError, match="Journal completion failed"):
        components["service"].ingest_document(
            filename="test.txt",
            content=b"Sample knowledge content",
        )

    components["source_repository"].delete.assert_called_once()
    components["knowledge_repository"].delete.assert_called_once()
    components["chunk_repository"].delete.assert_called_once()

    components["journal"].fail.assert_called_once()

    assert not components["stored_file"].exists()