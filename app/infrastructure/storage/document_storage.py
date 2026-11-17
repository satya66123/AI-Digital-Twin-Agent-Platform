
from pathlib import Path
from uuid import uuid4
import re


class DocumentStorage:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
        ".csv",
    }

    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

    def __init__(
        self,
        storage_dir: str = "data/knowledge/uploads",
    ) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def validate(self, filename: str, file_size: int) -> None:
        if not isinstance(filename, str) or not filename.strip():
            raise ValueError("A valid filename is required.")

        if not isinstance(file_size, int) or isinstance(file_size, bool):
            raise ValueError("File size must be an integer.")

        if file_size <= 0:
            raise ValueError("Empty documents are not allowed.")

        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(
                "Document exceeds the maximum allowed size of 50 MB."
            )

        normalized_name = filename.replace("\\", "/")
        original_name = Path(normalized_name).name

        if not original_name or original_name in {".", ".."}:
            raise ValueError("Invalid document filename.")

        extension = Path(original_name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document format: {extension}"
            )

    def save(self, filename: str, content: bytes) -> str:
        if not isinstance(content, bytes):
            raise ValueError("Document content must be bytes.")

        self.validate(filename, len(content))

        normalized_name = filename.replace("\\", "/")
        original_name = Path(normalized_name).name

        safe_name = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            original_name,
        )

        extension = Path(safe_name).suffix.lower()
        stored_name = f"{uuid4().hex}{extension}"

        destination = self.storage_dir / stored_name
        temporary = destination.with_suffix(
            destination.suffix + ".tmp"
        )

        try:
            temporary.write_bytes(content)
            temporary.replace(destination)

        except OSError:
            temporary.unlink(missing_ok=True)
            raise

        return str(destination)
