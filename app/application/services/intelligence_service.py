
from dataclasses import dataclass

from app.application.services.ai_service import AIService
from app.application.services.intelligence_context_builder import (
    IntelligenceContext,
    IntelligenceContextBuilder,
)


@dataclass(frozen=True)
class IntelligenceResponse:
    query: str
    response: str
    context: IntelligenceContext
    model: str


class IntelligenceService:
    """Generates AI responses using knowledge and memory context."""

    def __init__(
        self,
        ai_service: AIService,
        context_builder: IntelligenceContextBuilder,
    ) -> None:
        self.ai_service = ai_service
        self.context_builder = context_builder

    def generate_response(
        self,
        query: str,
        model: str,
    ) -> IntelligenceResponse:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("User query cannot be empty.")

        if not isinstance(model, str) or not model.strip():
            raise ValueError("A valid AI model is required.")

        context = self.context_builder.build(query.strip())

        formatted_context = self.context_builder.format_context(context)

        prompt = f"""
You are an AI Digital Twin.

Use the following knowledge and memory context to answer
the user's question accurately.

If the provided context does not contain sufficient information,
clearly acknowledge the limitation. Do not invent personal facts.

{formatted_context}

User Question:
{query.strip()}

Provide a clear and helpful response.
"""

        response = self.ai_service.generate(
            model=model,
            prompt=prompt,
        )

        return IntelligenceResponse(
            query=query.strip(),
            response=response,
            context=context,
            model=model,
        )

    def available_models(self) -> list[str]:
        return self.ai_service.available_models()
