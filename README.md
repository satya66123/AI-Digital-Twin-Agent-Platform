# 🤖 AI Digital Twin Agent Platform

An AI-powered Digital Twin Agent Platform built with a modular,
SOLID-based, multi-provider and multi-model architecture.

## Project Status

**Current Phase:** Phase 0 — General Foundation

## Architecture

The platform follows:

- SOLID principles
- Separation of concerns
- Dependency inversion
- Interface-based design
- Modular architecture
- Multi-provider support
- Multi-model support

## AI Providers

The platform supports 8 AI providers:

1. Ollama
2. OpenAI
3. Anthropic
4. Google Gemini
5. Mistral
6. Groq
7. Cohere
8. DeepSeek

## AI Models

The platform supports 30 configured models.

### Ollama

- qwen2.5:1.5b
- gemma2:2b
- gemma3:4b
- mistral:latest
- phi3:latest
- qwen3:latest
- llama3.1:latest
- llama3:8b
- deepseek-coder:latest

### OpenAI

- gpt-5-mini
- gpt-4o
- gpt-4o-mini

### Anthropic

- claude-sonnet-4-5
- claude-haiku-4-5
- claude-opus-4-1

### Google Gemini

- gemini-3.6-flash
- gemini-2.5-flash
- gemini-2.5-pro

### Mistral

- mistral-medium-latest
- mistral-large-latest
- mistral-small-latest

### Groq

- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b-32768

### Cohere

- command-a-03-2025
- command-r-plus
- command-r

### DeepSeek

- deepseek-chat
- deepseek-reasoner
- deepseek-v4-flash

## Project Phases

```text
Phase 0 → General Foundation
Phase 1 → Knowledge Ingestion Process
Phase 2 → Intelligence & Memory Process
Phase 3 → Digital Twin Interaction Process
Phase 4 → Validation & Advanced Twin Intelligence
````

## Phase 0 Components

```text
Configuration
Provider Abstraction
Provider Clients
Provider Registry
Model Registry
Provider Factory
Dependency Injection
Application Bootstrap
Streamlit Foundation
Logging
Exception Handling
Testing Foundation
```

## Project Structure

```text
app/
├── application/
├── config/
├── core/
├── domain/
├── infrastructure/
└── presentation/

tests/
├── unit/
└── integration/
```

## Configuration

Create a local `.env` file from `.env.example`.

Never commit `.env` or API keys to source control.

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Streamlit:

```bash
streamlit run app.py
```

## Development Principles

Every phase follows:

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

## License

MIT License

````

### `docs/architecture.md`

```markdown
# Architecture

## Architectural Layers

```text
Presentation
     ↓
Application
     ↓
Domain
     ↓
Infrastructure
````

## Dependency Direction

```text
Presentation → Application → Domain
                         ↓
                  Infrastructure
```

The domain layer depends on abstractions rather than concrete
infrastructure implementations.

## Provider Architecture

```text
AIProvider
    ↑
Concrete Provider
    ↓
Provider Client
    ↓
External AI API
```

## SOLID

### Single Responsibility

Components have focused responsibilities.

### Open/Closed

New providers and models can be introduced without changing
core Digital Twin business logic.

### Liskov Substitution

Concrete providers implement the common provider abstraction.

### Interface Segregation

Interfaces remain focused and minimal.

### Dependency Inversion

Higher-level application and domain components depend on
abstractions.

## Multi-Provider Architecture

8 providers are supported.

## Multi-Model Architecture

30 models are configured.

Provider and model selection is independent from Digital Twin
business logic.

````

### `docs/phase-0.md`

```markdown
# Phase 0 — General Foundation

## Objective

Establish a clean, modular, SOLID-based foundation for the
AI Digital Twin Agent Platform.

## Completed

- Project definition
- Architecture design
- Repository structure
- Configuration
- Provider abstraction
- 8 provider implementations
- 30 model configuration
- Provider clients
- Provider registry
- Model registry
- Provider factory
- Dependency injection
- Application bootstrap
- Streamlit foundation
- Logging
- Exception handling
- Testing foundation
- Stabilization
- Documentation

## Status

Phase 0 is ready for final review.
````

## Phase 0 Tracker

```text
✅ 0.1  Project Definition & Architecture
✅ 0.2  Repository Structure
✅ 0.3  Configuration Foundation
✅ 0.4  Multi-Provider / Multi-Model Foundation
✅ 0.5  Provider Implementations
✅ 0.6  Provider Factory + Dependency Injection
✅ 0.7  Logging + Exception Foundation
✅ 0.8  Configuration Validation + Registry
✅ 0.9  Ollama Foundation
✅ 0.10 Remaining Provider Clients
✅ 0.11 Provider/Model Selection Service
✅ 0.12 Dependency Injection Container
✅ 0.13 Application Bootstrap
✅ 0.14 Streamlit Foundation
✅ 0.15 Configuration Cleanup
✅ 0.16 Testing Foundation
✅ 0.17 Stabilization
✅ 0.18 Documentation

⏳ 0.19 Final Review
⏳ 0.20 Phase 0 Complete
```

**Next → Step 0.19: Final Phase 0 Review.**
