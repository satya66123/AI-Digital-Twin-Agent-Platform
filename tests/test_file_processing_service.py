
import hashlib
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from app.application.services.file_processing_service import (
    FileProcessingResult,
    FileProcessingService,
)


@pytest.fixture
def document_extractor():
    extractor = Mock()
    extractor.supports.return_value = True
    return extractor


@pytest.fixture
def service(document_extractor):
    return FileProcessingService(
        document_extractor=document_extractor,
        max_file_size=1024,
    )


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello, knowledge platform!", encoding="utf-8")
    return file_path


def test_service_initialization(document_extractor):
    service = FileProcessingService(
        document_extractor=document_extractor,
        max_file_size=2048,
    )

    assert service.document_extractor is document_extractor
    assert service.max_file_size == 2048


def test_service_uses_default_max_file_size(document_extractor):
    service = FileProcessingService(
        document_extractor=document_extractor
    )

    assert service.max_file_size == 50 * 1024 * 1024


def test_service_creates_default_extractor():
    service = FileProcessingService()

    assert service.document_extractor is not None


def test_initialization_rejects_zero_max_file_size():
    with pytest.raises(ValueError, match="Maximum file size must be positive"):
        FileProcessingService(max_file_size=0)


def test_initialization_rejects_negative_max_file_size():
    with pytest.raises(ValueError, match="Maximum file size must be positive"):
        FileProcessingService(max_file_size=-1)


def test_process_returns_processing_result(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert isinstance(result, FileProcessingResult)


def test_process_returns_correct_file_path(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert result.file_path == str(sample_file.resolve())


def test_process_returns_correct_filename(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert result.filename == "sample.txt"


def test_process_returns_lowercase_file_extension(
    service,
    tmp_path,
):
    file_path = tmp_path / "sample.TXT"
    file_path.write_text("Example", encoding="utf-8")

    result = service.process(str(file_path))

    assert result.file_type == ".txt"


def test_process_returns_correct_file_size(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert result.file_size == sample_file.stat().st_size


def test_process_returns_sha256_checksum(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    expected_checksum = hashlib.sha256(
        sample_file.read_bytes()
    ).hexdigest()

    assert result.checksum == expected_checksum


def test_process_returns_supported_status(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert result.is_supported is True


def test_process_returns_utc_datetime(
    service,
    sample_file,
):
    result = service.process(str(sample_file))

    assert isinstance(result.processed_at, datetime)
    assert result.processed_at.tzinfo == timezone.utc


def test_process_calls_extractor_supports(
    service,
    document_extractor,
    sample_file,
):
    service.process(str(sample_file))

    document_extractor.supports.assert_called_once_with(".txt")


def test_process_rejects_empty_path(service):
    with pytest.raises(ValueError, match="A valid file path is required"):
        service.process("")


def test_process_rejects_whitespace_path(service):
    with pytest.raises(ValueError, match="A valid file path is required"):
        service.process("   ")


@pytest.mark.parametrize("invalid_path", [None, 123, [], {}])
def test_process_rejects_non_string_path(service, invalid_path):
    with pytest.raises(ValueError, match="A valid file path is required"):
        service.process(invalid_path)


def test_process_rejects_missing_file(service, tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="Document not found"):
        service.process(str(missing_file))


def test_process_rejects_directory(service, tmp_path):
    with pytest.raises(ValueError, match="provided path is not a file"):
        service.process(str(tmp_path))


def test_process_rejects_empty_document(service, tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_bytes(b"")

    with pytest.raises(ValueError, match="Empty documents"):
        service.process(str(empty_file))


def test_process_rejects_file_exceeding_maximum_size(
    service,
    tmp_path,
):
    large_file = tmp_path / "large.txt"
    large_file.write_bytes(b"x" * 1025)

    with pytest.raises(ValueError, match="maximum allowed size"):
        service.process(str(large_file))


def test_process_accepts_file_at_maximum_size(
    service,
    tmp_path,
):
    file_path = tmp_path / "maximum.txt"
    file_path.write_bytes(b"x" * 1024)

    result = service.process(str(file_path))

    assert result.file_size == 1024


def test_process_rejects_unsupported_format(
    service,
    document_extractor,
    tmp_path,
):
    file_path = tmp_path / "sample.exe"
    file_path.write_bytes(b"executable content")
    document_extractor.supports.return_value = False

    with pytest.raises(
        ValueError,
        match="Unsupported document format: .exe",
    ):
        service.process(str(file_path))


def test_calculate_checksum_returns_sha256(tmp_path):
    file_path = tmp_path / "checksum.txt"
    content = b"Test checksum calculation"
    file_path.write_bytes(content)

    result = FileProcessingService._calculate_checksum(file_path)

    assert result == hashlib.sha256(content).hexdigest()


def test_calculate_checksum_handles_file_larger_than_one_megabyte(
    tmp_path,
):
    file_path = tmp_path / "large_checksum.txt"
    content = b"a" * (1024 * 1024 + 100)
    file_path.write_bytes(content)

    result = FileProcessingService._calculate_checksum(file_path)

    assert result == hashlib.sha256(content).hexdigest()
