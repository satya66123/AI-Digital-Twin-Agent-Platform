
import json
import os
import tempfile

from datetime import datetime
from pathlib import Path
from threading import RLock
from uuid import UUID

from app.domain.entities.memory import Memory
from app.domain.entities.memory_type import MemoryType


class JSONMemoryRepository:
    """Stores and retrieves memories using JSON."""

    def __init__(
        self,
        storage_path: str = "data/memory/memories.json",
    ) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._lock = RLock()

    def _read(self) -> list[dict]:
        if not self.storage_path.exists():
            return []

        try:
            with self.storage_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError("Memory storage contains invalid JSON.") from exc

        if not isinstance(data, list):
            raise ValueError("Memory storage must contain a JSON list.")

        if not all(isinstance(item, dict) for item in data):
            raise ValueError("Memory records must be JSON objects.")

        return data

    def _write(self, data: list[dict]) -> None:
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.storage_path.parent,
                suffix=".tmp",
                delete=False,
            ) as file:
                temp_path = Path(file.name)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self.storage_path)

        except OSError:
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)
            raise

    @staticmethod
    def _serialize(memory: Memory) -> dict:
        return {
            "memory_id": str(memory.memory_id),
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "metadata": memory.metadata,
            "created_at": memory.created_at.isoformat(),
            "updated_at": memory.updated_at.isoformat(),
        }

    @staticmethod
    def _deserialize(data: dict) -> Memory:
        return Memory(
            memory_id=UUID(data["memory_id"]),
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def save(self, memory: Memory) -> Memory:
        if not isinstance(memory, Memory):
            raise ValueError("A valid Memory object is required.")

        with self._lock:
            records = self._read()
            serialized = self._serialize(memory)

            for index, record in enumerate(records):
                if record.get("memory_id") == str(memory.memory_id):
                    records[index] = serialized
                    break
            else:
                records.append(serialized)

            self._write(records)

        return memory

    def get_by_id(self, memory_id: UUID) -> Memory | None:
        with self._lock:
            for record in self._read():
                if record.get("memory_id") == str(memory_id):
                    return self._deserialize(record)

        return None

    def get_all(self) -> list[Memory]:
        with self._lock:
            return [
                self._deserialize(record)
                for record in self._read()
            ]

    def get_by_type(self, memory_type: MemoryType) -> list[Memory]:
        if not isinstance(memory_type, MemoryType):
            raise ValueError("A valid memory type is required.")

        with self._lock:
            return [
                self._deserialize(record)
                for record in self._read()
                if record.get("memory_type") == memory_type.value
            ]

    def delete(self, memory_id: UUID) -> bool:
        with self._lock:
            records = self._read()
            updated_records = [
                record for record in records
                if record.get("memory_id") != str(memory_id)
            ]

            if len(updated_records) == len(records):
                return False

            self._write(updated_records)
            return True
