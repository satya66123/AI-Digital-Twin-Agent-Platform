# Contributing Guidelines

## AI Digital Twin Agent Platform

**Version:** 1.0.0

Thank you for your interest in contributing to the AI Digital Twin Agent Platform!

This document explains the contribution process, development standards, architecture guidelines, and expectations for contributors.

---

## 1. Project Overview

The AI Digital Twin Agent Platform is a Python-based Generative AI application supporting:

- 8 AI providers and 30 configured models.
- Knowledge ingestion and retrieval.
- Four memory types.
- Persistent multi-turn conversations.
- Personalized Digital Twin interactions.
- Response quality evaluation.
- Response consistency evaluation.

Contributions should improve the platform while preserving its existing architecture.

## 2. Development Environment

Recommended development environment:

- Python 3.11+
- PyCharm or another Python IDE.
- Git.
- Streamlit.
- PyTest.
- Ollama for local model execution.

## 3. Getting Started

### Step 1: Fork the Repository

Create your own fork of the project repository.

### Step 2: Clone Your Fork

```bash
git clone <YOUR_FORK_URL>
cd <PROJECT_DIRECTORY>
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

Create your `.env` file using `.env.example` as a reference.

Do not commit real API keys or secrets.

## 4. Branching Strategy

Use descriptive branch names.

Examples:

```text
feature/advanced-memory-search
feature/new-ai-provider
fix/conversation-persistence
fix/response-validation
refactor/knowledge-service
docs/update-user-guide
```

Recommended branch categories:

| Prefix | Purpose |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `refactor/` | Code improvements |
| `docs/` | Documentation updates |
| `test/` | Testing improvements |

## 5. Coding Standards

Contributors should:

- Use clear and descriptive names.
- Follow Python conventions.
- Use type hints where appropriate.
- Keep functions focused.
- Avoid unnecessary code duplication.
- Handle exceptions appropriately.
- Use meaningful logging.
- Maintain readable code.
- Avoid hardcoded credentials.
- Preserve existing application behavior.

## 6. Architecture Guidelines

The project follows a four-layer architecture.

```text
app/
├── presentation/
├── application/
├── domain/
└── infrastructure/
```

### Presentation Layer

Responsible for user interface and application presentation.

### Application Layer

Responsible for agents, services, use cases, and orchestration.

### Domain Layer

Responsible for core entities, interfaces, and business rules.

### Infrastructure Layer

Responsible for external providers, repositories, and persistence.

Contributors should place new functionality in the appropriate layer.

## 7. SOLID Principles

All contributions should respect the project's SOLID foundation.

### Single Responsibility Principle

Each class should have a focused responsibility.

### Open/Closed Principle

New functionality should be introduced without unnecessary changes to existing stable components.

### Liskov Substitution Principle

Implementations should respect their parent abstractions and interface contracts.

### Interface Segregation Principle

Avoid unnecessarily large interfaces.

### Dependency Inversion Principle

Application logic should depend on abstractions rather than concrete infrastructure implementations.

## 8. AI Provider Contributions

When adding a new AI provider:

1. Implement the appropriate provider abstraction.
2. Follow the existing provider conventions.
3. Register the provider through ProviderFactory.
4. Configure required environment variables.
5. Handle provider-specific errors.
6. Verify model discovery and generation.
7. Preserve compatibility with existing providers.

Do not remove or replace existing provider registrations without an approved architectural change.

## 9. Memory Contributions

Memory-related changes should preserve:

- SHORT_TERM.
- LONG_TERM.
- EPISODIC.
- SEMANTIC.

Memory persistence must remain compatible with the existing JSON repository design unless a separately approved architecture change is introduced.

Memory consolidation must avoid deleting original data before successful persistence of the consolidated memory.

## 10. Knowledge Contributions

Knowledge-related changes should preserve:

- Document validation.
- Document extraction.
- Text chunking.
- Metadata processing.
- JSON persistence.
- Knowledge retrieval.
- Ingestion recovery behavior.

## 11. Conversation Contributions

Conversation-related changes should preserve:

- Conversation creation.
- User and assistant message roles.
- Conversation history.
- Persistent storage.
- Archiving.
- Deletion.
- Multi-turn interaction.

Changes should not silently discard existing conversation data.

## 12. Testing Guidelines

Use PyTest for relevant tests.

Before submitting changes:

1. Run relevant tests.
2. Check application imports.
3. Verify affected service behavior.
4. Check compatibility with existing functionality.
5. Test the integrated workflow when appropriate.

Do not claim test coverage or passing results without actually running the tests.

## 13. Documentation Guidelines

Update the relevant documentation when introducing changes.

Documentation should be:

- Clear.
- Accurate.
- Consistent with the implementation.
- Free from invented capabilities.
- Updated alongside important API or architecture changes.

## 14. Security Guidelines

Never commit:

- API keys.
- Passwords.
- Access tokens.
- Private user information.
- Sensitive JSON storage files.
- Production credentials.

Review staged changes before committing.

## 15. Commit Message Guidelines

Use descriptive commit messages.

Examples:

```text
feat: add advanced memory retrieval

feat: integrate new AI provider

fix: resolve conversation persistence issue

refactor: improve intelligence context builder

test: add response quality service tests

docs: update architecture documentation
```

## 16. Pull Request Process

Before submitting a pull request:

1. Synchronize your branch with the latest project changes.
2. Review your code.
3. Run relevant tests.
4. Check that no secrets are included.
5. Update documentation where necessary.
6. Describe the changes clearly.
7. Explain any architectural impact.

## 17. Pull Request Description

A useful pull request should include:

- Summary of changes.
- Reason for the changes.
- Main files modified.
- Testing performed.
- Screenshots when UI changes are involved.
- Known limitations.

## 18. Contribution Review

Contributions may be reviewed for:

- Correctness.
- Maintainability.
- Architecture compatibility.
- Security.
- Performance.
- Test quality.
- Documentation accuracy.

## 19. Project Development Workflow

The original project development cycle is:

**PLAN → DESIGN → IMPLEMENT → TEST → FIX → STABILIZE**

New contributions should follow an appropriate version of this workflow.

## 20. Thank You

Thank you for helping improve the AI Digital Twin Agent Platform.

Constructive contributions help maintain a reliable, modular, extensible, and maintainable Generative AI application.

---

**Document:** CONTRIBUTING.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
