# Application Workflow

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Project Status:** Completed

---

## 1. Overview

The AI Digital Twin Agent Platform follows a modular workflow that connects knowledge ingestion, memory management, contextual intelligence, personalization, and conversational interaction.

The workflow is designed to provide personalized AI responses using available knowledge, stored memories, and conversation history.

## 2. High-Level Application Workflow

```text
              USER
                |
                v
       Streamlit Interface
                |
                v
       Provider & Model Selection
                |
                v
       Digital Twin Interaction
                |
                v
       Context Preparation
                |
        +-------+-------+
        |       |       |
        v       v       v
     Knowledge Memory Conversation
        |       |       |
        +-------+-------+
                |
                v
       Intelligence Service
                |
                v
        Selected AI Provider
                |
                v
        Response Evaluation
                |
                v
       Conversation Management
                |
                v
         Display Response
```

This represents the logical application workflow.

## 3. Knowledge Ingestion Workflow

**Objective:** Make document information available to the intelligence process.

### Supported formats

- PDF
- DOCX
- TXT
- Markdown
- CSV

### Workflow

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
Context Preparation
```

The knowledge ingestion workflow is coordinated through KnowledgeAgent.

## 4. Memory Management Workflow

**Objective:** Maintain useful information for future digital twin interactions.

### Supported memory types

- SHORT_TERM
- LONG_TERM
- EPISODIC
- SEMANTIC

### Workflow

```text
Memory Input
     |
     v
MemoryAgent
     |
     v
MemoryService
     |
     v
Memory Repository
     |
     v
Memory Retrieval
     |
     v
Memory Search
     |
     v
Memory Update / Consolidation
```

MemoryService supports creation, retrieval, updating, deletion, searching, and consolidation.

The default JSON memory repository is:

```text
data/memory/memories.json
```

## 5. Intelligence Workflow

**Objective:** Generate responses using relevant application context.

### Context sources

1. Knowledge.
2. Memories.
3. Conversation history.

### Workflow

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

IntelligenceContextBuilder prepares the information, while IntelligenceService coordinates response generation.

## 6. Digital Twin Interaction Workflow

**Objective:** Support contextual multi-turn conversations.

### Workflow

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
Retrieve Conversation History
     |
     v
Build Intelligence Context
     |
     v
Generate AI Response
     |
     v
Update Conversation
     |
     v
Display Response
```

ConversationService supports:

- Conversation creation.
- Message addition.
- History retrieval.
- Archiving.
- Deletion.

The default JSON conversation repository is:

```text
data/conversations/conversations.json
```

## 7. Personalization Workflow

**Objective:** Organize stored information to support personalized interactions.

### Workflow

```text
Stored Memories
      |
      v
DigitalTwinPersonalizationService
      |
      v
Memory Categorization
      |
      +---- Profile
      |
      +---- Preferences
      |
      +---- Expertise
      |
      v
Personalization Context
```

The categorization uses metadata and keyword-based matching.

## 8. Response Evaluation Workflow

### ResponseQualityService

Evaluates:

- Empty responses.
- Very short responses.
- Repeated sentences.

Provides:

- Evaluation score.
- Detected issues.
- Suggestions.

### ResponseConsistencyService

Uses lexical Jaccard similarity to identify potentially repetitive responses compared with previous assistant messages.

It is an advisory repetition check and does not detect factual contradictions.

## 9. AI Provider Workflow

The platform supports eight AI providers and 30 configured models.

```text
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
        |
        v
Generated AI Response
```

Ollama is the preferred default provider.

Preferred default local model:

`qwen2.5:1.5b`

ApplicationContainer coordinates provider registration and dependency wiring.

## 10. Data Persistence Workflow

The platform uses JSON-based persistence for memories and conversations.

```text
Application Services
        |
        v
Repository Abstractions
        |
        v
JSON Repository Implementations
        |
        +---- memories.json
        |
        +---- conversations.json
```

Known default paths:

```text
data/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

Knowledge persistence follows its configured implementation.

## 11. Complete User Journey

The overall user journey can be understood as follows:

1. Start the Streamlit application.
2. Select an AI provider.
3. Select a configured model.
4. Ingest relevant knowledge documents.
5. Create or manage memories.
6. Start a digital twin conversation.
7. Prepare context from knowledge, memories, and conversation history.
8. Generate a response using the selected AI provider.
9. Evaluate response quality and potential repetition.
10. Maintain conversation history.
11. Continue interacting with the digital twin.

The exact sequence of user-interface actions depends on the implemented application pages.

## 12. Development Workflow

The project followed a structured development methodology:

**PLAN → DESIGN → IMPLEMENT → TEST → FIX → STABILIZE → DOCUMENT → NEXT PHASE**

### Completed phases

| Phase | Name | Status |
|---|---|---|
| Phase 0 | General Foundation | Completed |
| Phase 1 | Knowledge Ingestion Process | Completed |
| Phase 2 | Intelligence and Memory Process | Completed |
| Phase 3 | Digital Twin Interaction Process | Completed |
| Phase 4 | Validation and Advanced Twin Intelligence | Completed |

## 13. Final Workflow Summary

The AI Digital Twin Agent Platform connects knowledge, memory, intelligence, personalization, and conversation management through a modular application architecture.

Its workflow enables contextual AI interactions while maintaining separation between presentation, application logic, domain abstractions, and infrastructure implementations.

---

**Document:** WORKFLOW.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
