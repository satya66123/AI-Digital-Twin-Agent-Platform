# Troubleshooting Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Technology:** Python, Streamlit, Ollama, JSON, PyTest

---

## 1. Overview

This document provides troubleshooting guidance for common issues encountered while installing, configuring, running, and testing the AI Digital Twin Agent Platform.

It covers:

- Python environment issues.
- Dependency installation problems.
- Streamlit startup issues.
- AI provider connectivity.
- Ollama model availability.
- Knowledge ingestion.
- Memory persistence.
- Conversation management.
- JSON storage.
- Automated testing.

## 2. Python Environment Issues

### Problem: Python is not recognized

**Possible causes:**
- Python is not installed.
- Python is missing from the system PATH.

**Solutions:**

Verify Python:

```bash
python --version
```

If necessary, install Python 3.11 or later and configure the PATH.

### Problem: Virtual environment activation fails

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Verify that the virtual environment is active before installing dependencies.

## 3. Dependency Installation Issues

### Problem: ModuleNotFoundError

**Possible causes:**
- Required package is not installed.
- The wrong Python environment is active.

**Solutions:**

```bash
pip install -r requirements.txt
```

Verify installed packages:

```bash
pip list
```

Confirm that PyCharm or your terminal uses the intended Python interpreter.

### Problem: pip installation failure

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Retry dependency installation.

## 4. Streamlit Issues

### Problem: Streamlit command not found

Install Streamlit:

```bash
pip install streamlit
```

Verify installation:

```bash
streamlit --version
```

### Problem: Application does not start

Run the actual Streamlit entry-point file:

```bash
streamlit run <ENTRY_POINT_FILE>
```

Check:

- The entry-point path.
- Python environment.
- Installed dependencies.
- Terminal error messages.
- Application configuration.

### Problem: Application displays an error

Inspect the complete traceback and identify the failing module before changing code.

## 5. Ollama Issues

### Problem: Cannot connect to Ollama

**Possible causes:**
- Ollama is not running.
- Incorrect base URL.
- Network or local service issue.

**Solutions:**

Check the configured URL:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

Verify available models:

```bash
ollama list
```

Ensure the Ollama service is running.

### Problem: Model not found

Download the preferred default model:

```bash
ollama pull qwen2.5:1.5b
```

Verify:

```bash
ollama list
```

Confirm that the model identifier matches the application configuration.

### Problem: Local inference is slow

Possible causes include limited RAM, CPU capacity, GPU availability, or model size.

Try a smaller supported model and check system resource utilization.

## 6. Cloud AI Provider Issues

The platform supports:

- OpenAI.
- Anthropic.
- Gemini.
- Mistral.
- Groq.
- Cohere.
- DeepSeek.

### Problem: API authentication failure

Check:

1. The required API credential exists.
2. The environment variable name matches the Config implementation.
3. The credential is valid.
4. The provider account permits the requested API usage.

### Problem: Provider connection failure

Check:

- Internet connectivity.
- Provider service availability.
- API endpoint configuration.
- Provider-specific error messages.
- Model availability.

### Problem: Selected model is unavailable

Verify the model identifier against the application's configured model list and the provider's current availability.

## 7. Knowledge Ingestion Issues

### Problem: Document is not processed

Check:

- Supported file extension.
- File accessibility.
- Document validity.
- Content extraction errors.
- Required document-processing dependencies.

Supported formats:

- PDF
- DOCX
- TXT
- Markdown
- CSV

### Problem: Extracted content is empty

Possible causes:

- Empty source document.
- Unsupported document structure.
- Scanned PDF without an OCR processing step.
- Extraction failure.

Inspect the extraction result and application logs.

### Problem: Knowledge is not available during conversations

Check:

1. Whether ingestion completed successfully.
2. Whether knowledge was persisted.
3. Whether retrieval returns relevant content.
4. Whether IntelligenceContextBuilder receives the retrieved knowledge.

Verify the actual knowledge storage configuration.

## 8. Memory Management Issues

### Problem: Memories are not saved

Check the default memory repository:

```text
data/memory/memories.json
```

Verify:

- Directory existence.
- File permissions.
- JSON serialization.
- Repository configuration.
- Application error logs.

### Problem: Memory retrieval returns no results

Check:

- Whether memories were created.
- Whether the repository contains the expected records.
- Whether search criteria are correct.
- Whether the memory type is appropriate.

### Problem: JSON file is invalid

Validate the JSON file:

```python
import json
from pathlib import Path

path = Path("data/memory/memories.json")

with path.open("r", encoding="utf-8") as file:
    data = json.load(file)

print("Memory JSON is valid.")
```

Preserve the original file before attempting recovery.

## 9. Conversation Management Issues

### Problem: Conversation history is missing

Check the default conversation repository:

```text
data/conversations/conversations.json
```

Verify:

- The configured repository path.
- File existence.
- JSON validity.
- Filesystem permissions.
- Conversation identifiers.

### Problem: Messages are not persisted

Inspect ConversationService and JSONConversationRepository behavior.

Verify that message updates are successfully written to the configured JSON file.

## 10. Personalization Issues

### Problem: Personalization information is not identified

Check whether stored memories contain relevant metadata or keywords.

DigitalTwinPersonalizationService uses metadata and keyword-based matching to categorize:

- Profile.
- Preferences.
- Expertise.

Review the available memory information and categorization logic.

## 11. Response Evaluation Issues

### Problem: Response quality score is unexpected

ResponseQualityService checks characteristics such as:

- Empty responses.
- Very short responses.
- Repeated sentences.

Review the evaluation rules and the actual response content.

### Problem: Repetitive responses are not detected

ResponseConsistencyService uses lexical Jaccard similarity.

Different wording with similar meaning may not be identified as repetition. This component does not detect factual contradictions.

## 12. JSON Persistence Issues

### Problem: Permission denied

Check filesystem permissions for the data directory and repository files.

### Problem: Stored data is missing

Check:

- Application working directory.
- Repository configuration.
- Expected file paths.
- Whether the application is using a different data location.

### Problem: Data corruption

1. Stop the application.
2. Preserve the affected files.
3. Validate JSON syntax.
4. Identify a known-good backup.
5. Restore carefully.
6. Verify application retrieval.

Refer to `EXPORT_GUIDE.md` for backup and restoration guidance.

## 13. Testing Issues

### Problem: PyTest command not found

Install PyTest:

```bash
pip install pytest
```

### Problem: Tests fail

Run:

```bash
pytest -v
```

Review:

- Failure messages.
- Tracebacks.
- Test fixtures.
- Mock configurations.
- Dependency injection.
- Test data paths.

Run the affected test independently before executing the complete test suite again.

## 14. General Debugging Workflow

Follow this troubleshooting sequence:

1. Reproduce the issue.
2. Read the complete error message.
3. Identify the affected component.
4. Inspect configuration and dependencies.
5. Check application logs.
6. Verify data files and permissions.
7. Apply the smallest appropriate fix.
8. Rerun the affected test.
9. Run the complete test suite.
10. Confirm that the issue is resolved.

## 15. Important Recommendations

- Keep Python dependencies consistent.
- Use the correct virtual environment.
- Verify provider credentials.
- Keep Ollama running when using local inference.
- Back up JSON files before modifying them.
- Never expose API keys in logs.
- Use isolated test data.
- Check the actual repository configuration before changing file paths.

---

**Document:** TROUBLESHOOTING.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
