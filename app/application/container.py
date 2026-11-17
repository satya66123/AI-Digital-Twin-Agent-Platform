
from app.application.services.ai_service import AIService
from app.application.services.provider_factory import ProviderFactory
from app.application.services.provider_model_service import (
    ProviderModelService,
)

from app.application.agents import KnowledgeAgent

from app.application.services.knowledge_ingestion_service import (
    KnowledgeIngestionService,
)
from app.application.services.knowledge_retrieval_service import (
    KnowledgeRetrievalService,
)

from app.infrastructure.persistence import JSONStorage

from app.application.services.knowledge_ingestion_recovery_service import (
    KnowledgeIngestionRecoveryService,
)

from app.infrastructure.providers import (
    AnthropicProvider,
    CohereProvider,
    DeepSeekProvider,
    GeminiProvider,
    GroqProvider,
    MistralProvider,
    OllamaProvider,
    OpenAIProvider,
)

from app.infrastructure.providers.registry import (
    InMemoryProviderRegistry,
)


class ApplicationContainer:
    """Central application dependency container."""

    def create_knowledge_ingestion_recovery_service(
            self,
    ) -> KnowledgeIngestionRecoveryService:
        return KnowledgeIngestionRecoveryService(
            journal=self._knowledge_ingestion_service.journal,
            source_repository=self._knowledge_ingestion_service.source_repository,
            knowledge_repository=self._knowledge_ingestion_service.knowledge_repository,
            chunk_repository=self._knowledge_ingestion_service.chunk_repository,
        )

    def __init__(self) -> None:

        # ----------------------------------
        # Provider Infrastructure
        # ----------------------------------

        self._provider_registry = InMemoryProviderRegistry()
        self._provider_factory = ProviderFactory()

        self._register_providers()

        # ----------------------------------
        # Shared JSON Storage
        # ----------------------------------

        self._knowledge_storage = JSONStorage()

        # ----------------------------------
        # Knowledge Ingestion Service
        # ----------------------------------

        self._knowledge_ingestion_service = (
            KnowledgeIngestionService(
                json_storage=self._knowledge_storage,
            )
        )

        # ----------------------------------
        # Knowledge Retrieval Service
        # ----------------------------------

        self._knowledge_retrieval_service = (
            KnowledgeRetrievalService(
                chunk_repository=(
                    self._knowledge_ingestion_service.chunk_repository
                )
            )
        )

        # ----------------------------------
        # Knowledge Agent
        # ----------------------------------

        self._knowledge_agent = KnowledgeAgent(
            ingestion_service=self._knowledge_ingestion_service,
            retrieval_service=self._knowledge_retrieval_service,
        )

    # ==================================
    # Provider Registration
    # ==================================

    def _register_providers(self) -> None:

        self._provider_factory.register("ollama", OllamaProvider)
        self._provider_factory.register("openai", OpenAIProvider)
        self._provider_factory.register("anthropic", AnthropicProvider)
        self._provider_factory.register("gemini", GeminiProvider)
        self._provider_factory.register("mistral", MistralProvider)
        self._provider_factory.register("groq", GroqProvider)
        self._provider_factory.register("cohere", CohereProvider)
        self._provider_factory.register("deepseek", DeepSeekProvider)

    # ==================================
    # Provider Properties
    # ==================================

    @property
    def provider_registry(self) -> InMemoryProviderRegistry:
        return self._provider_registry

    @property
    def provider_factory(self) -> ProviderFactory:
        return self._provider_factory

    # ==================================
    # AI Services
    # ==================================

    def create_provider_model_service(
        self,
    ) -> ProviderModelService:

        return ProviderModelService(
            registry=self._provider_registry,
        )

    def create_ai_service(
        self,
        provider_name: str,
    ) -> AIService:

        provider = self._provider_factory.create(
            provider_name
        )

        return AIService(
            provider=provider,
        )

    # ==================================
    # Knowledge Services
    # ==================================

    def create_knowledge_ingestion_service(
        self,
    ) -> KnowledgeIngestionService:

        return self._knowledge_ingestion_service

    def create_knowledge_retrieval_service(
        self,
    ) -> KnowledgeRetrievalService:

        return self._knowledge_retrieval_service

    def create_knowledge_agent(
        self,
    ) -> KnowledgeAgent:

        return self._knowledge_agent

    # ==================================
    # JSON Storage
    # ==================================

    @property
    def knowledge_storage(self) -> JSONStorage:
        return self._knowledge_storage
