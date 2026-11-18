
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from threading import RLock
from uuid import UUID

from app.domain.entities.conversation import Conversation
from app.domain.entities.conversation_message import ConversationMessage
from app.domain.entities.conversation_role import ConversationRole
from app.domain.entities.conversation_status import ConversationStatus


class JSONConversationRepository:
    """JSON-based persistence for conversations and their messages."""

    def __init__(self, file_path: str | Path = "data/conversations/conversations.json"):
        self._file_path = Path(file_path)
        self._lock = RLock()
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._file_path.exists():
            self._write_data([])

    def _read_data(self) -> list[dict]:
        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError("Conversation storage contains invalid JSON.") from exc

        if not isinstance(data, list):
            raise ValueError("Conversation storage must contain a JSON list.")

        if not all(isinstance(item, dict) for item in data):
            raise ValueError("Conversation records must be JSON objects.")

        return data

    def _write_data(self, data: list[dict]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._file_path.parent,
                delete=False,
                suffix=".tmp",
            ) as file:
                temp_path = Path(file.name)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self._file_path)

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)

    @staticmethod
    def _serialize_conversation(conversation: Conversation) -> dict:
        return {
            "conversation_id": str(conversation.conversation_id),
            "title": conversation.title,
            "status": conversation.status.value,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "metadata": conversation.metadata,
            "messages": [],
        }

    @staticmethod
    def _deserialize_conversation(data: dict) -> Conversation:
        return Conversation(
            conversation_id=UUID(data["conversation_id"]),
            title=data["title"],
            status=ConversationStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def _serialize_message(message: ConversationMessage) -> dict:
        return {
            "message_id": str(message.message_id),
            "conversation_id": str(message.conversation_id),
            "role": message.role.value,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "metadata": message.metadata,
        }

    @staticmethod
    def _deserialize_message(data: dict) -> ConversationMessage:
        return ConversationMessage(
            message_id=UUID(data["message_id"]),
            conversation_id=UUID(data["conversation_id"]),
            role=ConversationRole(data["role"]),
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
        )

    def save(self, conversation: Conversation) -> Conversation:
        with self._lock:
            data = self._read_data()
            conversation_id = str(conversation.conversation_id)

            existing = next(
                (
                    item for item in data
                    if item["conversation_id"] == conversation_id
                ),
                None,
            )

            record = self._serialize_conversation(conversation)

            if existing:
                record["messages"] = existing.get("messages", [])
                index = data.index(existing)
                data[index] = record
            else:
                data.append(record)

            self._write_data(data)

        return conversation

    def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        with self._lock:
            data = self._read_data()

            for item in data:
                if item["conversation_id"] == str(conversation_id):
                    return self._deserialize_conversation(item)

        return None

    def get_all(self) -> list[Conversation]:
        with self._lock:
            data = self._read_data()
            return [self._deserialize_conversation(item) for item in data]

    def add_message(self, message: ConversationMessage) -> ConversationMessage:
        with self._lock:
            data = self._read_data()
            conversation_id = str(message.conversation_id)

            for item in data:
                if item["conversation_id"] == conversation_id:
                    messages = item.setdefault("messages", [])
                    messages.append(self._serialize_message(message))
                    item["updated_at"] = message.created_at.isoformat()
                    self._write_data(data)
                    return message

        raise ValueError("Conversation does not exist.")

    def get_messages(self, conversation_id: UUID) -> list[ConversationMessage]:
        with self._lock:
            data = self._read_data()

            for item in data:
                if item["conversation_id"] == str(conversation_id):
                    return [
                        self._deserialize_message(message)
                        for message in item.get("messages", [])
                    ]

        return []

    def delete(self, conversation_id: UUID) -> bool:
        with self._lock:
            data = self._read_data()
            updated_data = [
                item for item in data
                if item["conversation_id"] != str(conversation_id)
            ]

            if len(updated_data) == len(data):
                return False

            self._write_data(updated_data)
            return True
