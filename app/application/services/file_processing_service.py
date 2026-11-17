
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone
import hashlib

from app.infrastructure.extraction import DocumentExtractor


@dataclass(frozen=True)
class FileProcessingResult:
    file_path: str
    filename: str
    file_type: str
    file_size: int
    checksum: str
    is_supported: bool
    processed_at: datetime


class FileProcessingService:
    """Validates document files and prepares them for extraction."""

    def __init__(
        self,
        document_extractor: DocumentExtractor | None = None,
        max_file_size: int = 50 * 1024 * 1024,
    ) -> None:
        if max_file_size <= 0:
            raise ValueError("Maximum file size must be positive.")

        self.document_extractor = (
            document_extractor or DocumentExtractor()
        )
        self.max_file_size = max_file_size

    def process(self, file_path: str) -> FileProcessingResult:
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("A valid file path is required.")

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError("The provided path is not a file.")

        file_size = path.stat().st_size

        if file_size <= 0:
            raise ValueError("Empty documents cannot be processed.")

        if file_size > self.max_file_size:
            raise ValueError(
                "Document exceeds the maximum allowed size."
            )

        file_type = path.suffix.lower()

        if not self.document_extractor.supports(file_type):
            raise ValueError(
                f"Unsupported document format: {file_type}"
            )

        checksum = self._calculate_checksum(path)

        return FileProcessingResult(
            file_path=str(path.resolve()),
            filename=path.name,
            file_type=file_type,
            file_size=file_size,
            checksum=checksum,
            is_supported=True,
            processed_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _calculate_checksum(path: Path) -> str:
        """Calculate SHA-256 checksum without loading the whole file."""

        digest = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()
