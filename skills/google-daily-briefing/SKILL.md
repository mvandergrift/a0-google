---
name: "google-daily-briefing"
description: "Get a cross-service morning briefing combining inbox highlights, today's calendar, and pending tasks."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "briefing", "overview", "productivity"]
triggers:
  - "morning briefing"
  - "daily briefing"
  - "what's my day look like"
  - "daily overview"
  - "start my day"
  - "catch me up"
  - "what do I have today"
allowed_tools:
  - gmail_read
  - gmail_search
  - calendar_read
  - tasks_list
metadata:
  complexity: "intermediate"
  category: "productivity"
---

# Google Daily Briefing Skill

Generate a cross-service overview combining email highlights, today's calendar, and pending tasks into a single briefing.

## Workflow

Run these three checks and present a unified summary:

### Step 1: Today's Calendar
```json
{"tool": "calendar_read", "args": {"action": "list", "date_range": "today"}}
```

### Step 2: Inbox Highlights
```json
{"tool": "gmail_read", "args": {"action": "inbox", "max_results": 10}}
```

Or focus on unread only:
```json
{"tool": "gmail_search", "args": {"query": "is:unread", "max_results": 10}}
```

### Step 3: Pending Tasks
```json
{"tool": "tasks_list", "args": {"action": "tasks"}}
```

### Step 4: Present the Briefing

Combine the results into a structured summary:

**Format:**
```
📅 Today's Schedule
- 9:00 AM — Team Standup (30 min)
- 2:00 PM — 1:1 with Manager (1 hr)
- 4:30 PM — Design Review (45 min)

📧 Inbox (X unread)
- [Important] Budget approval from Finance
- [Action needed] PR review request from Sarah
- [FYI] Weekly newsletter

✅ Pending Tasks
- Complete Q1 report (due today)
- Review design mockups
- Update project timeline
```

## Tips
- Run all three steps before presenting — users expect a complete picture
- Highlight anything time-sensitive (meetings starting soon, overdue tasks, urgent emails)
- If Tasks service is disabled, skip Step 3 and note it in the briefing
- This skill works best as a morning routine — the user says "brief me" and gets everything at once
