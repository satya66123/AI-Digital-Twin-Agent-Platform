
from pathlib import Path

from app.domain.interfaces.document_reader import DocumentReader
from app.infrastructure.extraction.pdf_extractor import PDFExtractor
from app.infrastructure.extraction.docx_extractor import DOCXExtractor
from app.infrastructure.extraction.text_extractor import TextExtractor
from app.infrastructure.extraction.csv_extractor import CSVExtractor


class DocumentExtractor(DocumentReader):
    """Selects the appropriate extractor for a supported document."""

    def __init__(self) -> None:
        self.extractors = {
            ".pdf": PDFExtractor(),
            ".docx": DOCXExtractor(),
            ".txt": TextExtractor(),
            ".md": TextExtractor(),
            ".csv": CSVExtractor(),
        }

    def supports(self, file_type: str) -> bool:
        if not isinstance(file_type, str) or not file_type.strip():
            return False

        normalized_type = file_type.strip().lower()
        extension = (
            normalized_type
            if normalized_type.startswith(".")
            else Path(normalized_type).suffix.lower()
        )

        return extension in self.extractors

    def read(self, file_path: str) -> str:
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("A valid document path is required.")

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        extension = path.suffix.lower()
        extractor = self.extractors.get(extension)

        if extractor is None:
            raise ValueError(
                f"Unsupported document format: {extension}"
            )

        return extractor.extract(str(path))
