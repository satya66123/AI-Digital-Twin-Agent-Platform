
from pathlib import Path
import mimetypes

from app.domain.entities.knowledge_metadata import KnowledgeMetadata


class KnowledgeMetadataService:
    """Builds and manages metadata for ingested knowledge documents."""

    def build(
        self,
        file_path: str,
        author: str = "",
        source_url: str = "",
        extracted_text: str = "",
        checksum: str = "",
        extra_metadata: dict[str, str] | None = None,
    ) -> KnowledgeMetadata:

        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("A valid file path is required.")

        if not isinstance(extracted_text, str):
            raise ValueError("Extracted text must be a string.")

        if not isinstance(author, str):
            raise ValueError("Author must be a string.")

        if not isinstance(source_url, str):
            raise ValueError("Source URL must be a string.")

        if not isinstance(checksum, str):
            raise ValueError("Checksum must be a string.")

        path = Path(file_path)

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(
                f"Document file not found: {file_path}"
            )

        mime_type, _ = mimetypes.guess_type(path.name)

        metadata = {
            "file_size": str(path.stat().st_size),
            "file_extension": path.suffix.lower(),
            "file_path": str(path.resolve()),
        }

        if checksum:
            metadata["checksum"] = checksum

        if extracted_text:
            metadata["character_count"] = str(len(extracted_text))
            metadata["word_count"] = str(len(extracted_text.split()))

        if extra_metadata is not None:
            if not isinstance(extra_metadata, dict):
                raise ValueError("Extra metadata must be a dictionary.")

            for key, value in extra_metadata.items():
                if not isinstance(key, str) or not key.strip():
                    raise ValueError(
                        "Metadata keys must be non-empty strings."
                    )

                if not isinstance(value, str):
                    raise ValueError(
                        f"Metadata value for '{key}' must be a string."
                    )

                metadata[key.strip()] = value

        return KnowledgeMetadata(
            filename=path.name,
            file_type=path.suffix.lower().lstrip("."),
            mime_type=mime_type or "application/octet-stream",
            author=author.strip(),
            source_url=source_url.strip(),
            metadata=metadata,
        )

    @staticmethod
    def merge(
        existing: KnowledgeMetadata,
        updates: dict[str, str],
    ) -> KnowledgeMetadata:

        if not isinstance(existing, KnowledgeMetadata):
            raise ValueError("A valid KnowledgeMetadata object is required.")

        if not isinstance(updates, dict):
            raise ValueError("Metadata updates must be a dictionary.")

        merged_metadata = dict(existing.metadata)

        for key, value in updates.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Metadata keys must be non-empty strings.")

            if not isinstance(value, str):
                raise ValueError(
                    f"Metadata value for '{key}' must be a string."
                )

            merged_metadata[key.strip()] = value

        return KnowledgeMetadata(
            filename=existing.filename,
            file_type=existing.file_type,
            mime_type=existing.mime_type,
            language=existing.language,
            author=existing.author,
            source_url=existing.source_url,
            metadata=merged_metadata,
        )
