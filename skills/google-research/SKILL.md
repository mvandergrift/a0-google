---
name: "google-research"
description: "Triage, search, and summarize Gmail messages. Check inbox, find specific emails, and extract key information from threads."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "gmail", "search", "summarize", "inbox"]
triggers:
  - "check my email"
  - "check my inbox"
  - "search emails"
  - "find email"
  - "summarize emails"
  - "email summary"
  - "what emails do I have"
  - "unread emails"
allowed_tools:
  - gmail_read
  - gmail_search
  - gmail_summarize
  - gmail_manage
metadata:
  complexity: "intermediate"
  category: "research"
---

# Google Email Research Skill

Triage your inbox, search for specific emails, and summarize threads.

## Workflow

### Step 1: Check Inbox
```json
{"tool": "gmail_read", "args": {"action": "inbox", "max_results": 10}}
```

### Step 2: Search for Specific Emails
```json
{"tool": "gmail_search", "args": {"query": "from:boss@company.com after:2024/03/01", "max_results": 10}}
```

### Step 3: Read a Specific Message
```json
{"tool": "gmail_read", "args": {"action": "read", "message_id": "18abc1234def5678"}}
```

### Step 4: Summarize a Thread
```json
{"tool": "gmail_summarize", "args": {"message_id": "18abc1234def5678"}}
```

### Step 5: Manage After Triage
Mark as read after reviewing:
```json
{"tool": "gmail_manage", "args": {"action": "mark_read", "message_id": "18abc1234def5678"}}
```

Archive handled messages:
```json
{"tool": "gmail_manage", "args": {"action": "archive", "message_id": "18abc1234def5678"}}
```

Star important messages:
```json
{"tool": "gmail_manage", "args": {"action": "star", "message_id": "18abc1234def5678"}}
```

## Common Search Queries

| Need | Query |
|------|-------|
| Unread emails | `is:unread` |
| From a person | `from:jane@example.com` |
| With attachments | `has:attachment` |
| Recent and unread | `is:unread newer_than:2d` |
| By subject | `subject:invoice` |
| In a label | `label:important` |

## Tips
- Start with inbox to see recent messages, then narrow with search
- Gmail search uses the same syntax as the Gmail web UI
- Summarize saves to agent memory by default — great for follow-up questions
- Use `gmail_manage` to keep the inbox tidy after triage (archive, label, star)
- List available labels with `gmail_read` action `labels`
