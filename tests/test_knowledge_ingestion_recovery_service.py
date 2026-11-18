
from uuid import uuid4

import pytest

from app.application.services.knowledge_ingestion_recovery_service import (
    KnowledgeIngestionRecoveryService,
)
from app.domain.entities.knowledge_source import KnowledgeSource
from app.domain.entities.knowledge_type import KnowledgeType
from app.infrastructure.persistence import JSONStorage
from app.infrastructure.persistence.ingestion_journal import (
    JSONIngestionJournal,
)
from app.infrastructure.persistence.repositories import (
    JSONKnowledgeSourceRepository,
    JSONKnowledgeRepository,
    JSONKnowledgeChunkRepository,
)

@pytest.fixture
def recovery_components(tmp_path):
    """Create repositories and recovery service using shared storage."""

    storage = JSONStorage(str(tmp_path))

    source_repository = JSONKnowledgeSourceRepository(storage)
    knowledge_repository = JSONKnowledgeRepository(storage)
    chunk_repository = JSONKnowledgeChunkRepository(storage)

    journal = JSONIngestionJournal(storage)

    recovery_service = KnowledgeIngestionRecoveryService(
        journal=journal,
        source_repository=source_repository,
        knowledge_repository=knowledge_repository,
        chunk_repository=chunk_repository,
    )

    return {
        "storage": storage,
        "source_repository": source_repository,
        "knowledge_repository": knowledge_repository,
        "chunk_repository": chunk_repository,
        "journal": journal,
        "recovery_service": recovery_service,
    }

def test_recovery_removes_partial_ingestion(recovery_components):
    """Verify that failed ingestion records are cleaned up."""

    components = recovery_components

    source_repository = components["source_repository"]
    knowledge_repository = components["knowledge_repository"]
    journal = components["journal"]
    recovery_service = components["recovery_service"]

    source = KnowledgeSource(
        name="test.txt",
        source_type=KnowledgeType.DOCUMENT,
        location="test.txt",
    )

    source_repository.save(source)

    item_id = uuid4()
    chunk_ids = [uuid4(), uuid4()]

    ingestion_id = journal.start(
        source_id=source.source_id,
        knowledge_item_id=item_id,
        chunk_ids=chunk_ids,
    )

    journal.fail(
        ingestion_id,
        "Simulated interruption",
    )

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 1
    assert result["failed_count"] == 0
    assert ingestion_id in result["recovered"]

    assert source_repository.get_by_id(source.source_id) is None
    assert knowledge_repository.get_by_id(item_id) is None

    record = journal.get_by_id(ingestion_id)

    assert record is not None
    assert record["status"] == "recovered"
    assert record["stage"] == "recovered"
    assert record["error"] is None

def test_recovery_handles_empty_journal(recovery_components):
    """Verify recovery when no incomplete operations exist."""

    recovery_service = recovery_components["recovery_service"]

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 0
    assert result["failed_count"] == 0
    assert result["recovered"] == []
    assert result["failed"] == []

def test_recovery_does_not_modify_completed_ingestion(
    recovery_components,
):
    """Completed journal entries must not be recovered."""

    components = recovery_components

    journal = components["journal"]
    recovery_service = components["recovery_service"]

    ingestion_id = journal.start(
        source_id=uuid4(),
        knowledge_item_id=uuid4(),
        chunk_ids=[],
    )

    journal.complete(ingestion_id)

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 0
    assert result["failed_count"] == 0

    record = journal.get_by_id(ingestion_id)

    assert record["status"] == "completed"

def test_recovery_handles_multiple_failed_ingestions(
    recovery_components,
):
    """Verify that multiple incomplete operations are processed."""

    components = recovery_components

    journal = components["journal"]
    recovery_service = components["recovery_service"]

    ingestion_ids = []

    for _ in range(3):
        ingestion_id = journal.start(
            source_id=uuid4(),
            knowledge_item_id=uuid4(),
            chunk_ids=[],
        )

        journal.fail(
            ingestion_id,
            "Simulated failure",
        )

        ingestion_ids.append(ingestion_id)

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 3
    assert result["failed_count"] == 0

    for ingestion_id in ingestion_ids:
        record = journal.get_by_id(ingestion_id)
        assert record["status"] == "recovered"

def test_recovery_preserves_unrelated_source(recovery_components):
    """Recovery must not delete unrelated knowledge sources."""

    components = recovery_components

    source_repository = components["source_repository"]
    journal = components["journal"]
    recovery_service = components["recovery_service"]

    unrelated_source = KnowledgeSource(
        name="unrelated.txt",
        source_type=KnowledgeType.DOCUMENT,
        location="unrelated.txt",
    )

    source_repository.save(unrelated_source)

    failed_source = KnowledgeSource(
        name="failed.txt",
        source_type=KnowledgeType.DOCUMENT,
        location="failed.txt",
    )

    source_repository.save(failed_source)

    ingestion_id = journal.start(
        source_id=failed_source.source_id,
        knowledge_item_id=uuid4(),
        chunk_ids=[],
    )

    journal.fail(
        ingestion_id,
        "Simulated failure",
    )

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 1

    assert (
        source_repository.get_by_id(unrelated_source.source_id)
        is not None
    )

    assert (
        source_repository.get_by_id(failed_source.source_id)
        is None
    )

def test_recovery_is_idempotent(recovery_components):
    """Running recovery twice must not repeat completed cleanup."""

    components = recovery_components

    journal = components["journal"]
    recovery_service = components["recovery_service"]

    ingestion_id = journal.start(
        source_id=uuid4(),
        knowledge_item_id=uuid4(),
        chunk_ids=[],
    )

    journal.fail(
        ingestion_id,
        "Simulated failure",
    )

    first_result = recovery_service.recover_incomplete_ingestions()
    second_result = recovery_service.recover_incomplete_ingestions()

    assert first_result["recovered_count"] == 1
    assert second_result["recovered_count"] == 0

    assert journal.get_by_id(ingestion_id)["status"] == "recovered"

def test_recovery_reports_repository_failure(recovery_components):
    """Verify that a failed cleanup remains recoverable."""

    components = recovery_components

    journal = components["journal"]
    recovery_service = components["recovery_service"]

    ingestion_id = journal.start(
        source_id=uuid4(),
        knowledge_item_id=uuid4(),
        chunk_ids=[],
    )

    journal.fail(
        ingestion_id,
        "Simulated ingestion failure",
    )

    def failing_delete(source_id):
        raise OSError("Simulated storage failure")

    recovery_service.source_repository.delete = failing_delete

    result = recovery_service.recover_incomplete_ingestions()

    assert result["recovered_count"] == 0
    assert result["failed_count"] == 1

    assert result["failed"][0]["ingestion_id"] == ingestion_id

    record = journal.get_by_id(ingestion_id)

    assert record["status"] == "failed"
    assert "Simulated storage failure" in record["error"]