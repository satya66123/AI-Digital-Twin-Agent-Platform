
from pathlib import Path
from pypdf import PdfReader


class PDFExtractor:

    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Invalid PDF file.")

        reader = PdfReader(str(path))

        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        return "\n\n".join(pages).strip()
