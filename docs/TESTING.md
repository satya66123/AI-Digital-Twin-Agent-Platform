# Testing Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Testing Framework:** PyTest  
**Project Status:** Completed

---

## 1. Overview

Testing is an important part of the AI Digital Twin Agent Platform development lifecycle.

The project uses PyTest to validate application components, services, repositories, provider integrations, and workflows.

The development process follows:

**PLAN → DESIGN → IMPLEMENT → TEST → FIX → STABILIZE → DOCUMENT**

## 2. Testing Objectives

The main testing objectives are:

- Validate individual components.
- Verify service behavior.
- Test repository operations.
- Validate memory lifecycle operations.
- Verify conversation management.
- Test provider integration.
- Validate context construction.
- Identify regressions.
- Confirm integrated application behavior.

## 3. Testing Technology

| Technology | Purpose |
|---|---|
| PyTest | Automated testing |
| Python 3.11+ | Test execution environment |
| Mocking | Isolate dependencies where appropriate |
| JSON fixtures | Test persistence behavior |

Use the project's installed dependencies and existing test configuration.

## 4. Test Directory

The project uses a tests directory for automated test files.

Logical structure:

```text
tests/
├── test_agents/
├── test_services/
├── test_repositories/
├── test_providers/
└── test_application/
```

This is an illustrative organization. Check the actual repository for the implemented test directory structure.

## 5. Running Tests

Run the complete test suite:

```bash
pytest
```

Run tests with detailed output:

```bash
pytest -v
```

Show a summary of skipped and failed tests:

```bash
pytest -ra
```

Run a specific test file:

```bash
pytest tests/test_memory_service.py
```

Run a specific test:

```bash
pytest tests/test_memory_service.py::test_create_memory
```

The example test paths and test names must match the actual repository.

## 6. Agent Testing

The platform includes the following main agents:

- KnowledgeAgent
- MemoryAgent
- DigitalTwinInteractionAgent

Testing should verify that each agent coordinates its intended application workflow and interacts with its dependencies correctly.

## 7. Service Testing

### 7.1 MemoryService

Validate:

- Memory creation.
- Memory retrieval.
- Memory updating.
- Memory deletion.
- Memory searching.
- Memory consolidation.

### 7.2 IntelligenceService

Validate:

- Response generation.
- Provider interaction.
- Context usage.
- Handling of provider failures.

### 7.3 IntelligenceContextBuilder

Validate that the context builder combines:

- Relevant knowledge.
- Stored memories.
- Conversation history.

### 7.4 ConversationService

Validate:

- Conversation creation.
- Message addition.
- History retrieval.
- Archiving.
- Deletion.

### 7.5 DigitalTwinPersonalizationService

Validate categorization into:

- Profile.
- Preferences.
- Expertise.

### 7.6 ResponseQualityService

Validate evaluation behavior for:

- Empty responses.
- Very short responses.
- Repeated sentences.
- Evaluation scores and suggestions.

### 7.7 ResponseConsistencyService

Validate lexical similarity-based repetition detection.

Remember that this component checks potential repetition; it does not detect factual contradictions.

## 8. Repository Testing

Known repository implementations:

- JSONMemoryRepository.
- JSONConversationRepository.

Validate:

- Data creation.
- Data retrieval.
- Data updates.
- Data deletion.
- JSON serialization and deserialization.
- Handling of missing or invalid files.
- Persistence across application restarts.

Use temporary directories and isolated test data to avoid modifying actual application records.

## 9. Provider Testing

The platform supports eight AI providers:

1. Ollama.
2. OpenAI.
3. Anthropic.
4. Gemini.
5. Mistral.
6. Groq.
7. Cohere.
8. DeepSeek.

Provider tests should verify:

- Provider initialization.
- Model configuration.
- Authentication handling.
- Successful response handling.
- Error handling.
- Integration with application abstractions.

Use mocks for tests that should not make real network requests or consume provider credits.

## 10. Knowledge Ingestion Testing

The knowledge ingestion workflow supports:

- PDF.
- DOCX.
- TXT.
- Markdown.
- CSV.

Test:

- Supported file handling.
- Unsupported file rejection.
- Content extraction.
- Empty or invalid input handling.
- Knowledge preparation.
- Persistence and retrieval behavior.

## 11. Integration Testing

Integration testing verifies that multiple components work together.

Important workflows include:

### Knowledge workflow

```text
Document Input
      |
      v
KnowledgeAgent
      |
      v
Knowledge Processing
      |
      v
Knowledge Retrieval
```

### Memory workflow

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
JSONMemoryRepository
```

### Digital twin interaction workflow

```text
User Input
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
     v
IntelligenceService
     |
     v
Configured AI Provider
     |
     v
Generated Response
```

These diagrams describe the logical workflows. Verify exact execution order and integration details against the implementation.

## 12. Test Data Management

Follow these practices:

- Use temporary test directories.
- Keep test data separate from production data.
- Avoid modifying real memory files.
- Avoid modifying real conversation history.
- Use representative sample documents.
- Remove temporary files after testing.

## 13. Test Failure Investigation

When a test fails:

1. Read the complete error message.
2. Identify the failing component.
3. Check its dependencies.
4. Reproduce the failure.
5. Fix the underlying issue.
6. Rerun the affected test.
7. Run the complete test suite.
8. Confirm that the fix does not introduce regressions.

## 14. Testing Best Practices

- Keep tests independent.
- Use descriptive test names.
- Test both successful and failure scenarios.
- Mock external AI provider calls when appropriate.
- Use temporary storage for repository tests.
- Avoid hardcoded credentials.
- Maintain test coverage for important workflows.
- Run tests before completing changes.

## 15. Final Validation

The project completed its planned development phases.

The project owner confirmed that integrated application validation passed and final stabilization was completed.

This document describes the testing approach; exact test counts and coverage percentages should be taken from the actual PyTest reports rather than estimated.

---

**Document:** TESTING.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
