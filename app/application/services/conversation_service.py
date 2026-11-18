
from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

from app.domain.entities.conversation import Conversation
from app.domain.entities.conversation_message import ConversationMessage
from app.domain.entities.conversation_role import ConversationRole
from app.domain.entities.conversation_status import ConversationStatus
from app.infrastructure.persistence.repositories.json_conversation_repository import (
    JSONConversationRepository,
)


class ConversationService:
    """Manages conversation sessions and message history."""

    def __init__(
        self,
        repository: JSONConversationRepository | None = None,
    ) -> None:
        self._repository = repository or JSONConversationRepository()

    def create_conversation(
        self,
        title: str,
        metadata: dict[str, str] | None = None,
    ) -> Conversation:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Conversation title cannot be empty.")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Conversation metadata must be a dictionary.")

        conversation = Conversation(
            title=title.strip(),
            metadata=metadata or {},
        )

        return self._repository.save(conversation)

    def get_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        return self._repository.get_by_id(conversation_id)

    def get_all_conversations(self) -> list[Conversation]:
        return self._repository.get_all()

    def add_message(
        self,
        conversation_id: UUID,
        role: ConversationRole,
        content: str,
        metadata: dict[str, str] | None = None,
    ) -> ConversationMessage:
        if not isinstance(role, ConversationRole):
            raise ValueError("Invalid conversation message role.")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Message content cannot be empty.")

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("Message metadata must be a dictionary.")

        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise ValueError("Conversation does not exist.")

        if conversation.status != ConversationStatus.ACTIVE:
            raise ValueError("Cannot add messages to an archived conversation.")

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content.strip(),
            metadata=metadata or {},
        )

        return self._repository.add_message(message)

    def add_user_message(
        self,
        conversation_id: UUID,
        content: str,
    ) -> ConversationMessage:
        return self.add_message(
            conversation_id=conversation_id,
            role=ConversationRole.USER,
            content=content,
        )

    def add_assistant_message(
        self,
        conversation_id: UUID,
        content: str,
    ) -> ConversationMessage:
        return self.add_message(
            conversation_id=conversation_id,
            role=ConversationRole.ASSISTANT,
            content=content,
        )

    def get_messages(
        self,
        conversation_id: UUID,
    ) -> list[ConversationMessage]:
        if self.get_conversation(conversation_id) is None:
            raise ValueError("Conversation does not exist.")

        return self._repository.get_messages(conversation_id)

    def get_conversation_history(
        self,
        conversation_id: UUID,
    ) -> list[dict[str, str]]:
        messages = self.get_messages(conversation_id)

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

    def archive_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise ValueError("Conversation does not exist.")

        archived = replace(
            conversation,
            status=ConversationStatus.ARCHIVED,
            updated_at=datetime.now(timezone.utc),
        )

        return self._repository.save(archived)

    def delete_conversation(
        self,
        conversation_id: UUID,
    ) -> bool:
        return self._repository.delete(conversation_id)

    def count_conversations(self) -> int:
        return len(self.get_all_conversations())
