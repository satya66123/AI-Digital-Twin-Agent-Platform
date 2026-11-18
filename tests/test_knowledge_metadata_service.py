
import pytest

from app.application.services.knowledge_metadata_service import (
    KnowledgeMetadataService,
)
from app.domain.entities.knowledge_metadata import KnowledgeMetadata


@pytest.fixture
def metadata_service():
    return KnowledgeMetadataService()


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "This is sample knowledge content.",
        encoding="utf-8",
    )
    return file_path


def test_metadata_service_initialization(metadata_service):
    assert metadata_service is not None


def test_build_returns_metadata(metadata_service, sample_file):
    metadata = metadata_service.build(
        file_path=str(sample_file),
        author="Test Author",
        source_url="https://example.com",
        extracted_text="Sample knowledge content",
        checksum="abc123",
    )

    assert isinstance(metadata, KnowledgeMetadata)
    assert metadata.filename == "sample.txt"
    assert metadata.author == "Test Author"
    assert metadata.source_url == "https://example.com"
    assert metadata.metadata["checksum"] == "abc123"


def test_build_detects_file_extension(metadata_service, sample_file):
    metadata = metadata_service.build(
        file_path=str(sample_file),
    )

    assert metadata.file_type == "txt"
    assert metadata.metadata["file_extension"] == ".txt"


def test_build_detects_mime_type(metadata_service, sample_file):
    metadata = metadata_service.build(
        file_path=str(sample_file),
    )

    assert metadata.mime_type == "text/plain"


def test_build_calculates_file_size(metadata_service, sample_file):
    metadata = metadata_service.build(
        file_path=str(sample_file),
    )

    assert metadata.metadata["file_size"] == str(
        sample_file.stat().st_size
    )


def test_build_calculates_character_count(
    metadata_service,
    sample_file,
):
    text = "Sample knowledge content"

    metadata = metadata_service.build(
        file_path=str(sample_file),
        extracted_text=text,
    )

    assert metadata.metadata["character_count"] == str(len(text))


def test_build_calculates_word_count(
    metadata_service,
    sample_file,
):
    text = "Sample knowledge content"

    metadata = metadata_service.build(
        file_path=str(sample_file),
        extracted_text=text,
    )

    assert metadata.metadata["word_count"] == "3"


def test_build_preserves_extra_metadata(
    metadata_service,
    sample_file,
):
    metadata = metadata_service.build(
        file_path=str(sample_file),
        extra_metadata={
            "category": "technical",
            "department": "engineering",
        },
    )

    assert metadata.metadata["category"] == "technical"
    assert metadata.metadata["department"] == "engineering"


def test_build_handles_empty_extracted_text(
    metadata_service,
    sample_file,
):
    metadata = metadata_service.build(
        file_path=str(sample_file),
        extracted_text="",
    )

    assert "character_count" not in metadata.metadata
    assert "word_count" not in metadata.metadata


def test_build_strips_author_and_source_url(
    metadata_service,
    sample_file,
):
    metadata = metadata_service.build(
        file_path=str(sample_file),
        author=" Test Author ",
        source_url=" https://example.com ",
    )

    assert metadata.author == "Test Author"
    assert metadata.source_url == "https://example.com"


def test_merge_preserves_existing_metadata(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
        author="Original Author",
        extra_metadata={"category": "technical"},
    )

    merged = metadata_service.merge(
        original,
        {"department": "engineering"},
    )

    assert merged.author == "Original Author"
    assert merged.metadata["category"] == "technical"
    assert merged.metadata["department"] == "engineering"


def test_merge_does_not_modify_original_metadata(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
        extra_metadata={"category": "technical"},
    )

    original_metadata = dict(original.metadata)

    metadata_service.merge(
        original,
        {"department": "engineering"},
    )

    assert original.metadata == original_metadata
    assert "department" not in original.metadata


def test_merge_preserves_existing_entity_fields(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
        author="Test Author",
        source_url="https://example.com",
    )

    merged = metadata_service.merge(
        original,
        {"category": "technical"},
    )

    assert merged.filename == original.filename
    assert merged.file_type == original.file_type
    assert merged.mime_type == original.mime_type
    assert merged.language == original.language
    assert merged.author == original.author
    assert merged.source_url == original.source_url


def test_build_rejects_invalid_file_path(metadata_service):
    with pytest.raises(ValueError, match="valid file path"):
        metadata_service.build(file_path="   ")


def test_build_rejects_nonexistent_file(metadata_service, tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        metadata_service.build(file_path=str(missing_file))


def test_build_rejects_non_string_extracted_text(
    metadata_service,
    sample_file,
):
    with pytest.raises(ValueError, match="Extracted text must be a string"):
        metadata_service.build(
            file_path=str(sample_file),
            extracted_text=None,
        )


def test_build_rejects_invalid_extra_metadata(
    metadata_service,
    sample_file,
):
    with pytest.raises(ValueError, match="dictionary"):
        metadata_service.build(
            file_path=str(sample_file),
            extra_metadata="invalid",
        )


def test_build_rejects_empty_metadata_key(
    metadata_service,
    sample_file,
):
    with pytest.raises(ValueError, match="non-empty strings"):
        metadata_service.build(
            file_path=str(sample_file),
            extra_metadata={" ": "value"},
        )


def test_build_rejects_non_string_metadata_value(
    metadata_service,
    sample_file,
):
    with pytest.raises(ValueError, match="must be a string"):
        metadata_service.build(
            file_path=str(sample_file),
            extra_metadata={"category": 123},
        )


def test_merge_rejects_invalid_metadata_object(metadata_service):
    with pytest.raises(ValueError, match="valid KnowledgeMetadata"):
        metadata_service.merge(
            existing=None,
            updates={"category": "technical"},
        )


def test_merge_rejects_invalid_updates(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
    )

    with pytest.raises(ValueError, match="dictionary"):
        metadata_service.merge(original, "invalid")


def test_merge_rejects_empty_metadata_key(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
    )

    with pytest.raises(ValueError, match="non-empty strings"):
        metadata_service.merge(
            original,
            {" ": "value"},
        )


def test_merge_rejects_non_string_metadata_value(
    metadata_service,
    sample_file,
):
    original = metadata_service.build(
        file_path=str(sample_file),
    )

    with pytest.raises(ValueError, match="must be a string"):
        metadata_service.merge(
            original,
            {"category": 123},
        )
