---
name: "google-drive"
description: "Find, upload, download, and share files on Google Drive."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "drive", "files", "upload", "share"]
triggers:
  - "find file on drive"
  - "upload to drive"
  - "google drive"
  - "share file"
  - "download from drive"
  - "list drive files"
  - "search drive"
allowed_tools:
  - drive_list
  - drive_search
  - drive_upload
  - drive_download
  - drive_share
metadata:
  complexity: "basic"
  category: "productivity"
---

# Google Drive File Management Skill

Find, upload, download, and share files on Google Drive.

## Workflow

### Step 1: Find Files

List recent files:
```json
{"tool": "drive_list", "args": {"max_results": 10}}
```

List files in a specific folder:
```json
{"tool": "drive_list", "args": {"folder_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345"}}
```

Search by name or content:
```json
{"tool": "drive_search", "args": {"query": "quarterly report"}}
```

### Step 2: Download a File
```json
{"tool": "drive_download", "args": {"file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345", "local_path": "/a0/usr/workdir/report.pdf"}}
```

### Step 3: Upload a File
```json
{"tool": "drive_upload", "args": {"file_path": "/a0/usr/workdir/analysis.xlsx", "name": "Q1 Analysis"}}
```

Upload to a specific folder:
```json
{"tool": "drive_upload", "args": {"file_path": "/a0/usr/workdir/notes.txt", "name": "Meeting Notes", "folder_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345"}}
```

### Step 4: Share a File

Share with a specific person:
```json
{"tool": "drive_share", "args": {"file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345", "email": "colleague@example.com", "role": "reader"}}
```

Create a shareable link:
```json
{"tool": "drive_share", "args": {"file_id": "0AbCdEf_GhIjKlMnOpQrStUvWxYz12345", "link_sharing": true, "role": "reader"}}
```

## Common Upload → Share Workflow

1. Upload the file to Drive
2. Note the returned file ID
3. Share via email or link

## Tips
- Google Docs, Sheets, and Slides are auto-exported as PDF when downloaded
- Downloads are restricted to safe directories (`/a0/usr/workdir/`, `/a0/usr/files/`, `/tmp/`)
- Uploads cannot come from restricted system directories
- Share roles: `reader` (view only), `writer` (can edit), `commenter` (can comment)
- Use `drive_search` for full-text search across file contents, `drive_list` for browsing by folder
