
from dataclasses import dataclass
from uuid import UUID

from app.application.services.conversation_service import ConversationService
from app.application.services.intelligence_service import IntelligenceService
from app.domain.entities.conversation import Conversation
from app.domain.entities.conversation_message import ConversationMessage


@dataclass(frozen=True)
class DigitalTwinInteractionResult:
    conversation: Conversation
    user_message: ConversationMessage
    assistant_message: ConversationMessage
    response: str
    history: list[dict[str, str]]


class DigitalTwinInteractionAgent:
    """Coordinates context-aware Digital Twin conversations."""

    def __init__(
        self,
        conversation_service: ConversationService,
        intelligence_service: IntelligenceService,
        history_limit: int = 10,
    ) -> None:
        if history_limit <= 0:
            raise ValueError("History limit must be positive.")

        self._conversation_service = conversation_service
        self._intelligence_service = intelligence_service
        self._history_limit = history_limit

    def start_conversation(
        self,
        title: str = "New Digital Twin Conversation",
    ) -> Conversation:
        return self._conversation_service.create_conversation(title)

    def send_message(
        self,
        conversation_id: UUID,
        message: str,
        model: str,
    ) -> DigitalTwinInteractionResult:
        if not isinstance(message, str) or not message.strip():
            raise ValueError("User message cannot be empty.")

        if not isinstance(model, str) or not model.strip():
            raise ValueError("AI model cannot be empty.")

        conversation = self._conversation_service.get_conversation(
            conversation_id
        )

        if conversation is None:
            raise ValueError("Conversation does not exist.")

        # Retrieve previous conversation history before saving this message.
        previous_history = self._conversation_service.get_conversation_history(
            conversation_id
        )

        # Save the user's message.
        user_message = self._conversation_service.add_user_message(
            conversation_id,
            message.strip(),
        )

        # Use only the most recent messages for conversational context.
        recent_history = previous_history[-self._history_limit:]

        history_context = "\n".join(
            f"{item['role'].upper()}: {item['content']}"
            for item in recent_history
        )

        interaction_prompt = (
            "You are an AI Digital Twin having an ongoing conversation.\n"
            "Use the previous conversation as context when relevant.\n"
            "Do not repeat previous answers unnecessarily.\n\n"
            f"Previous Conversation:\n{history_context or 'No previous messages.'}\n\n"
            f"Current User Message:\n{message.strip()}\n\n"
            "Respond naturally and directly to the current user message."
        )

        # Reuse Phase 2 intelligence, knowledge and memory capabilities.
        intelligence_result = self._intelligence_service.generate_response(
            query=interaction_prompt,
            model=model.strip(),
        )

        response = intelligence_result.response

        # Save the assistant's response.
        assistant_message = self._conversation_service.add_assistant_message(
            conversation_id,
            response,
        )

        updated_history = self._conversation_service.get_conversation_history(
            conversation_id
        )

        updated_conversation = self._conversation_service.get_conversation(
            conversation_id
        )

        if updated_conversation is None:
            raise RuntimeError("Conversation could not be retrieved.")

        return DigitalTwinInteractionResult(
            conversation=updated_conversation,
            user_message=user_message,
            assistant_message=assistant_message,
            response=response,
            history=updated_history,
        )

    def get_conversation_history(
        self,
        conversation_id: UUID,
    ) -> list[dict[str, str]]:
        return self._conversation_service.get_conversation_history(
            conversation_id
        )

    def get_all_conversations(self) -> list[Conversation]:
        return self._conversation_service.get_all_conversations()

    def archive_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:
        return self._conversation_service.archive_conversation(
            conversation_id
        )

    def delete_conversation(
        self,
        conversation_id: UUID,
    ) -> bool:
        return self._conversation_service.delete_conversation(
            conversation_id
        )
