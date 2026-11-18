# Export Guide

## AI Digital Twin Agent Platform

**Version:** 1.0.0  
**Storage Format:** JSON  
**Platform:** Python and Streamlit

---

## 1. Overview

The AI Digital Twin Agent Platform uses JSON-based persistence for knowledge, memories, and conversations.

This guide explains how to back up these files, preserve application data, and prepare data for migration or recovery.

**Important:** This guide documents file-level backup and export procedures. A dedicated in-app export feature or export API is not established as part of the confirmed v1.0.0 functionality.

## 2. Data Categories

The platform maintains three primary data categories.

| Category | Purpose |
|---|---|
| Knowledge | Ingested documents, extracted content, and knowledge chunks |
| Memory | Stored personal and contextual memories |
| Conversations | Conversation sessions and message history |

## 3. JSON Storage Locations

Known default locations include:

```text
data/
├── memory/
│   └── memories.json
│
└── conversations/
    └── conversations.json
```

Knowledge storage is managed by the knowledge persistence implementation. Check the actual configured storage paths before creating a backup.

## 4. Create a Data Backup

Before exporting or modifying stored data:

1. Stop the Streamlit application.
2. Locate the application's data directory.
3. Identify the knowledge, memory, and conversation storage files.
4. Copy the relevant files to a separate backup directory.
5. Preserve the original directory structure.
6. Verify that the copied files are available.

Example backup structure:

```text
backup/
├── knowledge/
├── memory/
│   └── memories.json
└── conversations/
    └── conversations.json
```

The knowledge backup directory should contain the actual files and subdirectories used by your configured knowledge storage implementation.

## 5. Export JSON Files Manually

JSON files can be copied and preserved using standard file operations.

Example Python backup script:

```python
from pathlib import Path
import shutil

source = Path("data")
destination = Path("backup/data")

if not source.exists():
    raise FileNotFoundError(
        "Application data directory was not found."
    )

destination.parent.mkdir(
    parents=True,
    exist_ok=True,
)

shutil.copytree(
    source,
    destination,
    dirs_exist_ok=True,
)

print("Application data backup completed.")
```

Run this script while the application is stopped to avoid copying files during active writes.

## 6. Verify Exported JSON Files

Use Python to validate JSON files before relying on a backup.

```python
import json
from pathlib import Path

json_file = Path("backup/data/memory/memories.json")

if not json_file.exists():
    raise FileNotFoundError(json_file)

with json_file.open("r", encoding="utf-8") as file:
    data = json.load(file)

print("JSON file is valid.")
print("Record count:", len(data))
```

Adjust the file path for the specific JSON file being checked.

A successful JSON parse confirms syntax validity, not complete application-level data integrity.

## 7. Restore Application Data

To restore a backup:

1. Stop the application.
2. Preserve a copy of the current data directory.
3. Identify the correct backup.
4. Restore files to their original configured locations.
5. Preserve the expected directory structure.
6. Verify JSON syntax.
7. Start the application.
8. Check knowledge, memory, and conversation retrieval.

Never overwrite existing data without creating a backup first.

## 8. Data Migration

When moving the application to another machine:

1. Install the required Python environment.
2. Install application dependencies.
3. Configure the required AI providers.
4. Install and configure Ollama if local models are required.
5. Transfer the application data backup.
6. Restore JSON files to their configured paths.
7. Start the application.
8. Verify the restored data.

Keep the application version and storage structure compatible with the backup.

## 9. Export Security

Application data may contain personal information and conversation history.

Follow these precautions:

- Do not upload private memory files to public repositories.
- Do not commit conversation JSON files containing personal information.
- Protect backup directories.
- Avoid sharing API credentials.
- Use secure storage for exported files.
- Delete temporary copies when they are no longer required.

## 10. Recommended Backup Strategy

| Data | Recommended action |
|---|---|
| Knowledge | Back up knowledge storage and source files where applicable |
| Memory | Back up `memories.json` |
| Conversations | Back up `conversations.json` |
| Configuration | Preserve `.env.example`, not real secrets |
| Application code | Use Git version control |

Keep multiple backup copies when the stored information is important.

## 11. Troubleshooting

| Issue | Suggested action |
|---|---|
| Backup directory missing | Check the configured application data path |
| Invalid JSON | Preserve the original file and investigate a backup |
| Missing memories | Verify the restored memory repository path |
| Missing conversations | Check the conversation repository configuration |
| Missing knowledge | Verify the knowledge storage implementation and paths |
| Permission error | Check filesystem permissions |

## 12. Important Notes

- The application uses JSON-based persistence.
- Backup paths must match the actual project configuration.
- Stop the application before performing manual file backups or restores.
- Preserve original files until restoration has been verified.
- This guide does not imply that a dedicated export/import UI exists in v1.0.0.

---

**Document:** EXPORT_GUIDE.md  
**Project:** AI Digital Twin Agent Platform  
**Version:** 1.0.0
