
import logging
from typing import Any


class KnowledgeLogger:
    """Centralized logging for knowledge management operations."""

    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger("app.knowledge")

    def ingestion_started(self, filename: str) -> None:
        self._logger.info(
            "Knowledge ingestion started",
            extra={
                "event": "knowledge_ingestion_started",
                "filename": filename,
            },
        )

    def ingestion_completed(
        self,
        filename: str,
        source_id: str,
        item_id: str,
        chunk_count: int,
    ) -> None:
        self._logger.info(
            "Knowledge ingestion completed",
            extra={
                "event": "knowledge_ingestion_completed",
                "filename": filename,
                "source_id": source_id,
                "knowledge_item_id": item_id,
                "chunk_count": chunk_count,
            },
        )

    def ingestion_failed(
        self,
        filename: str,
        error: Exception,
    ) -> None:
        self._logger.error(
            "Knowledge ingestion failed",
            extra={
                "event": "knowledge_ingestion_failed",
                "filename": filename,
                "error_type": type(error).__name__,
            },
            exc_info=True,
        )

    def file_processing_completed(
        self,
        filename: str,
        file_size: int,
        checksum: str,
    ) -> None:
        self._logger.info(
            "File processing completed",
            extra={
                "event": "file_processing_completed",
                "filename": filename,
                "file_size": file_size,
                "checksum": checksum,
            },
        )

    def extraction_completed(
        self,
        filename: str,
        character_count: int,
    ) -> None:
        self._logger.info(
            "Document text extraction completed",
            extra={
                "event": "text_extraction_completed",
                "filename": filename,
                "character_count": character_count,
            },
        )

    def chunking_completed(
        self,
        item_id: str,
        chunk_count: int,
    ) -> None:
        self._logger.info(
            "Knowledge chunking completed",
            extra={
                "event": "knowledge_chunking_completed",
                "knowledge_item_id": item_id,
                "chunk_count": chunk_count,
            },
        )

    def storage_completed(
        self,
        entity_type: str,
        entity_id: str,
    ) -> None:
        self._logger.info(
            "Knowledge storage operation completed",
            extra={
                "event": "knowledge_storage_completed",
                "entity_type": entity_type,
                "entity_id": entity_id,
            },
        )

    def retrieval_completed(
        self,
        result_count: int,
    ) -> None:
        self._logger.info(
            "Knowledge retrieval completed",
            extra={
                "event": "knowledge_retrieval_completed",
                "result_count": result_count,
            },
        )

    def operation_failed(
        self,
        operation: str,
        error: Exception,
    ) -> None:
        self._logger.error(
            "Knowledge operation failed",
            extra={
                "event": "knowledge_operation_failed",
                "operation": operation,
                "error_type": type(error).__name__,
            },
            exc_info=True,
        )
