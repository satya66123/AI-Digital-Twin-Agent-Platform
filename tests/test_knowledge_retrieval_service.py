
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.services.knowledge_retrieval_service import (
    KnowledgeRetrievalService,
)
from app.domain.entities.knowledge_chunk import KnowledgeChunk


@pytest.fixture
def retrieval_setup():
    chunk_repository = MagicMock()

    chunks = [
        KnowledgeChunk(
            knowledge_item_id=uuid4(),
            content="Python is a popular programming language.",
            chunk_index=0,
            start_position=0,
            end_position=44,
            metadata={"filename": "python.txt"},
        ),
        KnowledgeChunk(
            knowledge_item_id=uuid4(),
            content="Python supports object oriented programming.",
            chunk_index=1,
            start_position=45,
            end_position=91,
            metadata={"filename": "python_oop.txt"},
        ),
        KnowledgeChunk(
            knowledge_item_id=uuid4(),
            content="Java is also a programming language.",
            chunk_index=2,
            start_position=92,
            end_position=129,
            metadata={"filename": "java.txt"},
        ),
        KnowledgeChunk(
            knowledge_item_id=uuid4(),
            content="Machine learning uses data to train models.",
            chunk_index=3,
            start_position=130,
            end_position=175,
            metadata={"filename": "ml.txt"},
        ),
    ]

    chunk_repository.get_all.return_value = chunks

    service = KnowledgeRetrievalService(
        chunk_repository=chunk_repository,
    )

    return {
        "service": service,
        "chunk_repository": chunk_repository,
        "chunks": chunks,
    }


def test_search_returns_matching_results(retrieval_setup):
    service = retrieval_setup["service"]

    results = service.search("Python")

    assert len(results) == 2
    assert all("Python" in result.content for result in results)


def test_search_returns_relevant_results_first(retrieval_setup):
    service = retrieval_setup["service"]

    results = service.search("Python programming language")

    assert len(results) >= 2

    assert results[0].relevance_score >= results[-1].relevance_score


def test_search_respects_result_limit(retrieval_setup):
    service = retrieval_setup["service"]

    results = service.search("programming", limit=2)

    assert len(results) <= 2


def test_search_returns_empty_list_for_unmatched_query(
    retrieval_setup,
):
    service = retrieval_setup["service"]

    results = service.search("unrelatedkeywordxyz")

    assert results == []


def test_search_returns_empty_list_for_empty_repository(
    retrieval_setup,
):
    components = retrieval_setup
    components["chunk_repository"].get_all.return_value = []

    results = components["service"].search("Python")

    assert results == []


def test_search_result_contains_chunk_metadata(retrieval_setup):
    service = retrieval_setup["service"]

    results = service.search("Python")

    assert results

    result = results[0]

    assert result.chunk_id is not None
    assert result.knowledge_item_id is not None
    assert result.content
    assert isinstance(result.chunk_index, int)
    assert isinstance(result.relevance_score, (int, float))
    assert isinstance(result.metadata, dict)


def test_search_uses_chunk_repository(retrieval_setup):
    components = retrieval_setup

    components["service"].search("Python")

    components["chunk_repository"].get_all.assert_called_once()


def test_search_rejects_invalid_limit(retrieval_setup):
    service = retrieval_setup["service"]

    with pytest.raises(ValueError):
        service.search("Python", limit=0)


def test_search_rejects_empty_query(retrieval_setup):
    service = retrieval_setup["service"]

    with pytest.raises(ValueError):
        service.search("   ")
