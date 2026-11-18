# Architecture Documentation

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Architecture:** Modular Layered Architecture  
**Language:** Python 3.11+  
**Frontend:** Streamlit  
**Persistence:** JSON

---

## 1. Architecture Overview

The AI Digital Twin Agent Platform follows a modular, layered architecture designed to maintain separation of concerns, extensibility, and maintainability.

The architecture separates the application into four primary layers:

1. Presentation Layer
2. Application Layer
3. Domain Layer
4. Infrastructure Layer

Each layer has clearly defined responsibilities.

## 2. High-Level Architecture

```text
                 USER
                   |
                   v
       +-----------------------+
       |   Presentation Layer  |
       |       Streamlit       |
       +-----------------------+
                   |
                   v
       +-----------------------+
       |   Application Layer   |
       |                       |
       | Agents                |
       | Services              |
       | Intelligence          |
       | Personalization       |
       | Conversation          |
       | Response Evaluation   |
       +-----------------------+
                   |
                   v
       +-----------------------+
       |     Domain Layer      |
       |                       |
       | Entities              |
       | Interfaces            |
       | Business Rules        |
       +-----------------------+
                   |
                   v
       +-----------------------+
       | Infrastructure Layer |
       |                       |
       | AI Providers          |
       | JSON Persistence      |
       | Repositories          |
       | Storage               |
       +-----------------------+
```

## 3. Presentation Layer

**Location:** `app/presentation/`

### Responsibilities

- Provide the Streamlit user interface.
- Display application pages.
- Accept user inputs.
- Allow provider and model selection.
- Display knowledge and memory information.
- Support Digital Twin conversations.
- Display generated AI responses.

The presentation layer communicates with application services rather than directly implementing business logic.

## 4. Application Layer

**Location:** `app/application/`

The application layer coordinates the platform's use cases and business workflows.

### 4.1 Agents

**Location:** `app/application/agents/`

Main agents:

| Agent | Responsibility |
|---|---|
| KnowledgeAgent | Coordinates knowledge ingestion and retrieval. |
| MemoryAgent | Coordinates memory operations and intelligence-based memory interactions. |
| DigitalTwinInteractionAgent | Manages Digital Twin conversations and multi-turn interaction. |

### 4.2 Services

**Location:** `app/application/services/`

Important services:

| Service | Responsibility |
|---|---|
| AIService | AI provider communication |
| ProviderFactory | Provider creation |
| ProviderModelService | Provider and model selection |
| KnowledgeIngestionService | Document ingestion |
| KnowledgeRetrievalService | Knowledge retrieval |
| MemoryService | Memory management |
| IntelligenceContextBuilder | Context construction |
| IntelligenceService | AI response generation |
| ConversationService | Conversation management |
| DigitalTwinPersonalizationService | Personalization context |
| ResponseQualityService | Response quality evaluation |
| ResponseConsistencyService | Response similarity evaluation |

### 4.3 Application Container

**File:** `app/application/container.py`

`ApplicationContainer` is responsible for dependency creation and injection.

It coordinates:

- Provider registration.
- AI service creation.
- Knowledge services.
- Memory services.
- Intelligence services.
- Personalization services.
- Conversation services.
- Response evaluation services.

## 5. Domain Layer

**Location:** `app/domain/`

The domain layer represents the application's core entities, interfaces, and business concepts.

### Entities

Important domain entities include:

- Memory.
- MemoryType.
- Conversation.
- ConversationMessage.
- ConversationRole.
- ConversationStatus.

### Interfaces

Provider and repository abstractions help separate business logic from infrastructure implementations.

### Responsibilities

- Define core application entities.
- Represent domain concepts.
- Define required interfaces.
- Support separation between business logic and implementation details.

## 6. Infrastructure Layer

**Location:** `app/infrastructure/`

The infrastructure layer provides external integrations and persistence implementations.

### 6.1 AI Providers

Supported providers:

- Ollama.
- OpenAI.
- Anthropic.
- Gemini.
- Mistral.
- Groq.
- Cohere.
- DeepSeek.

### 6.2 Provider Registry

The provider registry supports provider registration and discovery.

### 6.3 JSON Persistence

The application uses JSON-based persistence for:

- Knowledge data.
- Memory records.
- Conversation records.
- Conversation messages.

### 6.4 Repositories

Main repository implementations:

- JSONMemoryRepository.
- JSONConversationRepository.

## 7. Multi-Provider Architecture

The platform uses provider abstraction and factory-based creation.

```text
             IntelligenceService
                     |
                     v
                  AIService
                     |
                     v
               ProviderFactory
                     |
          +----------+----------+
          |          |          |
          v          v          v
        Ollama     OpenAI    Anthropic
          |
          +------ Gemini
          |
          +------ Mistral
          |
          +------ Groq
          |
          +------ Cohere
          |
          +------ DeepSeek
```

The provider factory creates the selected provider implementation.

This allows the application to work with multiple AI providers through a consistent application interface.

## 8. Dependency Injection

Dependency injection is managed through `ApplicationContainer`.

Example:

```python
intelligence_service = container.create_intelligence_service(
    provider_name="ollama"
)
```

The container creates the required AI service and supplies the intelligence context builder and personalization and response evaluation services.

Benefits:

- Reduced tight coupling.
- Centralized dependency creation.
- Easier component replacement.
- Improved maintainability.
- Better separation of responsibilities.

## 9. Knowledge Architecture

```text
Document Upload
      |
      v
File Validation
      |
      v
Document Extraction
      |
      v
Text Chunking
      |
      v
Metadata Processing
      |
      v
JSON Persistence
      |
      v
Knowledge Retrieval
      |
      v
Intelligence Context
```

Knowledge ingestion and retrieval are managed through dedicated application services.

## 10. Memory Architecture

```text
              MemoryService
                    |
                    v
             JSONMemoryRepository
                    |
                    v
             JSON Memory Storage
                    |
       +------------+------------+
       |            |            |
       v            v            v
   Short-Term   Long-Term    Episodic
                              |
                              v
                           Semantic
```

The four memory categories are:

- SHORT_TERM
- LONG_TERM
- EPISODIC
- SEMANTIC

MemoryService manages memory creation, retrieval, searching, updates, deletion, and consolidation.

## 11. Digital Twin Interaction Architecture

```text
             User Message
                   |
                   v
       DigitalTwinInteractionAgent
                   |
                   v
           ConversationService
                   |
                   v
          Conversation History
                   |
                   v
             IntelligenceService
                   |
         +---------+---------+
         |         |         |
         v         v         v
      Knowledge  Memory  Personalization
         |         |         |
         +---------+---------+
                   |
                   v
             AI Provider
                   |
                   v
             AI Response
                   |
                   v
          Response Evaluation
                   |
                   v
           Assistant Message
                   |
                   v
          JSON Conversation Storage
```

The interaction agent coordinates the conversation workflow and invokes intelligence generation.

## 12. Intelligence Context Architecture

The IntelligenceContextBuilder combines:

1. Current user query.
2. Relevant knowledge.
3. Relevant memories.
4. Recent conversation history.

The IntelligenceService uses this context to construct the AI prompt.

## 13. Personalization Architecture

The DigitalTwinPersonalizationService retrieves existing memories and classifies relevant information into:

- Personal profile.
- User preferences.
- Professional expertise.

The resulting personalization context is included in the intelligence prompt.

## 14. Response Evaluation Architecture

Two independent services evaluate generated responses.

### Response Quality Service

Evaluates:

- Empty responses.
- Short responses.
- Repeated sentences.

### Response Consistency Service

Evaluates:

- Lexical similarity with previous assistant responses.
- Potentially repeated answers.

These services provide advisory evaluation results. They do not constitute comprehensive semantic fact-checking.

## 15. SOLID Principles

The platform follows the five SOLID design principles.

### Single Responsibility Principle

Each service and agent has a focused responsibility.

### Open/Closed Principle

The provider architecture supports adding provider implementations through registration without redesigning the entire application.

### Liskov Substitution Principle

Implementations of provider abstractions should remain interchangeable while respecting their interface contracts.

### Interface Segregation Principle

Interfaces should expose only the operations required by their consumers.

### Dependency Inversion Principle

Application components use abstractions and injected dependencies rather than depending directly on infrastructure implementations.

## 16. Data Flow

The primary data flow is:

1. User interacts through Streamlit.
2. Application selects the AI provider and model.
3. Knowledge and memory services retrieve relevant information.
4. Conversation history is collected.
5. Personalization context is constructed.
6. IntelligenceService builds the prompt.
7. AI provider generates a response.
8. Response quality and consistency are evaluated.
9. Digital Twin interaction returns the response.
10. Conversation messages are persisted.

## 17. Architectural Benefits

- Modular development.
- Clear separation of responsibilities.
- Multiple AI provider support.
- Extensible service architecture.
- Centralized dependency management.
- JSON-based persistence.
- Reusable application services.
- Easier maintenance and future enhancements.

## 18. Future Architecture Enhancements

Potential improvements:

- Embedding-based semantic retrieval.
- Advanced semantic memory.
- More sophisticated consistency evaluation.
- Advanced profile extraction.
- Production-grade deployment architecture.
- Additional provider integrations.

These are future enhancement possibilities and are not claimed as completed v1.0.0 capabilities.

---

**Document:** ARCHITECTURE.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
