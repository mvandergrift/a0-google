---
name: "google-communicate"
description: "Compose and send emails, create drafts, and manage recipients using Gmail and Contacts."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "gmail", "email", "send", "draft"]
triggers:
  - "send email"
  - "send an email"
  - "email someone"
  - "compose email"
  - "draft email"
  - "write an email"
  - "reply to email"
  - "forward email"
allowed_tools:
  - gmail_send
  - gmail_draft
  - gmail_read
  - contacts_search
metadata:
  complexity: "basic"
  category: "communication"
---

# Google Email Communication Skill

Compose and send emails, create drafts, and look up recipients via Contacts.

## Workflow

### Step 1: Find the Recipient (if needed)

If you don't have the email address, search contacts first:
```json
{"tool": "contacts_search", "args": {"query": "John Smith"}}
```

### Step 2: Send an Email
```json
{"tool": "gmail_send", "args": {"to": "john@example.com", "subject": "Meeting follow-up", "body": "Hi John,\n\nThanks for the great discussion today.\n\nBest regards"}}
```

### Send with CC/BCC
```json
{"tool": "gmail_send", "args": {"to": "john@example.com", "cc": "team@example.com", "subject": "Project update", "body": "Here's the latest update..."}}
```

### Create a Draft Instead
```json
{"tool": "gmail_draft", "args": {"action": "create", "to": "john@example.com", "subject": "Proposal", "body": "Draft content here..."}}
```

### List Existing Drafts
```json
{"tool": "gmail_draft", "args": {"action": "list"}}
```

### Send a Draft
```json
{"tool": "gmail_draft", "args": {"action": "send", "draft_id": "r1234567890"}}
```

### Reply to a Message
First read the original message to get the message ID and thread context:
```json
{"tool": "gmail_read", "args": {"action": "read", "message_id": "18abc1234def5678"}}
```

Then reply (the tool handles In-Reply-To and threading):
```json
{"tool": "gmail_send", "args": {"to": "sender@example.com", "subject": "Re: Original subject", "body": "Thanks for the update...", "reply_to": "18abc1234def5678"}}
```

## Tips
- If a recipient allow-list is configured, only those addresses can be emailed
- Use drafts when you want the user to review before sending
- The `contacts_search` tool searches by name or email — use it when the user says "email John" without an address
- Long email bodies are supported (up to 50,000 characters)
