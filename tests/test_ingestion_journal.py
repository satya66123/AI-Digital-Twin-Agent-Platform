
from uuid import uuid4

from app.infrastructure.persistence import JSONStorage
from app.infrastructure.persistence.ingestion_journal import (
    JSONIngestionJournal,
)


def create_journal(tmp_path):
    storage = JSONStorage(str(tmp_path))
    return JSONIngestionJournal(storage)


def test_start_creates_in_progress_entry(tmp_path):
    journal = create_journal(tmp_path)

    source_id = uuid4()
    item_id = uuid4()
    chunk_ids = [uuid4(), uuid4()]

    ingestion_id = journal.start(
        source_id=source_id,
        knowledge_item_id=item_id,
        chunk_ids=chunk_ids,
    )

    record = journal.get_by_id(ingestion_id)

    assert record is not None
    assert record["status"] == "in_progress"
    assert record["stage"] == "started"
    assert record["source_id"] == str(source_id)
    assert record["knowledge_item_id"] == str(item_id)
    assert record["chunk_ids"] == [str(item) for item in chunk_ids]


def test_update_stage_changes_current_stage(tmp_path):
    journal = create_journal(tmp_path)

    ingestion_id = journal.start(uuid4(), uuid4(), [])

    journal.update_stage(ingestion_id, "source_saved")

    record = journal.get_by_id(ingestion_id)

    assert record["stage"] == "source_saved"
    assert record["status"] == "in_progress"


def test_complete_marks_entry_completed(tmp_path):
    journal = create_journal(tmp_path)

    ingestion_id = journal.start(uuid4(), uuid4(), [])

    journal.complete(ingestion_id)

    record = journal.get_by_id(ingestion_id)

    assert record["status"] == "completed"
    assert record["stage"] == "completed"
    assert record["error"] is None


def test_fail_marks_entry_failed(tmp_path):
    journal = create_journal(tmp_path)

    ingestion_id = journal.start(uuid4(), uuid4(), [])

    journal.fail(ingestion_id, "Simulated failure")

    record = journal.get_by_id(ingestion_id)

    assert record["status"] == "failed"
    assert record["stage"] == "failed"
    assert record["error"] == "Simulated failure"


def test_recovered_marks_entry_recovered(tmp_path):
    journal = create_journal(tmp_path)

    ingestion_id = journal.start(uuid4(), uuid4(), [])
    journal.fail(ingestion_id, "Simulated failure")

    journal.recovered(ingestion_id)

    record = journal.get_by_id(ingestion_id)

    assert record["status"] == "recovered"
    assert record["stage"] == "recovered"
    assert record["error"] is None


def test_get_incomplete_returns_failed_and_in_progress(tmp_path):
    journal = create_journal(tmp_path)

    in_progress_id = journal.start(uuid4(), uuid4(), [])

    failed_id = journal.start(uuid4(), uuid4(), [])
    journal.fail(failed_id, "Simulated failure")

    completed_id = journal.start(uuid4(), uuid4(), [])
    journal.complete(completed_id)

    recovered_id = journal.start(uuid4(), uuid4(), [])
    journal.fail(recovered_id, "Simulated failure")
    journal.recovered(recovered_id)

    incomplete = journal.get_incomplete()
    incomplete_ids = {record["ingestion_id"] for record in incomplete}

    assert incomplete_ids == {in_progress_id, failed_id}


def test_get_by_id_returns_none_for_unknown_entry(tmp_path):
    journal = create_journal(tmp_path)

    assert journal.get_by_id("unknown-id") is None


def test_update_unknown_entry_raises_value_error(tmp_path):
    journal = create_journal(tmp_path)

    try:
        journal.update_stage("unknown-id", "source_saved")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "journal entry not found" in str(exc)
