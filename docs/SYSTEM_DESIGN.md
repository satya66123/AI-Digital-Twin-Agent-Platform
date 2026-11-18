# System Design

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Architecture:** Four-Layer Modular Architecture  
**Technology:** Python, Streamlit, Generative AI, JSON

---

## 1. System Overview

The AI Digital Twin Agent Platform is designed to provide personalized, context-aware AI interactions by combining document knowledge, persistent memories, and conversation history.

The system supports eight AI providers and 30 configured models.

Its design emphasizes modularity, maintainability, separation of concerns, and extensibility.

## 2. System Architecture

The platform follows four architectural layers:

1. Presentation Layer
2. Application Layer
3. Domain Layer
4. Infrastructure Layer

```text
             USER
               |
               v
      +------------------+
      | Presentation     |
      | Streamlit UI     |
      +------------------+
               |
               v
      +------------------+
      | Application      |
      | Agents & Services|
      +------------------+
               |
               v
      +------------------+
      | Domain           |
      | Entities         |
      | Interfaces       |
      +------------------+
               ^
               |
      +------------------+
      | Infrastructure   |
      | AI Providers     |
      | JSON Repositories|
      +------------------+
```

ApplicationContainer coordinates dependency wiring between application components and infrastructure implementations.

## 3. Presentation Layer

**Technology:** Streamlit

### Responsibilities

- Present the application interface.
- Collect user inputs.
- Support provider and model selection.
- Provide access to knowledge workflows.
- Present digital twin conversations.
- Display generated responses.

The presentation layer delegates application operations to the application layer.

## 4. Application Layer

The application layer coordinates the platform's main workflows.

### 4.1 Agents

| Agent | Responsibility |
|---|---|
| KnowledgeAgent | Knowledge ingestion workflow |
| MemoryAgent | Memory operations |
| DigitalTwinInteractionAgent | Digital twin interaction |

### 4.2 Services

| Service | Responsibility |
|---|---|
| MemoryService | Memory lifecycle management |
| IntelligenceService | Context-aware response generation |
| IntelligenceContextBuilder | Context construction |
| ConversationService | Conversation lifecycle management |
| DigitalTwinPersonalizationService | Personalization categorization |
| ResponseQualityService | Response quality evaluation |
| ResponseConsistencyService | Repetition similarity evaluation |

### 4.3 ApplicationContainer

ApplicationContainer provides centralized dependency wiring and component creation.

It helps keep services independent of concrete provider and repository implementations.

## 5. Domain Layer

The domain layer defines the core concepts and abstractions of the application.

Conceptual responsibilities include:

- Knowledge-related entities.
- Memory entities.
- Conversation entities.
- Message entities.
- Provider abstractions.
- Repository interfaces.

The domain layer provides the abstractions used by higher-level application components.

## 6. Infrastructure Layer

The infrastructure layer implements external integrations and persistence.

### 6.1 AI Providers

The platform supports:

| Provider | Configured Models |
|---|---:|
| Ollama | 9 |
| OpenAI | 3 |
| Anthropic | 3 |
| Gemini | 3 |
| Mistral | 3 |
| Groq | 3 |
| Cohere | 3 |
| DeepSeek | 3 |
| **Total** | **30** |

Ollama is the preferred default provider, with `qwen2.5:1.5b` as the preferred default local model.

### 6.2 Persistence

Known JSON repository implementations:

- JSONMemoryRepository
- JSONConversationRepository

Default storage paths:

```text
data/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

Knowledge storage uses its configured persistence implementation. Its exact path should be verified in the repository.

## 7. Knowledge Ingestion Workflow

### Objective

Convert supported documents into information that can be used during contextual response generation.

### Supported formats

- PDF
- DOCX
- TXT
- Markdown
- CSV

### Logical workflow

```text
Document Input
      |
      v
Document Validation
      |
      v
Content Extraction
      |
      v
Knowledge Preparation
      |
      v
Knowledge Persistence
      |
      v
Knowledge Retrieval
      |
      v
Intelligence Context
```

This represents the logical workflow; implementation-specific processing details should be checked in the actual source code.

## 8. Memory Management Design

The platform supports four memory types:

- SHORT_TERM
- LONG_TERM
- EPISODIC
- SEMANTIC

### Memory lifecycle

```text
Memory Input
     |
     v
Memory Creation
     |
     v
Memory Persistence
     |
     v
Memory Retrieval
     |
     v
Memory Search
     |
     v
Memory Update / Delete
```

Suitable short-term memories can be consolidated into long-term memory.

MemoryService manages the memory lifecycle through the configured repository.

## 9. Intelligence and Context Design

### IntelligenceContextBuilder

The context builder combines three primary information sources:

1. Relevant knowledge.
2. Stored memories.
3. Conversation history.

### IntelligenceService

The intelligence service uses the prepared context to generate responses through the configured AI provider.

```text
Knowledge
    |
Memories
    |
Conversation History
    |
    v
IntelligenceContextBuilder
    |
    v
Prepared Context
    |
    v
IntelligenceService
    |
    v
Configured AI Provider
    |
    v
Generated Response
```

## 10. Digital Twin Personalization Design

DigitalTwinPersonalizationService categorizes stored memories into:

- Profile.
- Preferences.
- Expertise.

The service uses metadata and keyword-based matching to organize personalization information.

This information can contribute to contextual AI interactions.

## 11. Conversation Management Design

ConversationService manages conversation sessions and messages.

### Supported operations

- Create conversation.
- Add messages.
- Retrieve conversation history.
- Archive conversations.
- Delete conversations.

Conversation history is available as an input to contextual intelligence.

## 12. Response Evaluation Design

### ResponseQualityService

Evaluates response characteristics such as:

- Empty responses.
- Very short responses.
- Repeated sentences.

Provides a score, issues, and suggestions.

### ResponseConsistencyService

Uses lexical Jaccard similarity to identify potentially repetitive responses compared with previous assistant messages.

It does not provide factual contradiction detection.

## 13. End-to-End Interaction Flow

The following diagram illustrates the logical interaction sequence:

```text
User
 |
 v
Streamlit Interface
 |
 v
DigitalTwinInteractionAgent
 |
 v
ConversationService
 |
 v
IntelligenceContextBuilder
 |
 +---- Knowledge
 |
 +---- Memory
 |
 +---- Conversation History
 |
 v
IntelligenceService
 |
 v
Configured AI Provider
 |
 v
Response Evaluation
 |
 v
Conversation Update
 |
 v
Display Response
```

The precise ordering of individual evaluation and persistence operations should be confirmed against the implementation.

## 14. Configuration Design

The platform uses environment-based configuration.

Important settings include:

- Ollama base URL.
- Provider-specific model settings.
- Default translation provider.
- Default caption language.
- Cloud provider credentials.

The exact variable names should be taken from `.env.example` and the Config implementation.

## 15. Key Design Decisions

| Decision | Reason |
|---|---|
| Four-layer architecture | Separate application responsibilities |
| SOLID principles | Improve maintainability |
| Interface-based design | Reduce concrete implementation coupling |
| Dependency inversion | Depend on abstractions |
| ApplicationContainer | Centralize dependency wiring |
| JSON persistence | Lightweight data storage |
| Multi-provider support | Model flexibility |
| PyTest | Automated testing |

## 16. Scalability and Future Improvements

Potential future improvements include:

- Advanced semantic memory retrieval.
- Stronger factual contradiction detection.
- Additional persistence implementations.
- Advanced knowledge retrieval.
- Improved personalization.
- Expanded logging and monitoring.
- Multi-user scalability.

These are future opportunities rather than confirmed v1.0.0 capabilities.

## 17. Final Design Summary

The AI Digital Twin Agent Platform combines modular application architecture with multi-provider AI integration, document knowledge ingestion, persistent memory, contextual intelligence, personalization, and conversation management.

Its four-layer architecture and dependency inversion approach provide a foundation for maintainable and extensible development.

---

**Document:** SYSTEM_DESIGN.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
