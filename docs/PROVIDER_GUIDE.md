# AI Provider Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Supported Providers:** 8  
**Configured Models:** 30

---

## 1. Overview

The AI Digital Twin Agent Platform supports multiple AI providers through a modular, interface-based architecture.

The objective is to allow users to select different AI providers and models without tightly coupling application services to individual provider implementations.

The platform supports:

- Local AI inference through Ollama.
- Cloud AI integrations.
- Multiple models per provider.
- Centralized provider configuration.
- Provider abstraction and dependency wiring.

## 2. Supported AI Providers

The platform supports eight providers:

| No. | Provider | Model Count | Integration Type |
|---:|---|---:|---|
| 1 | Ollama | 9 | Local |
| 2 | OpenAI | 3 | Cloud |
| 3 | Anthropic | 3 | Cloud |
| 4 | Gemini | 3 | Cloud |
| 5 | Mistral | 3 | Cloud |
| 6 | Groq | 3 | Cloud |
| 7 | Cohere | 3 | Cloud |
| 8 | DeepSeek | 3 | Cloud |
| | **Total** | **30** | |

## 3. Ollama – Local AI Provider

<badge color="success">Preferred default provider</badge>

Ollama allows users to run supported AI models locally.

### Configured models

1. `qwen2.5:1.5b`
2. `gemma2:2b`
3. `gemma3:4b`
4. `mistral:latest`
5. `phi3:latest`
6. `qwen3:latest`
7. `llama3.1:latest`
8. `llama3:8b`
9. `deepseek-coder:latest`

**Preferred default model:** `qwen2.5:1.5b`

### Configuration

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TRANSLATION_MODEL=qwen2.5:1.5b
```

### Installation and verification

Install Ollama and start its service.

Download the preferred model:

```bash
ollama pull qwen2.5:1.5b
```

List locally available models:

```bash
ollama list
```

### Important considerations

- Ollama must be running for local inference.
- Required models must be downloaded.
- The configured base URL must be accessible.
- Local inference depends on available system resources.

## 4. OpenAI

OpenAI provides cloud-based AI model integration.

### Configured models

1. `gpt-5-mini`
2. `gpt-4o`
3. `gpt-4o-mini`

### Configuration

```env
OPENAI_TRANSLATION_MODEL=gpt-5-mini
```

Configure the required OpenAI credentials using the environment variable expected by the project's Config implementation.

## 5. Anthropic

Anthropic provides cloud-based AI model integration.

### Configured models

1. `claude-sonnet-4-5`
2. `claude-haiku-4-5`
3. `claude-opus-4-1`

### Configuration

```env
ANTHROPIC_TRANSLATION_MODEL=claude-sonnet-4-5
```

Configure the required Anthropic credentials securely.

## 6. Gemini

Gemini provides Google's AI model integration.

### Configured models

1. `gemini-3.6-flash`
2. `gemini-2.5-flash`
3. `gemini-2.5-pro`

### Configuration

```env
GEMINI_TRANSLATION_MODEL=gemini-3.6-flash
```

Configure the required Gemini credentials securely.

## 7. Mistral

Mistral provides cloud-based AI model integration.

### Configured models

1. `mistral-medium-latest`
2. `mistral-large-latest`
3. `mistral-small-latest`

### Configuration

```env
MISTRAL_TRANSLATION_MODEL=mistral-medium-latest
```

## 8. Groq

Groq provides cloud-based model inference.

### Configured models

1. `llama-3.3-70b-versatile`
2. `llama-3.1-8b-instant`
3. `mixtral-8x7b-32768`

### Configuration

```env
GROQ_TRANSLATION_MODEL=llama-3.1-8b-instant
```

## 9. Cohere

Cohere provides cloud-based AI model integration.

### Configured models

1. `command-a-03-2025`
2. `command-r-plus`
3. `command-r`

### Configuration

```env
COHERE_TRANSLATION_MODEL=command-a-03-2025
```

## 10. DeepSeek

DeepSeek provides cloud-based AI model integration.

### Configured models

1. `deepseek-chat`
2. `deepseek-reasoner`
3. `deepseek-v4-flash`

### Configuration

```env
DEEPSEEK_TRANSLATION_MODEL=deepseek-v4-flash
```

## 11. Default Provider Configuration

The project uses Ollama as its preferred default translation provider.

```env
DEFAULT_TRANSLATION_PROVIDER=ollama
DEFAULT_CAPTION_LANGUAGE=en
```

The preferred default local model is:

```text
qwen2.5:1.5b
```

Other provider-specific model settings are maintained through the application configuration.

## 12. Provider Architecture

Provider integrations follow the project's interface-based architecture.

Conceptual provider flow:

```text
Presentation Layer
        |
        v
Application Services
        |
        v
Provider Abstraction
        |
        v
Provider Implementation
        |
        +---- Ollama
        +---- OpenAI
        +---- Anthropic
        +---- Gemini
        +---- Mistral
        +---- Groq
        +---- Cohere
        +---- DeepSeek
```

ApplicationContainer coordinates provider registration and dependency wiring.

This design separates application logic from provider-specific implementations.

## 13. Adding a New Provider

Follow these general steps when extending the provider architecture:

1. Review the existing provider abstraction.
2. Create an implementation that satisfies the required interface.
3. Implement provider-specific model configuration.
4. Handle authentication securely.
5. Integrate the implementation through ApplicationContainer.
6. Register the provider with the application.
7. Add unit tests.
8. Validate provider connectivity.
9. Test response generation.
10. Update provider documentation.

Follow the actual interfaces and registration conventions in the repository.

## 14. Provider Troubleshooting

| Problem | Recommended action |
|---|---|
| Provider connection failure | Verify connectivity and provider availability |
| Authentication failure | Check credentials and environment configuration |
| Model not found | Verify the configured model identifier |
| Ollama unavailable | Start the Ollama service |
| Local model missing | Download the required model |
| Invalid configuration | Review `.env.example` and Config |
| Provider response failure | Check provider-specific errors and logs |

## 15. Security Best Practices

- Store API keys in environment variables.
- Never commit `.env` containing real credentials.
- Keep `.env.example` free of secrets.
- Avoid printing credentials in application logs.
- Protect local memory and conversation data.
- Follow each provider's authentication requirements.

## 16. Provider Summary

The AI Digital Twin Agent Platform integrates eight providers and 30 configured models.

The multi-provider architecture gives the application flexibility to use local and cloud AI models while keeping provider-specific implementation details separate from application services.

---

**Document:** PROVIDER_GUIDE.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
