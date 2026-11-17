
from pathlib import Path


class TextExtractor:

    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {file_path}")

        if path.suffix.lower() not in {".txt", ".md"}:
            raise ValueError("Unsupported text file format.")

        return path.read_text(
            encoding="utf-8-sig"
        ).strip()
