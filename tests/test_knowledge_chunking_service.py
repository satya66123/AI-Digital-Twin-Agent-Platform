
from uuid import uuid4

import pytest

from app.application.services.knowledge_chunking_service import (
    KnowledgeChunkingService,
)


@pytest.fixture
def chunking_service():
    return KnowledgeChunkingService(
        chunk_size=10,
        chunk_overlap=2,
    )


def test_chunking_service_initialization(chunking_service):
    assert chunking_service.chunk_size == 10
    assert chunking_service.chunk_overlap == 2


def test_chunk_short_text_returns_one_chunk(chunking_service):
    item_id = uuid4()

    chunks = chunking_service.chunk(
        knowledge_item_id=item_id,
        text="Hello AI",
    )

    assert len(chunks) == 1
    assert chunks[0].content == "Hello AI"


def test_chunk_long_text_creates_multiple_chunks(chunking_service):
    item_id = uuid4()

    chunks = chunking_service.chunk(
        knowledge_item_id=item_id,
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )

    assert len(chunks) == 3
    assert chunks[0].content == "ABCDEFGHIJ"
    assert chunks[1].content == "IJKLMNOPQR"
    assert chunks[2].content == "QRSTUVWXYZ"


def test_chunks_have_correct_knowledge_item_id(chunking_service):
    item_id = uuid4()

    chunks = chunking_service.chunk(
        knowledge_item_id=item_id,
        text="Knowledge chunk testing",
    )

    assert all(
        chunk.knowledge_item_id == item_id
        for chunk in chunks
    )


def test_chunk_indexes_are_sequential(chunking_service):
    chunks = chunking_service.chunk(
        knowledge_item_id=uuid4(),
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )

    indexes = [chunk.chunk_index for chunk in chunks]

    assert indexes == [0, 1, 2]


def test_chunk_positions_are_valid(chunking_service):
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunking_service.chunk(
        knowledge_item_id=uuid4(),
        text=text,
    )

    normalized_text = text.strip()

    for chunk in chunks:
        assert chunk.start_position >= 0
        assert chunk.end_position > chunk.start_position
        assert chunk.end_position <= len(normalized_text)

        assert (
            chunk.content
            == normalized_text[
                chunk.start_position:chunk.end_position
            ]
        )


def test_chunks_have_unique_ids(chunking_service):
    chunks = chunking_service.chunk(
        knowledge_item_id=uuid4(),
        text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )

    chunk_ids = [chunk.chunk_id for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_empty_text_returns_empty_list(chunking_service):
    chunks = chunking_service.chunk(
        knowledge_item_id=uuid4(),
        text="",
    )

    assert chunks == []


def test_whitespace_only_text_returns_empty_list(chunking_service):
    chunks = chunking_service.chunk(
        knowledge_item_id=uuid4(),
        text="   \n\t   ",
    )

    assert chunks == []


def test_chunk_rejects_invalid_knowledge_item_id(chunking_service):
    with pytest.raises(ValueError, match="valid knowledge item ID"):
        chunking_service.chunk(
            knowledge_item_id="invalid-id",
            text="Sample content",
        )


def test_chunk_rejects_non_string_text(chunking_service):
    with pytest.raises(ValueError, match="must be a string"):
        chunking_service.chunk(
            knowledge_item_id=uuid4(),
            text=None,
        )


def test_chunk_size_must_be_positive():
    with pytest.raises(ValueError, match="Chunk size must be positive"):
        KnowledgeChunkingService(chunk_size=0)


def test_chunk_overlap_cannot_be_negative():
    with pytest.raises(ValueError, match="cannot be negative"):
        KnowledgeChunkingService(
            chunk_size=10,
            chunk_overlap=-1,
        )


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError, match="smaller than chunk size"):
        KnowledgeChunkingService(
            chunk_size=10,
            chunk_overlap=10,
        )


def test_zero_overlap_creates_non_overlapping_chunks():
    service = KnowledgeChunkingService(
        chunk_size=5,
        chunk_overlap=0,
    )

    chunks = service.chunk(
        knowledge_item_id=uuid4(),
        text="ABCDEFGHIJ",
    )

    assert len(chunks) == 2
    assert chunks[0].content == "ABCDE"
    assert chunks[1].content == "FGHIJ"
