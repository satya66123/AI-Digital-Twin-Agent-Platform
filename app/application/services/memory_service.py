
import re
from uuid import UUID

from app.domain.entities.memory import Memory
from app.domain.entities.memory_type import MemoryType
from app.infrastructure.persistence.repositories.json_memory_repository import (
    JSONMemoryRepository,
)


class MemoryService:
    """Manages Digital Twin memory operations and intelligent retrieval."""

    _STOP_WORDS = {
        "a", "an", "the", "is", "are", "was", "were",
        "am", "be", "been", "being", "to", "of", "in",
        "on", "at", "for", "from", "with", "by", "as",
        "and", "or", "but", "if", "then", "this", "that",
        "these", "those", "it", "its", "my", "me", "i",
        "you", "your", "we", "our", "they", "them",
        "what", "which", "who", "when", "where", "why",
        "how", "do", "does", "did", "can", "could",
        "would", "should", "will", "about",
    }

    def __init__(
        self,
        repository: JSONMemoryRepository | None = None,
    ) -> None:
        self.repository = repository or JSONMemoryRepository()

    # ==================================
    # Memory Creation
    # ==================================

    def create_memory(
        self,
        content: str,
        memory_type: MemoryType,
        metadata: dict[str, str] | None = None,
    ) -> Memory:

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Memory content cannot be empty.")

        if not isinstance(memory_type, MemoryType):
            raise ValueError("A valid memory type is required.")

        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValueError("Memory metadata must be a dictionary.")

            for key, value in metadata.items():
                if not isinstance(key, str) or not key.strip():
                    raise ValueError(
                        "Metadata keys must be non-empty strings."
                    )

                if not isinstance(value, str):
                    raise ValueError(
                        "Metadata values must be strings."
                    )

        memory = Memory(
            content=content.strip(),
            memory_type=memory_type,
            metadata=metadata or {},
        )

        return self.repository.save(memory)

    # ==================================
    # Memory Retrieval
    # ==================================

    def get_memory(self, memory_id: UUID) -> Memory | None:

        if not isinstance(memory_id, UUID):
            raise ValueError("A valid memory ID is required.")

        return self.repository.get_by_id(memory_id)

    def get_all_memories(self) -> list[Memory]:
        return self.repository.get_all()

    def get_memories_by_type(
        self,
        memory_type: MemoryType,
    ) -> list[Memory]:

        if not isinstance(memory_type, MemoryType):
            raise ValueError("A valid memory type is required.")

        return self.repository.get_by_type(memory_type)

    # ==================================
    # Memory Update
    # ==================================

    def update_memory(self, memory: Memory) -> Memory:

        if not isinstance(memory, Memory):
            raise ValueError("A valid Memory object is required.")

        existing = self.repository.get_by_id(memory.memory_id)

        if existing is None:
            raise ValueError("Memory not found.")

        return self.repository.save(memory)

    # ==================================
    # Memory Deletion
    # ==================================

    def delete_memory(self, memory_id: UUID) -> bool:

        if not isinstance(memory_id, UUID):
            raise ValueError("A valid memory ID is required.")

        return self.repository.delete(memory_id)

    def count_memories(self) -> int:
        return len(self.repository.get_all())

    # ==================================
    # Short-Term Memory
    # ==================================

    def create_short_term_memory(
        self,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> Memory:

        return self.create_memory(
            content=content,
            memory_type=MemoryType.SHORT_TERM,
            metadata=metadata,
        )

    def get_short_term_memories(self) -> list[Memory]:
        return self.get_memories_by_type(MemoryType.SHORT_TERM)

    def clear_short_term_memories(self) -> int:

        memories = self.get_short_term_memories()
        deleted_count = 0

        for memory in memories:
            if self.delete_memory(memory.memory_id):
                deleted_count += 1

        return deleted_count

    # ==================================
    # Long-Term Memory
    # ==================================

    def create_long_term_memory(
        self,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> Memory:

        return self.create_memory(
            content=content,
            memory_type=MemoryType.LONG_TERM,
            metadata=metadata,
        )

    def get_long_term_memories(self) -> list[Memory]:
        return self.get_memories_by_type(MemoryType.LONG_TERM)

    # ==================================
    # Advanced Memory Search
    # ==================================

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text for consistent matching."""

        return " ".join(
            re.findall(r"\w+", text.lower())
        )

    @classmethod
    def _extract_keywords(cls, text: str) -> set[str]:
        """Extract meaningful keywords from text."""

        words = set(re.findall(r"\w+", text.lower()))

        return {
            word
            for word in words
            if word not in cls._STOP_WORDS and len(word) > 1
        }

    @classmethod
    def _calculate_relevance(
        cls,
        query: str,
        memory: Memory,
    ) -> float:
        """Calculate keyword and phrase relevance."""

        query_words = cls._extract_keywords(query)
        content_words = cls._extract_keywords(memory.content)

        if not query_words or not content_words:
            return 0.0

        matched_words = query_words.intersection(content_words)

        if not matched_words:
            return 0.0

        # Keyword coverage.
        coverage = len(matched_words) / len(query_words)

        # Keyword precision.
        precision = len(matched_words) / len(content_words)

        # Weighted relevance score.
        score = (
            coverage * 0.65
            + precision * 0.35
        )

        normalized_query = cls._normalize_text(query)
        normalized_content = cls._normalize_text(memory.content)

        # Reward an exact phrase match.
        if normalized_query in normalized_content:
            score += 0.30

        # Reward complete keyword matches.
        if query_words.issubset(content_words):
            score += 0.20

        return score

    def search_memories(
        self,
        query: str,
        limit: int | None = None,
        memory_types: list[MemoryType] | None = None,
        deduplicate: bool = True,
    ) -> list[Memory]:
        """
        Retrieve memories ranked by relevance.

        Args:
            query: User search query.
            limit: Maximum number of results. None returns all matches.
            memory_types: Optional memory type filters.
            deduplicate: Remove identical memory content.

        Returns:
            Memories ordered by relevance.
        """

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if limit is not None:
            if (
                not isinstance(limit, int)
                or isinstance(limit, bool)
                or limit <= 0
            ):
                raise ValueError("Search limit must be positive.")

        if memory_types is not None:
            if not isinstance(memory_types, list):
                raise ValueError("Memory types must be a list.")

            if not all(
                isinstance(item, MemoryType)
                for item in memory_types
            ):
                raise ValueError("Invalid memory type filter.")

        normalized_query = query.strip()

        memories = self.get_all_memories()

        # ----------------------------------
        # Type-Aware Filtering
        # ----------------------------------

        if memory_types is not None:
            allowed_types = set(memory_types)

            memories = [
                memory
                for memory in memories
                if memory.memory_type in allowed_types
            ]

        # ----------------------------------
        # Relevance Scoring
        # ----------------------------------

        scored_memories = []

        for memory in memories:

            score = self._calculate_relevance(
                normalized_query,
                memory,
            )

            if score > 0:
                scored_memories.append(
                    (score, memory)
                )

        # ----------------------------------
        # Prioritize Relevant Memories
        # ----------------------------------

        scored_memories.sort(
            key=lambda item: (
                item[0],
                item[1].created_at.timestamp(),
            ),
            reverse=True,
        )

        # ----------------------------------
        # Duplicate Filtering
        # ----------------------------------

        results = []
        seen_content = set()

        for _, memory in scored_memories:

            normalized_content = self._normalize_text(
                memory.content
            )

            if deduplicate:
                if normalized_content in seen_content:
                    continue

                seen_content.add(normalized_content)

            results.append(memory)

            if limit is not None and len(results) >= limit:
                break

        return results

    # ==================================
    # Memory Consolidation
    # ==================================

    def consolidate_short_term_memories(self) -> int:

        short_term_memories = self.get_short_term_memories()
        consolidated_count = 0

        for memory in short_term_memories:

            long_term_memory = Memory(
                content=memory.content,
                memory_type=MemoryType.LONG_TERM,
                metadata={
                    **memory.metadata,
                    "consolidated_from": str(memory.memory_id),
                },
            )

            self.repository.save(long_term_memory)

            if self.delete_memory(memory.memory_id):
                consolidated_count += 1

        return consolidated_count
