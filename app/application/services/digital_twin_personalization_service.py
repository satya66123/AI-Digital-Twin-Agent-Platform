
from dataclasses import dataclass

from app.application.services.memory_service import MemoryService
from app.domain.entities.memory import Memory


@dataclass(frozen=True)
class PersonalizationContext:
    profile_memories: tuple[Memory, ...]
    preference_memories: tuple[Memory, ...]
    expertise_memories: tuple[Memory, ...]

    @property
    def total_memories(self) -> int:
        return (
            len(self.profile_memories)
            + len(self.preference_memories)
            + len(self.expertise_memories)
        )

    def format_context(self) -> str:
        sections = []

        if self.profile_memories:
            sections.append(
                "PERSONAL PROFILE:\n"
                + "\n".join(
                    f"- {memory.content}"
                    for memory in self.profile_memories
                )
            )

        if self.preference_memories:
            sections.append(
                "USER PREFERENCES:\n"
                + "\n".join(
                    f"- {memory.content}"
                    for memory in self.preference_memories
                )
            )

        if self.expertise_memories:
            sections.append(
                "USER EXPERTISE:\n"
                + "\n".join(
                    f"- {memory.content}"
                    for memory in self.expertise_memories
                )
            )

        return "\n\n".join(sections)


class DigitalTwinPersonalizationService:
    PROFILE_KEYWORDS = {
        "name", "age", "location", "city", "country",
        "occupation", "profession", "developer", "identity",
        "background", "personal",
    }

    PREFERENCE_KEYWORDS = {
        "prefer", "preference", "like", "dislike",
        "favorite", "favourite", "style", "format",
        "communication", "language",
    }

    EXPERTISE_KEYWORDS = {
        "experience", "expertise", "skill", "skills",
        "developer", "programming", "python", "java",
        "framework", "technology", "technical",
    }

    def __init__(self, memory_service: MemoryService) -> None:
        if memory_service is None:
            raise ValueError("MemoryService is required.")

        self.memory_service = memory_service

    @staticmethod
    def _metadata_category(memory: Memory) -> str:
        metadata = memory.metadata or {}

        for key in ("category", "memory_category", "topic"):
            value = metadata.get(key)

            if value:
                return value.strip().lower()

        return ""

    @staticmethod
    def _contains_keywords(
        content: str,
        keywords: set[str],
    ) -> bool:
        words = set(content.lower().replace("-", " ").split())
        return bool(words.intersection(keywords))

    def build_context(self) -> PersonalizationContext:
        memories = self.memory_service.get_all_memories()

        profile = []
        preferences = []
        expertise = []

        for memory in memories:
            category = self._metadata_category(memory)
            content = memory.content

            if (
                category in {"profile", "personal", "identity"}
                or self._contains_keywords(
                    content, self.PROFILE_KEYWORDS
                )
            ):
                profile.append(memory)

            if (
                category in {"preference", "preferences"}
                or self._contains_keywords(
                    content, self.PREFERENCE_KEYWORDS
                )
            ):
                preferences.append(memory)

            if (
                category in {"expertise", "skills", "professional"}
                or self._contains_keywords(
                    content, self.EXPERTISE_KEYWORDS
                )
            ):
                expertise.append(memory)

        return PersonalizationContext(
            profile_memories=tuple(profile),
            preference_memories=tuple(preferences),
            expertise_memories=tuple(expertise),
        )

    def get_personalization_context(self) -> str:
        return self.build_context().format_context()
