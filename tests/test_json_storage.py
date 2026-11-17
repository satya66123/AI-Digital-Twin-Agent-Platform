
import json

import pytest

from app.infrastructure.persistence.json_storage import JSONStorage


def test_read_missing_file_returns_empty_list(tmp_path):
    storage = JSONStorage(str(tmp_path))

    assert storage.read("missing.json") == []


def test_write_and_read_json_records(tmp_path):
    storage = JSONStorage(str(tmp_path))
    records = [{"id": "1", "name": "Knowledge"}]

    storage.write("test.json", records)

    assert storage.read("test.json") == records


def test_write_replaces_existing_records(tmp_path):
    storage = JSONStorage(str(tmp_path))

    storage.write("test.json", [{"id": "1"}])
    storage.write("test.json", [{"id": "2"}])

    assert storage.read("test.json") == [{"id": "2"}]


def test_read_invalid_json_raises_value_error(tmp_path):
    storage = JSONStorage(str(tmp_path))
    (tmp_path / "invalid.json").write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON storage file"):
        storage.read("invalid.json")


def test_read_non_list_json_raises_value_error(tmp_path):
    storage = JSONStorage(str(tmp_path))
    (tmp_path / "invalid.json").write_text(
        '{"id": "1"}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Expected a JSON list"):
        storage.read("invalid.json")


def test_read_non_object_list_entry_raises_value_error(tmp_path):
    storage = JSONStorage(str(tmp_path))
    (tmp_path / "invalid.json").write_text(
        '["invalid"]',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Expected JSON objects"):
        storage.read("invalid.json")


@pytest.mark.parametrize(
    "filename",
    ["../outside.json", "nested/file.json", "", ".."],
)
def test_invalid_filename_is_rejected(tmp_path, filename):
    storage = JSONStorage(str(tmp_path))

    with pytest.raises(ValueError, match="Invalid JSON storage filename"):
        storage.read(filename)


def test_write_rejects_non_list_data(tmp_path):
    storage = JSONStorage(str(tmp_path))

    with pytest.raises(ValueError):
        storage.write("test.json", {"id": "1"})


def test_write_rejects_non_dictionary_entries(tmp_path):
    storage = JSONStorage(str(tmp_path))

    with pytest.raises(ValueError):
        storage.write("test.json", ["invalid"])
