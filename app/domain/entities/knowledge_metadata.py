from dataclasses import dataclass, field


@dataclass(frozen=True)
class KnowledgeMetadata:
    filename: str = ""
    file_type: str = ""
    mime_type: str = ""
    language: str = ""
    author: str = ""
    source_url: str = ""
    metadata: dict[str, str] = field(default_factory=dict)