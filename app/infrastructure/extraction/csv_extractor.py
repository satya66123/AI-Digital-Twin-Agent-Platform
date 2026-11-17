
import csv
from pathlib import Path


class CSVExtractor:

    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {file_path}")

        if path.suffix.lower() != ".csv":
            raise ValueError("Invalid CSV file.")

        rows = []

        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.reader(file)

            for row in reader:
                rows.append(" | ".join(row))

        return "\n".join(rows).strip()
