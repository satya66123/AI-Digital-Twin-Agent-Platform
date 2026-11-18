
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.application.agents.knowledge_agent import (
    KnowledgeAgent,
)


@pytest.fixture
def knowledge_agent_setup():
    ingestion_service = MagicMock()
    retrieval_service = MagicMock()

    agent = KnowledgeAgent(
        ingestion_service=ingestion_service,
        retrieval_service=retrieval_service,
    )

    return {
        "agent": agent,
        "ingestion_service": ingestion_service,
        "retrieval_service": retrieval_service,
    }


def test_agent_initialization(knowledge_agent_setup):
    agent = knowledge_agent_setup["agent"]

    assert agent is not None


def test_ingest_document_delegates_to_ingestion_service(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup
    expected_result = SimpleNamespace(
        source_id="source-1",
        knowledge_item_id="item-1",
        chunk_count=3,
    )

    components["ingestion_service"].ingest_document.return_value = (
        expected_result
    )

    result = components["agent"].ingest_document(
        filename="document.txt",
        content=b"Knowledge content",
        author="Test Author",
        source_url="https://example.com",
    )

    assert result == expected_result

    components["ingestion_service"].ingest_document.assert_called_once_with(
        filename="document.txt",
        content=b"Knowledge content",
        author="Test Author",
        source_url="https://example.com",
    )


def test_search_knowledge_delegates_to_retrieval_service(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup
    expected_results = [
        SimpleNamespace(content="Python knowledge"),
    ]

    components["retrieval_service"].search.return_value = expected_results

    results = components["agent"].search_knowledge(
        query="Python",
        limit=5,
    )

    assert results == expected_results

    components["retrieval_service"].search.assert_called_once_with(
        query="Python",
        limit=5,
    )


def test_retrieve_context_returns_knowledge_context(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup

    results = [
        SimpleNamespace(content="Python is a programming language."),
        SimpleNamespace(content="Python supports multiple paradigms."),
    ]

    components["retrieval_service"].search.return_value = results

    context = components["agent"].retrieve_context(
        query="Python",
        limit=5,
    )

    assert context.query == "Python"
    assert context.results == results
    assert context.result_count == 2
    assert "Python is a programming language." in context.context_text
    assert "Python supports multiple paradigms." in context.context_text


def test_retrieve_context_handles_no_results(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup
    components["retrieval_service"].search.return_value = []

    context = components["agent"].retrieve_context(
        query="Unknown topic",
    )

    assert context.query == "Unknown topic"
    assert context.results == []
    assert context.result_count == 0
    assert context.context_text == ""


def test_has_knowledge_returns_true_when_results_exist(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup

    components["retrieval_service"].search.return_value = [
        SimpleNamespace(content="Relevant knowledge"),
    ]

    assert components["agent"].has_knowledge("Python") is True


def test_has_knowledge_returns_false_when_no_results(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup
    components["retrieval_service"].search.return_value = []

    assert components["agent"].has_knowledge("Unknown topic") is False


def test_ingestion_service_error_is_propagated(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup

    components["ingestion_service"].ingest_document.side_effect = (
        ValueError("Document ingestion failed")
    )

    with pytest.raises(ValueError, match="Document ingestion failed"):
        components["agent"].ingest_document(
            filename="document.txt",
            content=b"Test content",
        )


def test_retrieval_service_error_is_propagated(
    knowledge_agent_setup,
):
    components = knowledge_agent_setup

    components["retrieval_service"].search.side_effect = (
        RuntimeError("Retrieval failed")
    )

    with pytest.raises(RuntimeError, match="Retrieval failed"):
        components["agent"].search_knowledge("Python")
