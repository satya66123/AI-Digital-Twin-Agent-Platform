from enum import Enum


class KnowledgeType(str, Enum):
    DOCUMENT = "document"
    TEXT = "text"
    NOTE = "note"
    WEB_PAGE = "web_page"
    CONVERSATION = "conversation"
    OTHER = "other"