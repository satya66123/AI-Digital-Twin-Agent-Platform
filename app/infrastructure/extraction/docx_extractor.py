
from pathlib import Path
from docx import Document


class DOCXExtractor:

    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"DOCX not found: {file_path}")

        if path.suffix.lower() != ".docx":
            raise ValueError("Invalid DOCX file.")

        document = Document(str(path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        table_text = []

        for table in document.tables:
            for row in table.rows:
                cells = [
                    cell.text.strip()
                    for cell in row.cells
                ]
                table_text.append(" | ".join(cells))

        return "\n".join(paragraphs + table_text).strip()
