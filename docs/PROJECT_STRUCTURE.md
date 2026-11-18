# Project Structure

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Architecture:** Four-Layer Modular Architecture  
**Language:** Python 3.11+

---

## 1. Overview

The AI Digital Twin Agent Platform follows a modular architecture designed around separation of concerns, SOLID principles, dependency inversion, and interface-based design.

The application is organized into four major architectural layers:

1. Presentation Layer
2. Application Layer
3. Domain Layer
4. Infrastructure Layer

Each layer has a clearly defined responsibility.

## 2. Architectural Structure

```text
AI-Digital-Twin-Agent-Platform/
│
├── Presentation Layer
│   └── Streamlit UI
│
├── Application Layer
│   ├── Agents
│   ├── Services
│   └── ApplicationContainer
│
├── Domain Layer
│   ├── Entities
│   └── Interfaces
│
├── Infrastructure Layer
│   ├── Providers
│   └── Persistence
│
├── data/
│   ├── memory/
│   │   └── memories.json
│   │
│   └── conversations/
│       └── conversations.json
│
├── tests/
│
├── config/
│
├── docs/
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

**Note:** This is a logical architectural illustration, not a verified exact filesystem listing. Refer to the actual repository for the precise directory and filename structure.

## 3. Presentation Layer

**Responsibility:** Provide the user interface and handle user interactions.

Technology:

- Streamlit

Main responsibilities:

- Display application pages.
- Collect user inputs.
- Allow provider and model selection.
- Present knowledge and conversation workflows.
- Display AI-generated responses.

The presentation layer communicates with application components rather than directly implementing business logic.

## 4. Application Layer

**Responsibility:** Coordinate application workflows and business operations.

### Agents

| Agent | Responsibility |
|---|---|
| KnowledgeAgent | Coordinates knowledge ingestion |
| MemoryAgent | Coordinates memory operations |
| DigitalTwinInteractionAgent | Coordinates digital twin interactions |

### Services

| Service | Responsibility |
|---|---|
| MemoryService | Memory lifecycle management |
| IntelligenceService | Context-aware response generation |
| IntelligenceContextBuilder | Combines knowledge, memory, and conversation context |
| ConversationService | Conversation lifecycle management |
| DigitalTwinPersonalizationService | Categorizes profile, preferences, and expertise |
| ResponseQualityService | Evaluates response quality |
| ResponseConsistencyService | Identifies potentially repetitive responses |

### ApplicationContainer

ApplicationContainer provides centralized dependency wiring and application component creation.

It connects services, repositories, and provider implementations through the application's abstractions.

## 5. Domain Layer

**Responsibility:** Represent the core concepts and abstractions of the application.

This layer contains the domain entities and interfaces used by application components.

Main conceptual areas include:

- Knowledge.
- Memory.
- Conversation.
- Messages.
- AI provider abstractions.
- Repository abstractions.

The domain layer helps prevent core application logic from becoming dependent on infrastructure-specific implementations.

## 6. Infrastructure Layer

**Responsibility:** Provide concrete implementations for external integrations and data persistence.

### AI Provider Integrations

The platform supports:

1. Ollama
2. OpenAI
3. Anthropic
4. Gemini
5. Mistral
6. Groq
7. Cohere
8. DeepSeek

There are 30 configured models across these providers.

### Persistence Implementations

Known JSON repository implementations:

- JSONMemoryRepository
- JSONConversationRepository

Default storage locations:

```text
data/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

Knowledge persistence is managed by its configured implementation; verify its actual location in the repository.

## 7. Data Directory

The application uses JSON-based persistence for important application information.

| Directory or File | Purpose |
|---|---|
| `data/memory/` | Memory storage |
| `memories.json` | Persisted memory data |
| `data/conversations/` | Conversation storage |
| `conversations.json` | Persisted conversation data |

Protect these files because they may contain personal information and conversation history.

## 8. Configuration Directory

Configuration is responsible for managing application settings and provider configuration.

Important configuration resources:

- `.env`
- `.env.example`
- Config implementation
- Provider and model settings

Keep actual credentials in the local environment and never publish them in the repository.

## 9. Tests Directory

The tests directory contains automated tests executed through PyTest.

Testing areas include:

- Agent behavior.
- Service operations.
- Memory management.
- Conversation management.
- Provider integration.
- Repository behavior.
- Context construction.
- Integrated application workflows.

Run the tests using:

```bash
pytest
```

## 10. Documentation Directory

The documentation directory contains project guides, technical references, and development records.

Documentation includes:

- API documentation.
- Architecture documentation.
- Configuration instructions.
- Installation guide.
- User guide.
- Testing guide.
- Provider guide.
- Troubleshooting guide.
- Project planning and implementation records.

## 11. Dependency Flow

The architecture follows a dependency direction based on abstractions.

```text
Presentation Layer
        |
        v
Application Layer
        |
        v
Domain Abstractions
        ^
        |
Infrastructure Implementations
```

Infrastructure implementations provide concrete behavior for the abstractions used by the application.

ApplicationContainer coordinates dependency wiring.

## 12. Architectural Benefits

- Clear separation of responsibilities.
- Easier maintenance.
- Reusable application services.
- Independent provider implementations.
- Improved testability.
- Reduced coupling.
- Easier extension of existing functionality.
- More manageable application growth.

## 13. Important Design Decisions

| Design Decision | Reason |
|---|---|
| Four-layer architecture | Organize responsibilities |
| SOLID principles | Improve maintainability |
| Interface-based design | Reduce implementation coupling |
| Dependency inversion | Depend on abstractions |
| ApplicationContainer | Centralize dependency wiring |
| JSON persistence | Lightweight data storage |
| Multi-provider integration | Provide model flexibility |
| PyTest | Automated validation |

## 14. Final Project Structure Summary

The platform separates user interaction, application workflows, domain abstractions, and infrastructure implementations.

This modular organization supports the integration of eight AI providers, knowledge ingestion, four memory types, contextual intelligence, digital twin personalization, and conversation management.

---

**Document:** PROJECT_STRUCTURE.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
