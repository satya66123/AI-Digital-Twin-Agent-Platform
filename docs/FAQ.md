# Frequently Asked Questions (FAQ)

## AI Digital Twin Agent Platform

**Version:** 1.0.0

---

## 1. General Questions

### What is the AI Digital Twin Agent Platform?

The AI Digital Twin Agent Platform is a modular, multi-provider AI application designed to build a personalized digital twin using knowledge ingestion, memory management, contextual intelligence, and conversational interaction.

### What are the main capabilities?

- Knowledge ingestion from supported document formats.
- Memory creation and retrieval.
- Short-term and long-term memory management.
- Context-aware AI responses.
- Personalized digital twin interactions.
- Conversation history management.
- Response quality and consistency evaluation.
- Multi-provider and multi-model support.

### Which technologies are used?

The project uses:

- Python 3.11+
- Streamlit
- PyTest
- JSON-based persistence
- Ollama and cloud AI providers
- Git and GitHub

## 2. AI Providers and Models

### Which AI providers are supported?

The platform supports eight providers:

1. Ollama
2. OpenAI
3. Anthropic
4. Gemini
5. Mistral
6. Groq
7. Cohere
8. DeepSeek

### How many models are configured?

The platform has 30 configured models across the eight providers.

### Which Ollama model is preferred by default?

`qwen2.5:1.5b` is the preferred default local model.

### Can I use a local AI model?

Yes. Ollama provides local model support. The Ollama service must be installed, running, and configured with the required model.

### Can I switch AI providers?

The application supports multiple providers. Provider and model selection depend on the application's configuration and user interface.

## 3. Knowledge Management

### Which document formats are supported?

The knowledge ingestion process supports:

- PDF
- DOCX
- TXT
- Markdown
- CSV

### What is knowledge ingestion?

Knowledge ingestion is the process of accepting documents, extracting their content, and preparing that information for retrieval and use in AI responses.

### Does the platform use uploaded knowledge during conversations?

The IntelligenceContextBuilder combines relevant knowledge with memories and conversation history to provide context for responses.

## 4. Memory Management

### What types of memory are supported?

The platform supports four memory types:

- SHORT_TERM
- LONG_TERM
- EPISODIC
- SEMANTIC

### What is short-term memory?

Short-term memory stores information intended for immediate or near-term contextual use.

### What is long-term memory?

Long-term memory preserves useful information for future interactions.

### What is memory consolidation?

Memory consolidation is the process of promoting suitable short-term memories into long-term memory.

### Where are memories stored?

The default JSON memory repository path is:

```text
data/memory/memories.json
```

## 5. Digital Twin Interaction

### How does the digital twin generate responses?

The intelligence process combines available knowledge, relevant memories, and conversation history before generating a response through the configured AI provider.

### Does the platform support multi-turn conversations?

Yes. Conversation services manage conversation sessions, messages, and history to support multi-turn interactions.

### Can conversations be archived or deleted?

The ConversationService supports conversation management operations, including archiving and deletion.

## 6. Architecture and Development

### Does the project follow SOLID principles?

Yes. The architecture follows SOLID principles, separation of concerns, dependency inversion, and interface-based design.

### What are the main architectural layers?

1. Presentation Layer
2. Application Layer
3. Domain Layer
4. Infrastructure Layer

### What is ApplicationContainer?

ApplicationContainer provides dependency wiring and application component creation, helping keep services and infrastructure implementations decoupled.

### Is a relational database required?

No relational database is required for the confirmed v1.0.0 JSON persistence approach.

## 7. Testing and Quality

### Which testing framework is used?

PyTest is used for automated testing.

### What is response quality evaluation?

ResponseQualityService evaluates response characteristics such as empty or short content and repeated sentences. It provides a score, issues, and suggestions.

### What is response consistency evaluation?

ResponseConsistencyService uses lexical Jaccard similarity to identify potentially repetitive responses compared with previous assistant messages.

It is an advisory repetition check, not a factual contradiction detector.

## 8. Configuration and Security

### Where should I configure API credentials?

Use the project's environment configuration. Refer to `.env.example` and the Config implementation for the exact variable names.

Never commit real API keys to Git.

### What should I do if Ollama is unavailable?

Check that Ollama is installed and running, verify its configured base URL, and confirm that the required model is available locally.

### Are memory and conversation files sensitive?

They may contain personal information and conversation content. Protect them and avoid committing them to public repositories.

## 9. Troubleshooting

### The application cannot connect to an AI provider. What should I check?

- Verify provider configuration.
- Check API credentials where applicable.
- Check network connectivity for cloud providers.
- Confirm the selected model is supported by the configured provider.

### The application cannot find an Ollama model. What should I check?

- Confirm the Ollama service is running.
- Verify the model name.
- Confirm the model has been downloaded.
- Check the configured Ollama base URL.

### Memory or conversation history is missing. What should I check?

- Verify the JSON repository paths.
- Confirm that the expected files exist.
- Check filesystem permissions.
- Validate JSON syntax.
- Restore from a known-good backup if necessary.

---

## 10. Additional Help

For more information, refer to:

- `README.md`
- `INSTALLATION.md`
- `CONFIGURATION.md`
- `ARCHITECTURE.md`
- `API_DOCUMENTATION.md`
- `USER_GUIDE.md`
- `TROUBLESHOOTING.md`
- `TESTING.md`

---

**Document:** FAQ.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
