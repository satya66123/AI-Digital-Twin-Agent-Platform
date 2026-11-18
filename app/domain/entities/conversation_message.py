
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.conversation_role import ConversationRole


@dataclass(frozen=True)
class ConversationMessage:
    conversation_id: UUID
    role: ConversationRole
    content: str
    message_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, str] = field(default_factory=dict)
