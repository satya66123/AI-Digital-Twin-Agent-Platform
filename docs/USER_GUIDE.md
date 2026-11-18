# User Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Interface:** Streamlit  
**Default Provider:** Ollama  
**Preferred Default Model:** qwen2.5:1.5b

---

## 1. Introduction

The AI Digital Twin Agent Platform is designed to provide personalized AI interactions using knowledge, memories, and conversation history.

The platform supports eight AI providers and 30 configured models.

Its major capabilities include:

- Knowledge ingestion.
- Intelligent memory management.
- Context-aware response generation.
- Digital twin personalization.
- Conversation management.
- Response quality and consistency evaluation.

## 2. Starting the Application

1. Open the project in your development environment.
2. Activate the Python virtual environment.
3. Verify application configuration.
4. Start the Ollama service if using local models.
5. Run the Streamlit entry-point file.

Example:

```bash
streamlit run <ENTRY_POINT_FILE>
```

Replace the placeholder with the actual application entry-point filename.

## 3. Selecting an AI Provider and Model

The platform supports the following providers:

1. Ollama
2. OpenAI
3. Anthropic
4. Gemini
5. Mistral
6. Groq
7. Cohere
8. DeepSeek

### Preferred local configuration

- Provider: Ollama
- Model: `qwen2.5:1.5b`

For Ollama, make sure the service is running and the selected model is downloaded.

For cloud providers, configure the required API credentials.

## 4. Managing Knowledge

The knowledge ingestion process allows supported documents to be processed for use in contextual interactions.

### Supported document formats

- PDF
- DOCX
- TXT
- Markdown
- CSV

### General workflow

1. Provide a supported document.
2. Allow the application to process its content.
3. Verify that the document was successfully ingested.
4. Use relevant questions during digital twin conversations.
5. Review whether the generated response uses the available knowledge.

The exact user-interface controls depend on the implemented Streamlit pages.

## 5. Understanding Memory

The platform supports four memory categories:

| Memory Type | Description |
|---|---|
| SHORT_TERM | Immediate contextual information |
| LONG_TERM | Information retained for future interactions |
| EPISODIC | Experience and event-related information |
| SEMANTIC | General facts and concepts |

### Memory operations

MemoryService supports:

- Creating memories.
- Retrieving memories.
- Updating memories.
- Deleting memories.
- Searching memories.
- Consolidating suitable short-term memories into long-term memory.

### Memory storage

The default memory repository is:

```text
data/memory/memories.json
```

## 6. Interacting with Your Digital Twin

The Digital Twin Interaction Process supports contextual conversations.

### General interaction workflow

1. Start a conversation.
2. Enter a question or message.
3. Allow the application to prepare relevant context.
4. Receive an AI-generated response.
5. Continue the conversation with follow-up questions.
6. Review the conversation history.

The intelligence process can combine:

- Relevant knowledge.
- Stored memories.
- Conversation history.

This helps maintain continuity across interactions.

## 7. Personalization

The platform includes DigitalTwinPersonalizationService.

It categorizes memories into:

- Profile.
- Preferences.
- Expertise.

These categories help organize relevant information for personalized interactions.

The categorization uses metadata and keyword-based matching.

## 8. Conversation Management

ConversationService supports the following operations:

| Operation | Purpose |
|---|---|
| Create | Start a new conversation |
| Add message | Store a conversation message |
| Retrieve history | Access previous messages |
| Archive | Archive a conversation |
| Delete | Remove a conversation |

The default conversation repository is:

```text
data/conversations/conversations.json
```

## 9. Response Quality

The platform includes ResponseQualityService.

It evaluates response characteristics such as:

- Empty responses.
- Very short responses.
- Repeated sentences.

The service provides an evaluation score, issues, and suggestions.

## 10. Response Consistency

ResponseConsistencyService uses lexical Jaccard similarity to identify potentially repetitive responses compared with previous assistant messages.

This feature is an advisory repetition check. It does not establish factual accuracy or detect semantic contradictions.

## 11. Backing Up Your Data

Important application data includes:

- Knowledge storage.
- Memory records.
- Conversation history.

Before modifying or transferring data:

1. Stop the application.
2. Back up the configured data directory.
3. Preserve the directory structure.
4. Verify JSON files.
5. Store backups securely.

Refer to `EXPORT_GUIDE.md` for additional instructions.

## 12. Troubleshooting

| Problem | Recommended action |
|---|---|
| Application does not start | Check Python environment and Streamlit configuration |
| Ollama unavailable | Start Ollama and verify its base URL |
| Model not found | Download the selected model |
| Cloud provider authentication fails | Check API credentials |
| Knowledge is unavailable | Verify ingestion and retrieval |
| Memories are missing | Check the memory repository path |
| Conversation history is missing | Check the conversation repository path |

Refer to `TROUBLESHOOTING.md` for more detailed solutions.

## 13. Security Recommendations

- Never share API credentials.
- Keep `.env` private.
- Protect memory and conversation files.
- Avoid uploading confidential information to external providers without authorization.
- Back up important data.
- Do not commit private application data to public repositories.

## 14. Additional Documentation

For more information, refer to:

- `INSTALLATION.md`
- `CONFIGURATION.md`
- `PROVIDER_GUIDE.md`
- `FEATURES.md`
- `ARCHITECTURE.md`
- `API_DOCUMENTATION.md`
- `TESTING.md`
- `EXPORT_GUIDE.md`
- `TROUBLESHOOTING.md`
- `SECURITY.md`

---

**Document:** USER_GUIDE.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
