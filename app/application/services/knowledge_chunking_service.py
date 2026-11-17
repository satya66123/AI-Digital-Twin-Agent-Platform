
from uuid import UUID

from app.domain.entities.knowledge_chunk import KnowledgeChunk


class KnowledgeChunkingService:
    """Splits knowledge text into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive.")

        if chunk_overlap < 0:
            raise ValueError("Chunk overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        knowledge_item_id: UUID,
        text: str,
    ) -> list[KnowledgeChunk]:
        if not isinstance(knowledge_item_id, UUID):
            raise ValueError("A valid knowledge item ID is required.")

        if not isinstance(text, str):
            raise ValueError("Knowledge text must be a string.")

        normalized_text = text.strip()

        if not normalized_text:
            return []

        chunks: list[KnowledgeChunk] = []

        start = 0
        chunk_index = 0
        text_length = len(normalized_text)

        while start < text_length:
            end = min(
                start + self.chunk_size,
                text_length,
            )

            chunk_content = normalized_text[start:end]

            chunks.append(
                KnowledgeChunk(
                    knowledge_item_id=knowledge_item_id,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    start_position=start,
                    end_position=end,
                    metadata={
                        "chunk_size": str(len(chunk_content)),
                        "chunking_strategy": "fixed_size_overlap",
                    },
                )
            )

            if end >= text_length:
                break

            start = end - self.chunk_overlap
            chunk_index += 1

        return chunks
