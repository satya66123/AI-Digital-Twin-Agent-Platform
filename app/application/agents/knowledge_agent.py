
from dataclasses import dataclass

from app.application.services.knowledge_ingestion_service import (
    KnowledgeIngestionService,
    KnowledgeIngestionResult,
)
from app.application.services.knowledge_retrieval_service import (
    KnowledgeRetrievalService,
    KnowledgeSearchResult,
)


@dataclass(frozen=True)
class KnowledgeContext:
    query: str
    results: list[KnowledgeSearchResult]
    context_text: str
    result_count: int


class KnowledgeAgent:
    """Coordinates knowledge ingestion and retrieval."""

    def __init__(
        self,
        ingestion_service: KnowledgeIngestionService | None = None,
        retrieval_service: KnowledgeRetrievalService | None = None,
    ) -> None:
        self.ingestion_service = (
            ingestion_service or KnowledgeIngestionService()
        )

        self.retrieval_service = retrieval_service or (
            KnowledgeRetrievalService(
                self.ingestion_service.chunk_repository
            )
        )

    def ingest_document(
        self,
        filename: str,
        content: bytes,
        author: str = "",
        source_url: str = "",
    ) -> KnowledgeIngestionResult:
        """Ingest a document into the knowledge store."""

        return self.ingestion_service.ingest_document(
            filename=filename,
            content=content,
            author=author,
            source_url=source_url,
        )

    def search_knowledge(
        self,
        query: str,
        limit: int = 5,
    ) -> list[KnowledgeSearchResult]:
        """Search stored knowledge."""

        return self.retrieval_service.search(
            query=query,
            limit=limit,
        )

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
    ) -> KnowledgeContext:
        """Retrieve relevant knowledge and prepare context."""

        results = self.search_knowledge(
            query=query,
            limit=limit,
        )

        context_text = "\n\n".join(
            result.content for result in results
        )

        return KnowledgeContext(
            query=query,
            results=results,
            context_text=context_text,
            result_count=len(results),
        )

    def has_knowledge(self, query: str) -> bool:
        """Check whether relevant knowledge exists."""

        return bool(
            self.search_knowledge(query=query, limit=1)
        )
