# AI Digital Twin Agent Platform

An AI-powered Digital Twin Agent Platform designed to build, understand, learn, remember, and interact through an evolving digital representation of an individual.

The platform is designed as a **multi-provider, multi-model AI system** with a SOLID, extensible architecture that can evolve from foundational knowledge ingestion into long-term memory, intelligent interaction, and advanced digital-twin capabilities.

---

## 🚀 Project Status

**Current Status: Phase 0 — COMPLETE ✅**

```text
Phase 0 → General Foundation                 ✅ COMPLETE
Phase 1 → Knowledge Ingestion Process        ⏳ NEXT
Phase 2 → Intelligence & Memory Process      ⏳
Phase 3 → Digital Twin Interaction Process   ⏳
Phase 4 → Validation & Advanced Intelligence ⏳
```

Development follows:

```text
PLAN
  ↓
DESIGN
  ↓
IMPLEMENT
  ↓
TEST
  ↓
FIX
  ↓
STABILIZE
  ↓
DOCUMENT
  ↓
NEXT PHASE
```

> Phase 1 development begins after the completion and review of Phase 0.

---

# 🎯 Vision

The goal of this project is to create an intelligent digital representation capable of progressively understanding:

* Personal knowledge
* Documents
* Preferences
* Experiences
* Communication patterns
* Decisions
* Memories
* Context
* Behavioral patterns
* Interactions

The Digital Twin will evolve through multiple stages rather than being implemented as a single monolithic AI application.

---

# 🏗️ Architecture

The platform follows a layered architecture based on **SOLID principles**, dependency inversion, interfaces, dependency injection, and replaceable infrastructure implementations.

```text
┌──────────────────────────────────────────────┐
│              Presentation Layer              │
│              Streamlit Application           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             Application Layer                │
│       Services / Agents / Orchestration      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                Domain Layer                  │
│       Entities / Interfaces / Services       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           Infrastructure Layer               │
│ AI Providers / Clients / Storage / Adapters  │
└──────────────────────────────────────────────┘
```

---

# 🧠 Multi-Provider AI Architecture

The platform supports **8 AI providers and 30 configured models**.

## Providers

| Provider  | Models |
| --------- | -----: |
| Ollama    |      9 |
| OpenAI    |      3 |
| Anthropic |      3 |
| Gemini    |      3 |
| Mistral   |      3 |
| Groq      |      3 |
| Cohere    |      3 |
| DeepSeek  |      3 |
| **Total** | **30** |

---

# 🤖 Configured Models

## Ollama

```text
qwen2.5:1.5b
gemma2:2b
gemma3:4b
mistral:latest
phi3:latest
qwen3:latest
llama3.1:latest
llama3:8b
deepseek-coder:latest
```

## OpenAI

```text
gpt-5-mini
gpt-4o
gpt-4o-mini
```

## Anthropic

```text
claude-sonnet-4-5
claude-haiku-4-5
claude-opus-4-1
```

## Gemini

```text
gemini-3.6-flash
gemini-2.5-flash
gemini-2.5-pro
```

## Mistral

```text
mistral-medium-latest
mistral-large-latest
mistral-small-latest
```

## Groq

```text
llama-3.3-70b-versatile
llama-3.1-8b-instant
mixtral-8x7b-32768
```

## Cohere

```text
command-a-03-2025
command-r-plus
command-r
```

## DeepSeek

```text
deepseek-chat
deepseek-reasoner
deepseek-v4-flash
```

---

# 🔌 Provider Abstraction

All AI providers implement the common domain abstraction:

```python
class AIProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def generate(self, model: str, prompt: str) -> str:
        ...

    @abstractmethod
    def get_models(self) -> list[str]:
        ...
```

This allows application services to work with any provider without depending on provider-specific implementations.

---

# 🏭 Provider Factory

Provider creation uses a registration-based factory.

```text
Provider Name
      ↓
ProviderFactory
      ↓
Registered Provider Builder
      ↓
Concrete AIProvider
```

Providers can be registered without modifying the factory's internal creation logic.

Example:

```python
provider_factory.register(
    "ollama",
    OllamaProvider,
)
```

This supports the **Open/Closed Principle** and keeps provider creation extensible.

---

# 💉 Dependency Injection

Dependency injection is used throughout the architecture.

Example:

```python
class AIService:

    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider
```

The service depends on the abstraction:

```text
AIService
   ↓
AIProvider interface
   ↓
Concrete Provider
```

rather than directly depending on a specific provider.

The application container coordinates dependency construction.

```text
Application
     ↓
ApplicationContainer
     ├── ProviderRegistry
     ├── ProviderFactory
     ├── AIService
     └── Application Services
```

---

# 📚 Provider Registry

The provider registry maintains the configured provider and model definitions.

```python
ProviderRegistry
    ├── get_provider()
    ├── get_providers()
    └── get_models()
```

The current implementation uses:

```text
InMemoryProviderRegistry
```

This keeps configuration separate from application logic and allows future registry implementations.

---

# 🎛️ Provider & Model Selection

`ProviderModelService` provides application-level access to configured providers and models.

Capabilities include:

```text
Get Providers
Get Models
Check Provider Support
Check Model Support
Get Default Model
```

Example:

```python
service.get_providers()
service.get_models("ollama")
service.is_supported_provider("openai")
service.is_supported_model("ollama", "qwen2.5:1.5b")
service.get_default_model("ollama")
```

---

# ⚙️ Configuration

Configuration is centralized in:

```text
app/config/
```

The project uses environment variables through `python-dotenv`.

Sensitive API credentials are never stored in source code.

---

# 🔐 Environment Configuration

Create a local `.env` file based on:

```text
.env.example
```

Example:

```env
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_TRANSLATION_MODEL=qwen2.5:1.5b
OPENAI_TRANSLATION_MODEL=gpt-5-mini
ANTHROPIC_TRANSLATION_MODEL=claude-sonnet-4-5
GEMINI_TRANSLATION_MODEL=gemini-3.6-flash
MISTRAL_TRANSLATION_MODEL=mistral-medium-latest
GROQ_TRANSLATION_MODEL=llama-3.1-8b-instant
COHERE_TRANSLATION_MODEL=command-a-03-2025
DEEPSEEK_TRANSLATION_MODEL=deepseek-v4-flash

DEFAULT_TRANSLATION_PROVIDER=ollama
DEFAULT_CAPTION_LANGUAGE=en

OLLAMA_TIMEOUT=120
CLOUD_TIMEOUT=120
```

Cloud provider API keys should be supplied through environment variables.

Never commit:

```text
.env
```

---

# 🦙 Ollama

Ollama is supported as the primary local AI provider.

Default Ollama configuration:

```text
Base URL:
http://localhost:11434

Default translation model:
qwen2.5:1.5b
```

The Ollama client communicates with the local Ollama API and supports non-streaming text generation.

---

# ☁️ Cloud Providers

The platform contains provider clients for:

```text
OpenAI
Anthropic
Gemini
Mistral
Groq
Cohere
DeepSeek
```

Each provider has:

```text
Provider
   ↓
Provider Client
   ↓
External API
```

Provider-specific API details remain isolated inside the infrastructure layer.

---

# 🧩 Domain Entities

Phase 0 establishes the foundational domain entities:

```text
AIModel
AIProviderConfig
```

`AIModel`:

```python
@dataclass(frozen=True)
class AIModel:
    provider: str
    name: str
```

`AIProviderConfig`:

```python
@dataclass(frozen=True)
class AIProviderConfig:
    name: str
    models: tuple[AIModel, ...]
```

These immutable entities provide a clean domain representation of provider/model configuration.

---

# 🛡️ Error Handling

The project defines a domain-specific exception hierarchy:

```text
DigitalTwinError
├── ConfigurationError
├── ProviderError
└── ModelError
```

This allows application code to handle platform-specific failures without depending on infrastructure-specific exceptions.

---

# 📝 Logging

Centralized logging is provided through:

```text
app/core/logging.py
```

Logging includes:

```text
Timestamp
Log Level
Logger Name
Message
```

Application startup and major infrastructure events can therefore be tracked consistently.

---

# ✅ Configuration Validation

The application validates the configured AI provider/model architecture during startup.

Current validation verifies:

```text
Exactly 8 providers
Exactly 30 models
Every provider has a name
Every provider has at least one model
```

This prevents invalid provider configuration from silently reaching the application layer.

---

# 🖥️ Streamlit Foundation

The current Streamlit interface provides the initial application shell.

Current capabilities:

```text
AI Digital Twin Agent Platform
        ↓
Provider Selection
        ↓
Model Selection
```

The Streamlit presentation layer communicates with application services rather than directly constructing provider clients.

---

# 📁 Project Structure

```text
AI-Digital-Twin-Agent-Platform/
│
├── app.py
│
├── app/
│   ├── __init__.py
│   │
│   ├── bootstrap.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── providers.py
│   │   ├── settings.py
│   │   └── validation.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── ai_model.py
│   │   │   └── ai_provider_config.py
│   │   │
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   ├── ai_provider.py
│   │   │   └── provider_registry.py
│   │   │
│   │   └── services/
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── container.py
│   │   ├── agents/
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── ai_service.py
│   │       └── provider_model_service.py
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── ollama_client.py
│   │   │   ├── openai_client.py
│   │   │   ├── anthropic_client.py
│   │   │   ├── gemini_client.py
│   │   │   ├── mistral_client.py
│   │   │   ├── groq_client.py
│   │   │   ├── cohere_client.py
│   │   │   ├── deepseek_client.py
│   │   │   ├── ollama_provider.py
│   │   │   ├── openai_provider.py
│   │   │   ├── anthropic_provider.py
│   │   │   ├── gemini_provider.py
│   │   │   ├── mistral_provider.py
│   │   │   ├── groq_provider.py
│   │   │   ├── cohere_provider.py
│   │   │   ├── deepseek_provider.py
│   │   │   └── registry.py
│   │   │
│   │   └── storage/
│   │
│   └── presentation/
│       ├── __init__.py
│       └── pages/
│           ├── __init__.py
│           └── home.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
│
├── docs/
│   ├── architecture.md
│   └── phase-0.md
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

# 🧪 Testing Foundation

A testing structure has been established:

```text
tests/
├── unit/
└── integration/
```

Pytest configuration is maintained through:

```text
pyproject.toml
```

Actual test execution is intentionally deferred until the appropriate testing stage.

---

# 🧱 SOLID Principles

SOLID is a core architectural requirement.

## Single Responsibility Principle

Each component has a focused responsibility.

Examples:

```text
Provider Client
    → API communication

Provider
    → Provider abstraction

Provider Registry
    → Provider/model configuration lookup

Provider Factory
    → Provider construction

AIService
    → AI generation orchestration
```

## Open/Closed Principle

The provider factory uses registration rather than a fixed provider creation chain.

New providers can be registered without rewriting the factory.

## Liskov Substitution Principle

Concrete providers implement the common `AIProvider` contract and can be used wherever an `AIProvider` is required.

## Interface Segregation Principle

Domain contracts expose focused interfaces rather than forcing application components to depend on unnecessary functionality.

## Dependency Inversion Principle

Application services depend on domain abstractions.

```text
Application
    ↓
AIProvider
    ↓
Concrete Infrastructure
```

not:

```text
Application
    ↓
OllamaClient
```

---

# 🔄 Phase Roadmap

## Phase 0 — General Foundation

**Status: ✅ COMPLETE**

```text
Project Definition
Repository Structure
Configuration
Provider Architecture
30 Model Configuration
Provider Implementations
Provider Factory
Dependency Injection
Logging
Exception Handling
Registry
Ollama Foundation
Cloud Provider Clients
Provider/Model Selection
Application Container
Bootstrap
Streamlit Foundation
Testing Foundation
Stabilization
Documentation
Final Review
```

---

## Phase 1 — Knowledge Ingestion Process

**Status: ⏳ NEXT**

Planned capabilities:

```text
Knowledge Domain
Knowledge Entities
Knowledge Interfaces
Document Ingestion
Text Extraction
File Processing
Knowledge Chunking
Metadata
Knowledge Storage
Knowledge Retrieval
Ingestion Service
Knowledge Agent
Application Integration
Knowledge UI
Error Handling
Logging
Documentation
Stabilization
Validation
```

---

## Phase 2 — Intelligence & Memory Process

**Status: ⏳**

Planned focus:

```text
Memory
Learning
Context
Knowledge Relationships
Intelligence Services
Memory Agents
Long-Term Context
```

---

## Phase 3 — Digital Twin Interaction Process

**Status: ⏳**

Planned focus:

```text
Digital Twin Identity
Conversation
Behavior
Preferences
Decision Patterns
Interactive Agents
Personalized Responses
```

---

## Phase 4 — Validation & Advanced Twin Intelligence

**Status: ⏳**

Planned focus:

```text
Advanced Validation
Twin Evaluation
Behavioral Consistency
Advanced Memory
Advanced Intelligence
Continuous Improvement
Production Readiness
```

---

# ▶️ Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
copy .env.example .env
```

Configure the required environment variables.

Start Streamlit:

```bash
streamlit run app.py
```

---

# 🔒 Security

Never commit secrets.

The following should remain local:

```text
.env
API keys
Access tokens
Private credentials
```

`.env.example` contains configuration placeholders only.

If an API key is ever exposed publicly, revoke or rotate it immediately.

---

# 📦 Technology Stack

```text
Language
Python 3.11+

UI
Streamlit

Configuration
python-dotenv

HTTP
Requests

Testing
Pytest

AI Providers
Ollama
OpenAI
Anthropic
Gemini
Mistral
Groq
Cohere
DeepSeek
```

---

# 📌 Development Principles

The project follows these principles:

```text
SOLID
Clean Architecture
Dependency Injection
Interface-driven design
Separation of concerns
Provider abstraction
Configuration-driven architecture
Secure credential handling
Incremental development
Testability
Maintainability
Extensibility
```

---

# 🏁 Phase 0 Completion Summary

Phase 0 establishes the complete technical foundation required for the Digital Twin platform.

```text
8 AI Providers
        +
30 Configured Models
        +
Provider Abstraction
        +
Provider Registry
        +
Provider Factory
        +
Dependency Injection
        +
Application Container
        +
Configuration Validation
        +
Logging
        +
Exception Architecture
        +
Streamlit Foundation
        +
Testing Foundation
        +
Documentation
        ↓
Phase 0 COMPLETE ✅
```

The project is now ready to move into the **Knowledge Ingestion Process**.

---

# 📅 Next Development Step

```text
PHASE 1
Knowledge Ingestion Process
        ↓
1.1 Knowledge Domain Design
```

Phase 1 will begin only after the Phase 0 foundation is fully reviewed and accepted.

---

# 👨‍💻 Project

**AI Digital Twin Agent Platform**

> Building an evolving AI representation through knowledge, memory, intelligence, and interaction.
