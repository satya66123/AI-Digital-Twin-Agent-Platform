from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.knowledge_type import KnowledgeType


@dataclass(frozen=True)
class KnowledgeSource:
    name: str
    source_type: KnowledgeType
    location: str
    source_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )