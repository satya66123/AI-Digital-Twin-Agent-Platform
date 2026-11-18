
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ResponseQualityResult:
    is_valid: bool
    score: float
    issues: tuple[str, ...]
    suggestions: tuple[str, ...]


class ResponseQualityService:
    """Validates basic quality characteristics of AI responses."""

    def __init__(
        self,
        minimum_length: int = 2,
        maximum_repeated_sentence_ratio: float = 0.5,
    ) -> None:
        if (
            not isinstance(minimum_length, int)
            or isinstance(minimum_length, bool)
            or minimum_length < 1
        ):
            raise ValueError("minimum_length must be a positive integer.")

        if not isinstance(
            maximum_repeated_sentence_ratio, (int, float)
        ) or isinstance(maximum_repeated_sentence_ratio, bool):
            raise ValueError(
                "maximum_repeated_sentence_ratio must be numeric."
            )

        if not 0 <= maximum_repeated_sentence_ratio <= 1:
            raise ValueError(
                "maximum_repeated_sentence_ratio must be between 0 and 1."
            )

        self.minimum_length = minimum_length
        self.maximum_repeated_sentence_ratio = (
            maximum_repeated_sentence_ratio
        )

    @staticmethod
    def _extract_sentences(response: str) -> list[str]:
        return [
            sentence.strip().lower()
            for sentence in re.split(r"[.!?]+", response)
            if sentence.strip()
        ]

    def evaluate(self, response: str) -> ResponseQualityResult:
        if not isinstance(response, str):
            raise ValueError("Response must be a string.")

        issues = []
        suggestions = []

        normalized = response.strip()

        if not normalized:
            return ResponseQualityResult(
                is_valid=False,
                score=0.0,
                issues=("Response is empty.",),
                suggestions=("Generate a non-empty response.",),
            )

        if len(normalized) < self.minimum_length:
            issues.append("Response is too short.")
            suggestions.append(
                "Provide a more complete answer."
            )

        sentences = self._extract_sentences(normalized)

        if sentences:
            unique_sentences = set(sentences)
            repeated_ratio = (
                1 - len(unique_sentences) / len(sentences)
            )

            if (
                repeated_ratio
                > self.maximum_repeated_sentence_ratio
            ):
                issues.append("Response contains excessive repetition.")
                suggestions.append(
                    "Remove repeated sentences and provide distinct information."
                )

        score = max(0.0, 1.0 - (len(issues) * 0.3))

        return ResponseQualityResult(
            is_valid=not issues,
            score=round(score, 2),
            issues=tuple(issues),
            suggestions=tuple(suggestions),
        )
