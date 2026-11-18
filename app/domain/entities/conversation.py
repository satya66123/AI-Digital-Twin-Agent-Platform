
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.conversation_status import ConversationStatus


@dataclass(frozen=True)
class Conversation:
    title: str
    conversation_id: UUID = field(default_factory=uuid4)
    status: ConversationStatus = ConversationStatus.ACTIVE
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, str] = field(default_factory=dict)
