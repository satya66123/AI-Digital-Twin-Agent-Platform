
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ResponseConsistencyResult:
    is_consistent: bool
    similarity_score: float
    repeated_responses: tuple[str, ...]
    warnings: tuple[str, ...]


class ResponseConsistencyService:
    """Checks new responses against previous assistant responses."""

    def __init__(
        self,
        similarity_threshold: float = 0.85,
    ) -> None:
        if (
            not isinstance(similarity_threshold, (int, float))
            or isinstance(similarity_threshold, bool)
        ):
            raise ValueError("similarity_threshold must be numeric.")

        if not 0 <= similarity_threshold <= 1:
            raise ValueError(
                "similarity_threshold must be between 0 and 1."
            )

        self.similarity_threshold = float(similarity_threshold)

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return " ".join(text.split())

    @classmethod
    def _similarity(cls, first: str, second: str) -> float:
        first_words = set(cls._normalize(first).split())
        second_words = set(cls._normalize(second).split())

        if not first_words or not second_words:
            return 0.0

        intersection = first_words.intersection(second_words)
        union = first_words.union(second_words)

        return len(intersection) / len(union)

    def evaluate(
        self,
        response: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> ResponseConsistencyResult:

        if not isinstance(response, str) or not response.strip():
            raise ValueError("Response cannot be empty.")

        if conversation_history is None:
            conversation_history = []

        if not isinstance(conversation_history, list):
            raise ValueError("Conversation history must be a list.")

        assistant_messages = []

        for message in conversation_history:
            if not isinstance(message, dict):
                raise ValueError(
                    "Each conversation history item must be a dictionary."
                )

            role = message.get("role")
            content = message.get("content")

            if role == "assistant" and isinstance(content, str):
                if content.strip():
                    assistant_messages.append(content.strip())

        similarities = [
            (previous, self._similarity(response, previous))
            for previous in assistant_messages
        ]

        repeated_responses = tuple(
            previous
            for previous, score in similarities
            if score >= self.similarity_threshold
        )

        highest_similarity = max(
            (score for _, score in similarities),
            default=0.0,
        )

        warnings = []

        if repeated_responses:
            warnings.append(
                "The response is highly similar to a previous assistant response."
            )

        return ResponseConsistencyResult(
            is_consistent=not bool(repeated_responses),
            similarity_score=round(highest_similarity, 3),
            repeated_responses=repeated_responses,
            warnings=tuple(warnings),
        )
