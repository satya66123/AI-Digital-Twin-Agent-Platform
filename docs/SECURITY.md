# Security Guidelines

## AI Digital Twin Agent Platform

**Version:** 1.0.0

---

## 1. Overview

Security is important for the AI Digital Twin Agent Platform because it handles AI provider credentials, knowledge documents, personal memories, and conversation history.

This document describes security practices for configuring, operating, and maintaining the application.

## 2. API Key Management

The platform integrates eight AI providers:

- Ollama
- OpenAI
- Anthropic
- Gemini
- Mistral
- Groq
- Cohere
- DeepSeek

Follow these practices:

- Store cloud provider API keys in environment variables.
- Keep `.env` files private.
- Never hardcode API credentials.
- Never commit real API keys to GitHub.
- Use `.env.example` with placeholder values.
- Rotate credentials if they are accidentally exposed.

## 3. Environment Configuration

Use the project's `.env.example` as the configuration reference.

Recommended Git ignore entries:

```gitignore
.env
.env.*
!.env.example
```

Review the existing `.gitignore` before applying changes to avoid overriding other project-specific rules.

## 4. Personal Data Protection

The platform stores information that may contain personal or sensitive content.

Known default storage locations:

```text
data/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

Security recommendations:

- Restrict access to application data directories.
- Avoid sharing memory files publicly.
- Protect conversation history.
- Secure backup files.
- Avoid storing unnecessary personal information.
- Delete data when it is no longer required.

## 5. Knowledge Document Security

Uploaded documents may contain confidential information.

Recommended practices:

- Validate uploaded file types.
- Reject unsupported file formats.
- Apply appropriate file-size limits.
- Avoid processing untrusted files without validation.
- Protect extracted document content.
- Restrict access to stored knowledge.

Supported document formats:

- PDF
- DOCX
- TXT
- Markdown
- CSV

## 6. AI Provider Security

When using cloud AI providers:

- Understand the provider's data handling policies.
- Avoid sending unnecessary personal information.
- Protect authentication credentials.
- Handle provider errors without exposing secrets.
- Verify provider configuration before deployment.

When using Ollama, protect access to the local service and ensure it is not unintentionally exposed to untrusted networks.

## 7. Application Security

Recommended application practices:

- Validate user inputs.
- Handle exceptions safely.
- Avoid displaying internal stack traces to end users.
- Avoid logging API keys or private user content.
- Keep dependencies updated.
- Apply appropriate access restrictions.
- Review file operations for path traversal risks.

## 8. JSON Persistence Security

The platform uses JSON-based persistence for memory and conversation data.

Known repositories:

- JSONMemoryRepository
- JSONConversationRepository

Recommendations:

- Validate JSON before loading it.
- Preserve backups before modifying stored files.
- Restrict filesystem permissions.
- Protect stored data from unauthorized modification.
- Avoid concurrent writes without appropriate safeguards.

## 9. GitHub Security

Before pushing code to GitHub:

1. Check that `.env` is excluded.
2. Search for accidentally committed credentials.
3. Review staged files.
4. Exclude private memory and conversation data.
5. Avoid uploading confidential documents.
6. Review dependencies and configuration files.

Example commands:

```bash
git status
git diff --cached
```

If a credential has been committed, removing it from the latest commit alone may not remove it from Git history. Rotate the exposed credential and follow an appropriate repository cleanup process.

## 10. Backup and Recovery

- Create regular backups of important JSON data.
- Store backups in a protected location.
- Avoid keeping the only backup on the same machine.
- Verify JSON validity before restoration.
- Test restoration using a safe copy of the data.

Refer to `EXPORT_GUIDE.md` for backup and restoration instructions.

## 11. Deployment Considerations

Before deploying the application:

- Configure secrets securely.
- Restrict access to private user data.
- Use HTTPS through an appropriately configured deployment environment.
- Review file upload handling.
- Restrict access to local services.
- Review provider permissions and network access.
- Establish a backup and recovery procedure.

## 12. Security Incident Response

If credentials or private data are exposed:

1. Identify the exposed information.
2. Revoke or rotate affected credentials.
3. Restrict access to affected resources.
4. Review Git history and logs where applicable.
5. Assess potential data exposure.
6. Restore affected data from a trusted backup if required.
7. Document the incident and corrective actions.

## 13. Important Security Limitations

This document describes recommended security practices. It does not claim that the application has undergone an independent security audit, penetration test, or formal compliance certification.

Production deployment should include a dedicated security review.

---

**Document:** SECURITY.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
