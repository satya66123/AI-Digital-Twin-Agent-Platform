
from app.application.services.ai_service import AIService
from app.application.services.provider_factory import ProviderFactory
from app.application.services.provider_model_service import (
    ProviderModelService,
)

from app.application.services.response_quality_service import (
    ResponseQualityService,
)
from app.application.services.response_consistency_service import (
    ResponseConsistencyService,
)

from app.application.agents.knowledge_agent import KnowledgeAgent
from app.application.agents.memory_agent import MemoryAgent
from app.application.agents.digital_twin_interaction_agent import (
    DigitalTwinInteractionAgent,
)

from app.application.services.knowledge_ingestion_service import (
    KnowledgeIngestionService,
)
from app.application.services.knowledge_retrieval_service import (
    KnowledgeRetrievalService,
)
from app.application.services.knowledge_ingestion_recovery_service import (
    KnowledgeIngestionRecoveryService,
)

from app.application.services.memory_service import MemoryService
from app.application.services.intelligence_context_builder import (
    IntelligenceContextBuilder,
)
from app.application.services.intelligence_service import IntelligenceService
from app.application.services.conversation_service import ConversationService
from app.application.services.digital_twin_personalization_service import (
    DigitalTwinPersonalizationService,
)

from app.infrastructure.persistence import JSONStorage
from app.infrastructure.persistence.repositories.json_memory_repository import (
    JSONMemoryRepository,
)
from app.infrastructure.persistence.repositories.json_conversation_repository import (
    JSONConversationRepository,
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

    def __init__(self) -> None:

        # ----------------------------------
        # Provider Infrastructure
        # ----------------------------------

        self._provider_registry = InMemoryProviderRegistry()
        self._provider_factory = ProviderFactory()

        self._register_providers()

        # ----------------------------------
        # Shared Knowledge JSON Storage
        # ----------------------------------

        self._knowledge_storage = JSONStorage()

        # ----------------------------------
        # Knowledge Ingestion Service
        # ----------------------------------

        self._knowledge_ingestion_service = KnowledgeIngestionService(
            json_storage=self._knowledge_storage,
        )

        # ----------------------------------
        # Knowledge Retrieval Service
        # ----------------------------------

        self._knowledge_retrieval_service = KnowledgeRetrievalService(
            chunk_repository=(
                self._knowledge_ingestion_service.chunk_repository
            )
        )

        # ----------------------------------
        # Knowledge Agent
        # ----------------------------------

        self._knowledge_agent = KnowledgeAgent(
            ingestion_service=self._knowledge_ingestion_service,
            retrieval_service=self._knowledge_retrieval_service,
        )

        # ----------------------------------
        # Phase 2: Memory Infrastructure
        # ----------------------------------

        self._memory_repository = JSONMemoryRepository()

        # ----------------------------------
        # Memory Service
        # ----------------------------------

        self._memory_service = MemoryService(
            repository=self._memory_repository,
        )

        # ----------------------------------
        # Phase 4.3: Digital Twin Personalization
        # ----------------------------------

        self._digital_twin_personalization_service = (
            DigitalTwinPersonalizationService(
                memory_service=self._memory_service,
            )
        )

        # ----------------------------------
        # Intelligence Context Builder
        # ----------------------------------

        self._intelligence_context_builder = IntelligenceContextBuilder(
            knowledge_retrieval_service=self._knowledge_retrieval_service,
            memory_service=self._memory_service,
        )

        # ----------------------------------
        # Phase 3: Conversation Infrastructure
        # ----------------------------------

        self._conversation_repository = JSONConversationRepository()

        # ----------------------------------
        # Conversation Service
        # ----------------------------------

        self._conversation_service = ConversationService(
            repository=self._conversation_repository,
        )

        # ----------------------------------
        # Phase 4.4: Response Quality
        # ----------------------------------

        self._response_quality_service = ResponseQualityService()

        self._response_consistency_service = (
            ResponseConsistencyService()
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

    def create_provider_model_service(self) -> ProviderModelService:

        return ProviderModelService(
            registry=self._provider_registry,
        )

    def create_ai_service(self, provider_name: str) -> AIService:

        provider = self._provider_factory.create(provider_name)

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

    def create_knowledge_agent(self) -> KnowledgeAgent:

        return self._knowledge_agent

    # ==================================
    # Knowledge Recovery
    # ==================================

    def create_knowledge_ingestion_recovery_service(
        self,
    ) -> KnowledgeIngestionRecoveryService:

        return KnowledgeIngestionRecoveryService(
            journal=self._knowledge_ingestion_service.journal,
            source_repository=(
                self._knowledge_ingestion_service.source_repository
            ),
            knowledge_repository=(
                self._knowledge_ingestion_service.knowledge_repository
            ),
            chunk_repository=(
                self._knowledge_ingestion_service.chunk_repository
            ),
        )

    # ==================================
    # Phase 2: Memory Services
    # ==================================

    def create_memory_repository(self) -> JSONMemoryRepository:

        return self._memory_repository

    def create_memory_service(self) -> MemoryService:

        return self._memory_service

    # ==================================
    # Phase 4.3: Personalization Services
    # ==================================

    def create_digital_twin_personalization_service(
        self,
    ) -> DigitalTwinPersonalizationService:

        return self._digital_twin_personalization_service

    # ==================================
    # Phase 2: Intelligence Services
    # ==================================

    def create_intelligence_context_builder(
        self,
    ) -> IntelligenceContextBuilder:

        return self._intelligence_context_builder

    def create_intelligence_service(
            self,
            provider_name: str,
    ) -> IntelligenceService:
        ai_service = self.create_ai_service(provider_name)

        return IntelligenceService(
            ai_service=ai_service,
            context_builder=self._intelligence_context_builder,
            personalization_service=(
                self._digital_twin_personalization_service
            ),
            response_quality_service=self._response_quality_service,
            response_consistency_service=(
                self._response_consistency_service
            ),
        )

    # ==================================
    # Phase 2: Memory Agent
    # ==================================

    def create_memory_agent(self, provider_name: str) -> MemoryAgent:

        intelligence_service = self.create_intelligence_service(
            provider_name
        )

        return MemoryAgent(
            memory_service=self._memory_service,
            intelligence_service=intelligence_service,
        )

    # ==================================
    # Phase 3: Conversation Services
    # ==================================

    def create_conversation_repository(
        self,
    ) -> JSONConversationRepository:

        return self._conversation_repository

    def create_conversation_service(self) -> ConversationService:

        return self._conversation_service

    # ==================================
    # Phase 3: Digital Twin Interaction
    # ==================================

    def create_digital_twin_interaction_agent(
        self,
        provider_name: str,
        history_limit: int = 10,
    ) -> DigitalTwinInteractionAgent:

        intelligence_service = self.create_intelligence_service(
            provider_name
        )

        return DigitalTwinInteractionAgent(
            conversation_service=self._conversation_service,
            intelligence_service=intelligence_service,
            history_limit=history_limit,
        )

    # ==================================
    # JSON Storage
    # ==================================

    @property
    def knowledge_storage(self) -> JSONStorage:

        return self._knowledge_storage

    @property
    def memory_repository(self) -> JSONMemoryRepository:

        return self._memory_repository

    @property
    def conversation_repository(self) -> JSONConversationRepository:

        return self._conversation_repository
