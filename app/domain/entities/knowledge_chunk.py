from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class KnowledgeChunk:
    knowledge_item_id: UUID
    content: str
    chunk_index: int
    start_position: int = 0
    end_position: int = 0
    metadata: dict[str, str] = field(default_factory=dict)
    chunk_id: UUID = field(default_factory=uuid4)