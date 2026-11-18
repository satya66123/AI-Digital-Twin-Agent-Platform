# Installation Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Language:** Python 3.11+  
**Interface:** Streamlit

---

## 1. Overview

This document explains how to prepare the development environment, install dependencies, configure AI providers, and run the AI Digital Twin Agent Platform locally.

## 2. Prerequisites

Install the following before setting up the project:

| Requirement | Purpose |
|---|---|
| Python 3.11+ | Application runtime |
| pip | Python package installation |
| Git | Source code management |
| Ollama | Local AI model execution, if using local models |
| PyCharm or another IDE | Development environment |

An internet connection is required to install packages and access cloud AI providers.

## 3. Clone the Repository

Clone the project repository:

```bash
git clone <YOUR_REPOSITORY_URL>
```

Navigate into the cloned project directory:

```bash
cd <PROJECT_DIRECTORY>
```

Replace the placeholders with your actual repository URL and project directory.

## 4. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

## 5. Install Dependencies

Install the dependencies from the project's requirements file:

```bash
pip install -r requirements.txt
```

If the repository uses a different dependency-management file, follow the instructions provided by that file.

## 6. Configure Environment Variables

Create a local `.env` file using the project's `.env.example` as a reference.

Example configuration values:

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
```

These are example project configuration values. Confirm the exact variable names and supported settings in `.env.example` and the Config implementation.

Add provider credentials using the actual environment variable names expected by the project. Never commit real API keys.

## 7. Configure Ollama

If you plan to use local AI models:

1. Install Ollama.
2. Start the Ollama service.
3. Confirm the service is accessible at the configured base URL.
4. Download the required model.

Preferred default model:

```bash
ollama pull qwen2.5:1.5b
```

Verify the available models:

```bash
ollama list
```

The application also supports the configured cloud AI providers.

## 8. Configure Application Data

The platform uses JSON-based persistence.

Known default storage paths:

```text
data/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

Create the required directories if they are not created automatically by the application.

Check the actual repository and knowledge-storage configuration for additional data directories.

## 9. Run the Application

Identify the Streamlit entry-point file in the project repository.

Run it using:

```bash
streamlit run <ENTRY_POINT_FILE>
```

Replace `<ENTRY_POINT_FILE>` with the actual Streamlit application file.

Streamlit will display the local application address in the terminal.

## 10. Verify the Installation

After starting the application, verify:

- The Streamlit interface loads.
- The application configuration is available.
- The selected provider is configured correctly.
- Ollama is accessible if using local inference.
- The selected model is available.
- Knowledge ingestion can be accessed.
- Memory operations work.
- Conversation interactions work.

## 11. Run Automated Tests

Run the project's test suite:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

For a summary of test execution:

```bash
pytest -ra
```

Resolve any test failures before treating the environment as validated.

## 12. Common Installation Problems

| Problem | Suggested solution |
|---|---|
| Python not found | Verify Python installation and PATH |
| pip installation failure | Upgrade pip and retry |
| Missing dependency | Install the dependency listed by the project |
| Ollama connection failure | Start Ollama and check its base URL |
| Model not found | Download the required model |
| API authentication failure | Verify provider credentials |
| Streamlit command not found | Activate the virtual environment and verify installation |
| Data directory missing | Check configured storage paths and directory permissions |

## 13. Security Recommendations

- Keep `.env` private.
- Never commit API keys.
- Use `.env.example` for documenting required configuration.
- Protect JSON memory and conversation files.
- Keep dependencies updated.
- Back up application data before making changes.

## 14. Installation Complete

Once dependencies, configuration, provider connectivity, and application startup have been verified, the local development environment is ready.

---

**Document:** INSTALLATION.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
