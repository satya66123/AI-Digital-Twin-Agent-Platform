
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.application.services.document_ingestion_service import (
    DocumentIngestionResult,
    DocumentIngestionService,
)
from app.domain.entities.knowledge_source import KnowledgeSource
from app.domain.entities.knowledge_type import KnowledgeType


@pytest.fixture
def storage(tmp_path):
    mock_storage = Mock()
    mock_storage.save.return_value = str(tmp_path / "sample.txt")
    return mock_storage


@pytest.fixture
def service(storage):
    return DocumentIngestionService(storage=storage)


@pytest.fixture
def document_content():
    return b"Sample document content for ingestion."


def test_service_initialization(storage):
    service = DocumentIngestionService(storage=storage)

    assert service.storage is storage


def test_service_creates_default_storage():
    service = DocumentIngestionService()

    assert service.storage is not None


def test_ingest_returns_document_ingestion_result(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert isinstance(result, DocumentIngestionResult)


def test_ingest_returns_knowledge_source(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert isinstance(result.source, KnowledgeSource)


def test_ingest_preserves_original_filename(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert result.original_filename == "sample.txt"


def test_ingest_sets_source_name(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert result.source.name == "sample.txt"


def test_ingest_sets_document_knowledge_type(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert result.source.source_type == KnowledgeType.DOCUMENT


def test_ingest_sets_stored_path(
    service,
    storage,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    expected_path = storage.save.return_value

    assert result.stored_path == expected_path
    assert result.source.location == expected_path


def test_ingest_returns_correct_file_size(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert result.file_size == len(document_content)


def test_ingest_returns_utc_datetime(
    service,
    document_content,
):
    result = service.ingest("sample.txt", document_content)

    assert isinstance(result.ingested_at, datetime)
    assert result.ingested_at.tzinfo == timezone.utc


def test_ingest_calls_storage_validation(
    service,
    storage,
    document_content,
):
    service.ingest("sample.txt", document_content)

    storage.validate.assert_called_once_with(
        "sample.txt",
        len(document_content),
    )


def test_ingest_calls_storage_save(
    service,
    storage,
    document_content,
):
    service.ingest("sample.txt", document_content)

    storage.save.assert_called_once_with(
        "sample.txt",
        document_content,
    )


def test_ingest_validates_before_saving(
    service,
    storage,
    document_content,
):
    call_order = []

    storage.validate.side_effect = (
        lambda *args: call_order.append("validate")
    )

    storage.save.side_effect = (
        lambda *args: call_order.append("save") or "stored/sample.txt"
    )

    service.ingest("sample.txt", document_content)

    assert call_order == ["validate", "save"]


def test_ingest_rejects_empty_filename(
    service,
    document_content,
):
    with pytest.raises(
        ValueError,
        match="Document filename is required",
    ):
        service.ingest("", document_content)


def test_ingest_rejects_whitespace_filename(
    service,
    document_content,
):
    with pytest.raises(
        ValueError,
        match="Document filename is required",
    ):
        service.ingest("   ", document_content)


@pytest.mark.parametrize(
    "filename",
    [None, 123, [], {}],
)
def test_ingest_rejects_non_string_filename(
    service,
    filename,
    document_content,
):
    with pytest.raises(
        ValueError,
        match="Document filename is required",
    ):
        service.ingest(filename, document_content)


def test_ingest_rejects_non_bytes_content(service):
    with pytest.raises(
        ValueError,
        match="Document content must be bytes",
    ):
        service.ingest("sample.txt", "not bytes")


@pytest.mark.parametrize(
    "content",
    [None, 123, [], {}, bytearray(b"sample")],
)
def test_ingest_rejects_invalid_content_types(
    service,
    content,
):
    with pytest.raises(
        ValueError,
        match="Document content must be bytes",
    ):
        service.ingest("sample.txt", content)


def test_ingest_does_not_save_when_validation_fails(
    service,
    storage,
    document_content,
):
    storage.validate.side_effect = ValueError("Invalid document")

    with pytest.raises(ValueError, match="Invalid document"):
        service.ingest("sample.txt", document_content)

    storage.save.assert_not_called()


def test_ingest_propagates_storage_save_error(
    service,
    storage,
    document_content,
):
    storage.save.side_effect = OSError("Storage failure")

    with pytest.raises(OSError, match="Storage failure"):
        service.ingest("sample.txt", document_content)


def test_ingest_normalizes_windows_filename(
    service,
    document_content,
):
    result = service.ingest(
        r"folder\subfolder\sample.txt",
        document_content,
    )

    assert result.original_filename == "sample.txt"
    assert result.source.name == "sample.txt"


def test_ingest_normalizes_unix_filename(
    service,
    document_content,
):
    result = service.ingest(
        "folder/subfolder/sample.txt",
        document_content,
    )

    assert result.original_filename == "sample.txt"


def test_ingest_preserves_filename_with_multiple_dots(
    service,
    document_content,
):
    result = service.ingest(
        "report.final.version.txt",
        document_content,
    )

    assert result.original_filename == "report.final.version.txt"


def test_ingest_preserves_unicode_filename(
    service,
    document_content,
):
    result = service.ingest(
        "తెలుగు_పత్రం.txt",
        document_content,
    )

    assert result.original_filename == "తెలుగు_పత్రం.txt"


def test_ingest_accepts_empty_bytes_at_service_level(
    service,
    storage,
):
    # Empty-file validation is delegated to DocumentStorage.
    storage.validate.return_value = None

    result = service.ingest("sample.txt", b"")

    assert result.file_size == 0

    storage.validate.assert_called_once_with(
        "sample.txt",
        0,
    )


def test_ingest_uses_the_returned_storage_path(
    service,
    storage,
    document_content,
):
    storage.save.return_value = "/custom/storage/document.txt"

    result = service.ingest("document.txt", document_content)

    assert result.stored_path == "/custom/storage/document.txt"
    assert result.source.location == "/custom/storage/document.txt"
