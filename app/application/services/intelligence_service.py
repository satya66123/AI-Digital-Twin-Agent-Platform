
from dataclasses import dataclass
from typing import Optional

from app.application.services.ai_service import AIService
from app.application.services.intelligence_context_builder import (
    IntelligenceContext,
    IntelligenceContextBuilder,
)
from app.application.services.digital_twin_personalization_service import (
    DigitalTwinPersonalizationService,
)
from app.application.services.response_quality_service import (
    ResponseQualityService,
    ResponseQualityResult,
)
from app.application.services.response_consistency_service import (
    ResponseConsistencyService,
    ResponseConsistencyResult,
)


@dataclass(frozen=True)
class IntelligenceResponse:
    query: str
    response: str
    context: IntelligenceContext
    model: str
    quality_result: Optional[ResponseQualityResult] = None
    consistency_result: Optional[ResponseConsistencyResult] = None


class IntelligenceService:
    """Generates personalized and quality-evaluated Digital Twin responses."""

    def __init__(
        self,
        ai_service: AIService,
        context_builder: IntelligenceContextBuilder,
        personalization_service: Optional[
            DigitalTwinPersonalizationService
        ] = None,
        response_quality_service: Optional[
            ResponseQualityService
        ] = None,
        response_consistency_service: Optional[
            ResponseConsistencyService
        ] = None,
    ) -> None:

        if ai_service is None:
            raise ValueError("AIService is required.")

        if context_builder is None:
            raise ValueError("IntelligenceContextBuilder is required.")

        self.ai_service = ai_service
        self.context_builder = context_builder
        self.personalization_service = personalization_service

        self.response_quality_service = (
            response_quality_service or ResponseQualityService()
        )

        self.response_consistency_service = (
            response_consistency_service
            or ResponseConsistencyService()
        )

    def generate_response(
        self,
        query: str,
        model: str,
        conversation_history: Optional[list[dict[str, str]]] = None,
    ) -> IntelligenceResponse:

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query cannot be empty.")

        if not isinstance(model, str) or not model.strip():
            raise ValueError("Model cannot be empty.")

        normalized_query = query.strip()
        normalized_model = model.strip()

        # ----------------------------------
        # Build Knowledge, Memory and
        # Conversation Context
        # ----------------------------------

        context = self.context_builder.build(
            query=normalized_query,
            conversation_history=conversation_history,
        )

        formatted_context = self.context_builder.format_context(context)

        # ----------------------------------
        # Build Personalization Context
        # ----------------------------------

        personalization_context = ""

        if self.personalization_service is not None:
            personalization_context = (
                self.personalization_service.get_personalization_context()
            )

        # ----------------------------------
        # Construct Digital Twin Prompt
        # ----------------------------------

        prompt = f"""
You are an AI Digital Twin.

Your responsibility is to provide accurate, relevant,
consistent, and personalized responses.

KNOWLEDGE, MEMORY AND CONVERSATION CONTEXT:
{formatted_context}

PERSONALIZATION CONTEXT:
{
    personalization_context
    if personalization_context
    else "No additional personalization information is available."
}

INSTRUCTIONS:

1. Use relevant knowledge and memories when answering.
2. Use conversation history to maintain continuity.
3. Personalize explanations using available profile,
   preferences, and expertise information.
4. Adapt explanations to the user's known expertise.
5. Respect stored communication preferences.
6. Do not invent personal information or preferences.
7. Acknowledge when information is unavailable.
8. Do not treat unrelated memories as relevant facts.
9. Avoid unnecessarily repeating previous answers.
10. If context conflicts or is uncertain, avoid unsupported assumptions.
11. Answer the current question directly.

CURRENT USER QUERY:
{normalized_query}

Provide a clear and helpful response.
"""

        # ----------------------------------
        # Generate AI Response
        # ----------------------------------

        response = self.ai_service.generate(
            model=normalized_model,
            prompt=prompt,
        )

        if not isinstance(response, str) or not response.strip():
            raise ValueError("AI provider returned an empty response.")

        normalized_response = response.strip()

        # ----------------------------------
        # Response Quality Evaluation
        # ----------------------------------

        quality_result = self.response_quality_service.evaluate(
            normalized_response
        )

        # ----------------------------------
        # Response Consistency Evaluation
        # ----------------------------------

        consistency_result = (
            self.response_consistency_service.evaluate(
                response=normalized_response,
                conversation_history=conversation_history,
            )
        )

        # ----------------------------------
        # Return Complete Intelligence Result
        # ----------------------------------

        return IntelligenceResponse(
            query=normalized_query,
            response=normalized_response,
            context=context,
            model=normalized_model,
            quality_result=quality_result,
            consistency_result=consistency_result,
        )

    def available_models(self) -> list[str]:

        return self.ai_service.available_models()
