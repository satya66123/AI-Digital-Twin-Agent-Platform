
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.memory_type import MemoryType


@dataclass(frozen=True)
class Memory:
    content: str
    memory_type: MemoryType
    memory_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
