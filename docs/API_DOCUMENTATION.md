# API Documentation

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Language:** Python 3.11+  
**Architecture:** Layered Architecture

---

## 1. Overview

This document describes the main application services, agents, interfaces, and their responsibilities in the AI Digital Twin Agent Platform.

The platform uses an internal service-oriented application architecture. Its services communicate through Python classes and dependency injection.

The current application is not documented as a REST API; this document describes its internal application interfaces.

## 2. Application Architecture

The API and service responsibilities are organized into:

- Provider Services
- Knowledge Services
- Memory Services
- Intelligence Services
- Conversation Services
- Personalization Services
- Response Evaluation Services

## 3. Provider Services

### 3.1 AIService

**Module:** `app.application.services.ai_service`

**Responsibility:** Provides a common application interface for interacting with the selected AI provider.

Main operations:

| Method | Description |
|---|---|
| `available_models()` | Returns models exposed by the configured provider. |
| `generate(model, prompt)` | Generates a response using the selected model. |

### 3.2 ProviderFactory

**Module:** `app.application.services.provider_factory`

**Responsibility:** Creates provider instances using provider registration.

Supported providers:

- Ollama
- OpenAI
- Anthropic
- Gemini
- Mistral
- Groq
- Cohere
- DeepSeek

### 3.3 ProviderModelService

**Module:** `app.application.services.provider_model_service`

**Responsibility:** Supports provider and model selection through the provider registry.

## 4. Knowledge Services

### 4.1 KnowledgeIngestionService

**Module:** `app.application.services.knowledge_ingestion_service`

**Responsibility:** Manages document ingestion and knowledge persistence.

Core responsibilities:

- Document processing.
- Extracted content management.
- Knowledge chunk management.
- Metadata management.
- JSON persistence.

### 4.2 KnowledgeRetrievalService

**Module:** `app.application.services.knowledge_retrieval_service`

**Responsibility:** Searches stored knowledge and retrieves relevant content.

Primary operation:

- Search knowledge using a query and result limit.

### 4.3 KnowledgeIngestionRecoveryService

**Module:** `app.application.services.knowledge_ingestion_recovery_service`

**Responsibility:** Supports recovery of interrupted knowledge ingestion operations using the ingestion journal and repositories.

### 4.4 KnowledgeAgent

**Module:** `app.application.agents.knowledge_agent`

**Responsibility:** Coordinates knowledge ingestion and retrieval operations.

## 5. Memory Services

### 5.1 MemoryService

**Module:** `app.application.services.memory_service`

**Responsibility:** Manages the Digital Twin's persistent memories.

Supported memory types:

- SHORT_TERM
- LONG_TERM
- EPISODIC
- SEMANTIC

Core operations:

| Operation | Description |
|---|---|
| `create_memory()` | Creates and persists a memory. |
| `get_memory()` | Retrieves a memory by ID. |
| `get_all_memories()` | Retrieves all memories. |
| `get_memories_by_type()` | Filters memories by type. |
| `update_memory()` | Updates an existing memory. |
| `delete_memory()` | Deletes a memory. |
| `search_memories()` | Searches memories using a query. |
| `count_memories()` | Returns the number of memories. |
| `consolidate_short_term_memories()` | Consolidates short-term memories into long-term memories. |

### 5.2 MemoryAgent

**Module:** `app.application.agents.memory_agent`

**Responsibility:** Coordinates memory operations and intelligence-based memory interactions.

## 6. Intelligence Services

### 6.1 IntelligenceContextBuilder

**Module:** `app.application.services.intelligence_context_builder`

**Responsibility:** Builds the context required for Digital Twin response generation.

Context sources:

- Knowledge retrieval.
- Memory retrieval.
- Conversation history.

### 6.2 IntelligenceService

**Module:** `app.application.services.intelligence_service`

**Responsibility:** Generates AI responses using the selected provider and contextual information.

Main operation:

`generate_response(query, model, conversation_history=None)`

The response contains:

- Original query.
- Generated response.
- Intelligence context.
- Selected model.
- Response quality result.
- Response consistency result.

### 6.3 DigitalTwinPersonalizationService

**Module:** `app.application.services.digital_twin_personalization_service`

**Responsibility:** Builds personalization context from stored memories.

Personalization categories:

- Personal profile.
- User preferences.
- Professional expertise.

Main operations:

- `build_context()`
- `get_personalization_context()`

## 7. Conversation Services

### 7.1 ConversationService

**Module:** `app.application.services.conversation_service`

**Responsibility:** Manages conversation sessions and messages.

Core operations:

- Create conversations.
- Retrieve conversations.
- Add user messages.
- Add assistant messages.
- Retrieve conversation history.
- Archive conversations.
- Delete conversations.

### 7.2 DigitalTwinInteractionAgent

**Module:** `app.application.agents.digital_twin_interaction_agent`

**Responsibility:** Coordinates multi-turn Digital Twin interactions.

Core operations:

- Start a conversation.
- Send a message.
- Retrieve conversation history.
- Retrieve conversations.
- Archive conversations.
- Delete conversations.

## 8. Response Evaluation Services

### 8.1 ResponseQualityService

**Module:** `app.application.services.response_quality_service`

**Responsibility:** Evaluates basic response quality.

Checks:

- Empty responses.
- Short responses.
- Excessive sentence repetition.

Result fields:

- `is_valid`
- `score`
- `issues`
- `suggestions`

### 8.2 ResponseConsistencyService

**Module:** `app.application.services.response_consistency_service`

**Responsibility:** Compares newly generated responses with previous assistant responses.

Checks:

- Lexical similarity.
- Potentially repeated responses.

Result fields:

- `is_consistent`
- `similarity_score`
- `repeated_responses`
- `warnings`

These evaluations are heuristic checks and do not independently verify factual accuracy.

## 9. Dependency Injection

**Module:** `app.application.container`

`ApplicationContainer` manages application dependencies and creates service instances.

Important factory methods include:

- `create_ai_service()`
- `create_provider_model_service()`
- `create_knowledge_ingestion_service()`
- `create_knowledge_retrieval_service()`
- `create_knowledge_agent()`
- `create_memory_repository()`
- `create_memory_service()`
- `create_intelligence_context_builder()`
- `create_intelligence_service()`
- `create_memory_agent()`
- `create_conversation_repository()`
- `create_conversation_service()`
- `create_digital_twin_personalization_service()`
- `create_digital_twin_interaction_agent()`

## 10. Persistence Interfaces

The platform uses JSON-based repositories.

Main repositories:

- `JSONMemoryRepository`
- `JSONConversationRepository`

Knowledge persistence is managed through the knowledge ingestion and storage infrastructure.

## 11. Error Handling

Application services validate inputs and raise appropriate exceptions when required information is missing or invalid.

Examples include:

- Empty queries.
- Missing models.
- Invalid memory content.
- Invalid conversation identifiers.
- Invalid JSON persistence data.
- Invalid response inputs.

## 12. Important Notes

This document describes the known application service responsibilities and method interfaces.

It does not claim that the platform exposes HTTP endpoints, authentication routes, or external REST APIs.

For exact parameter types, return types, and exception contracts, consult the corresponding Python source files.

---

**Document:** API_DOCUMENTATION.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0