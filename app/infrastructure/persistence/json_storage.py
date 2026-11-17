
import json
import os
import tempfile

from pathlib import Path
from threading import RLock
from typing import Any, ClassVar


class JSONStorage:
    """Provides thread-safe and atomic JSON file operations."""

    # Shared across all JSONStorage instances in this process.
    _lock: ClassVar[RLock] = RLock()

    def __init__(
        self,
        storage_dir: str = "data/knowledge/storage",
    ) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, filename: str) -> Path:
        """Validate and resolve a storage filename."""

        if not filename or Path(filename).name != filename:
            raise ValueError("Invalid JSON storage filename.")

        if filename in {".", ".."}:
            raise ValueError("Invalid JSON storage filename.")

        return self.storage_dir / filename

    def read(self, filename: str) -> list[dict[str, Any]]:
        path = self._get_path(filename)

        with self._lock:
            if not path.exists():
                return []

            try:
                with path.open("r", encoding="utf-8") as file:
                    data = json.load(file)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON storage file: {filename}"
                ) from exc

            if not isinstance(data, list):
                raise ValueError(
                    f"Expected a JSON list in {filename}"
                )

            if not all(isinstance(item, dict) for item in data):
                raise ValueError(
                    f"Expected JSON objects in {filename}"
                )

            return data

    def write(
        self,
        filename: str,
        data: list[dict[str, Any]],
    ) -> None:
        path = self._get_path(filename)

        if not isinstance(data, list):
            raise ValueError("JSON storage data must be a list.")

        if not all(isinstance(item, dict) for item in data):
            raise ValueError("JSON storage entries must be objects.")

        temporary_path: Path | None = None

        with self._lock:
            try:
                # Create a unique temporary file in the same directory.
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=self.storage_dir,
                    prefix=f".{filename}.",
                    suffix=".tmp",
                    delete=False,
                ) as file:
                    temporary_path = Path(file.name)

                    json.dump(
                        data,
                        file,
                        indent=4,
                        ensure_ascii=False,
                    )

                    file.flush()
                    os.fsync(file.fileno())

                # Atomically replace the original JSON file.
                os.replace(temporary_path, path)

            except OSError:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
                raise
