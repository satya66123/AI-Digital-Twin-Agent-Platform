
import re
from collections import Counter
from dataclasses import dataclass
from uuid import UUID

from app.infrastructure.logging import KnowledgeLogger

from app.domain.entities.knowledge_chunk import KnowledgeChunk
from app.domain.interfaces.knowledge_chunk_repository import (
    KnowledgeChunkRepository,
)


@dataclass(frozen=True)
class KnowledgeSearchResult:
    chunk_id: UUID
    knowledge_item_id: UUID
    content: str
    chunk_index: int
    relevance_score: float
    metadata: dict[str, str]


class KnowledgeRetrievalService:
    """Retrieves relevant knowledge chunks using keyword relevance."""

    def __init__(
        self,
        chunk_repository: KnowledgeChunkRepository,
    knowledge_logger: KnowledgeLogger | None = None,
    ) -> None:
        self.chunk_repository = chunk_repository
        self.logger = knowledge_logger or KnowledgeLogger()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[KnowledgeSearchResult]:

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError("Search limit must be an integer.")

        if limit <= 0:
            raise ValueError("Search limit must be positive.")

        query_terms = self._tokenize(query)

        if not query_terms:
            return []

        chunks = self.chunk_repository.get_all()

        scored_results = []

        for chunk in chunks:
            score = self._calculate_score(
                query_terms,
                chunk.content,
            )

            if score > 0:
                scored_results.append(
                    KnowledgeSearchResult(
                        chunk_id=chunk.chunk_id,
                        knowledge_item_id=chunk.knowledge_item_id,
                        content=chunk.content,
                        chunk_index=chunk.chunk_index,
                        relevance_score=round(score, 4),
                        metadata=chunk.metadata,
                    )
                )

        scored_results.sort(
            key=lambda result: (
                -result.relevance_score,
                str(result.knowledge_item_id),
                result.chunk_index,
            )
        )

        self.logger.retrieval_completed(
            result_count=len(scored_results[:limit])
        )

        return scored_results[:limit]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())

    @classmethod
    def _calculate_score(
        cls,
        query_terms: list[str],
        content: str,
    ) -> float:

        document_terms = Counter(cls._tokenize(content))

        if not document_terms:
            return 0.0

        query_counts = Counter(query_terms)
        score = 0.0

        for term, query_frequency in query_counts.items():
            document_frequency = document_terms.get(term, 0)

            if document_frequency:
                score += min(document_frequency, 3) * query_frequency

        return score / max(len(query_terms), 1)
