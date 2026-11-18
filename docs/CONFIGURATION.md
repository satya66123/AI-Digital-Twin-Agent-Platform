# Configuration Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Language:** Python 3.11+  
**Configuration:** Environment Variables and Application Configuration  
**Storage:** JSON

---

## 1. Overview

The AI Digital Twin Agent Platform supports multiple AI providers, configurable models, local Ollama integration, and JSON-based persistence.

Configuration is managed through the application's configuration foundation and environment variables.

This document explains the main configuration areas.

## 2. Environment Configuration

Create a `.env` file in the project root directory.

Use `.env.example` as a reference if it is available in the repository.

Example structure:

```env
# Application
APP_ENV=development
DEBUG=true

# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Provider API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
MISTRAL_API_KEY=
GROQ_API_KEY=
COHERE_API_KEY=
DEEPSEEK_API_KEY=

# Default Provider
DEFAULT_TRANSLATION_PROVIDER=ollama

# Default Caption Language
DEFAULT_CAPTION_LANGUAGE=en
```

The variable names above are illustrative configuration entries. Keep the actual names consistent with the project's existing configuration classes and `.env.example`.

Never commit real API keys or secrets.

## 3. AI Provider Configuration

The platform supports eight AI providers.

| Provider | Configuration |
|---|---|
| Ollama | Base URL and local model configuration |
| OpenAI | API credentials and model configuration |
| Anthropic | API credentials and model configuration |
| Gemini | API credentials and model configuration |
| Mistral | API credentials and model configuration |
| Groq | API credentials and model configuration |
| Cohere | API credentials and model configuration |
| DeepSeek | API credentials and model configuration |

Configure credentials only for the providers you intend to use.

## 4. Ollama Configuration

Ollama provides local model execution.

Default local server URL:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

Preferred default model:

```text
qwen2.5:1.5b
```

Example model download:

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama:

```bash
ollama serve
```

Ensure that the configured model is available locally before selecting it in the application.

## 5. Configured AI Models

The platform maintains 30 configured models across eight providers.

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

### Gemini
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

## 6. Default Model Configuration

The preferred local model is:

```text
qwen2.5:1.5b
```

The application also supports selecting other configured providers and models.

The actual default provider and model behavior is controlled by the project's configuration and Streamlit selection logic.

## 7. Translation Configuration

The project configuration includes provider-specific translation model settings.

Known configuration entries include:

```env
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
```

These settings should be retained in the actual application configuration where applicable.

## 8. JSON Storage Configuration

The platform uses JSON-based persistence.

Storage responsibilities include:

- Knowledge storage.
- Memory storage.
- Conversation storage.

Known default storage paths include:

```text
data/
├── memory/
│   └── memories.json
│
└── conversations/
    └── conversations.json
```

Knowledge storage paths are managed through the knowledge persistence implementation.

Ensure that the application has permission to create and modify its data directories.

## 9. Memory Configuration

The platform supports four memory categories:

```text
SHORT_TERM
LONG_TERM
EPISODIC
SEMANTIC
```

Memory operations are managed by `MemoryService` and persisted through `JSONMemoryRepository`.

## 10. Conversation Configuration

Conversation storage uses:

```text
data/conversations/conversations.json
```

The conversation repository manages:

- Conversation records.
- Message history.
- Conversation status.
- Creation and update timestamps.

## 11. Provider Selection

The application uses:

- ProviderFactory.
- Provider Registry.
- ProviderModelService.
- AIService.

Provider registration is managed by `ApplicationContainer`.

The Streamlit interface allows users to select a configured provider and model.

## 12. Configuration Security

Follow these practices:

1. Store API keys in environment variables.
2. Keep `.env` out of Git commits.
3. Maintain a `.env.example` without real credentials.
4. Never print secrets in application logs.
5. Restrict access to personal JSON data.
6. Back up important memory and conversation files.
7. Review configuration before deployment.

## 13. Configuration Troubleshooting

| Issue | Suggested action |
|---|---|
| Missing API key | Configure the required provider credential. |
| Ollama unavailable | Start Ollama and check its base URL. |
| Model not found | Verify the model name and provider availability. |
| Invalid environment variable | Compare `.env` with `.env.example` and configuration code. |
| JSON storage unavailable | Check the directory and file permissions. |
| Provider initialization failure | Verify provider registration and required settings. |

## 14. Configuration Summary

The platform configuration supports:

- Eight AI providers.
- Thirty configured models.
- Local Ollama integration.
- Cloud provider credentials.
- Translation model selection.
- Caption language settings.
- JSON-based persistence.
- Centralized application dependency configuration.

---

**Document:** CONFIGURATION.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
