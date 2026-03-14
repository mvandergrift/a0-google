---
name: "google-tasks"
description: "Manage Google Tasks: view task lists, create tasks, mark complete, and organize to-dos."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "tasks", "todo", "productivity"]
triggers:
  - "show my tasks"
  - "add a task"
  - "create task"
  - "complete task"
  - "google tasks"
  - "my todo list"
  - "mark task done"
allowed_tools:
  - tasks_list
  - tasks_manage
metadata:
  complexity: "basic"
  category: "productivity"
---

# Google Tasks Management Skill

View, create, complete, and organize tasks across Google Tasks lists.

## Workflow

### Step 1: View Task Lists
```json
{"tool": "tasks_list", "args": {"action": "lists"}}
```

### Step 2: View Tasks in a List
```json
{"tool": "tasks_list", "args": {"action": "tasks", "list_id": "MTIzNDU2Nzg5"}}
```

Or view all tasks across all lists:
```json
{"tool": "tasks_list", "args": {"action": "tasks"}}
```

### Step 3: Create a Task
```json
{"tool": "tasks_manage", "args": {"action": "create", "title": "Review Q1 report", "notes": "Focus on revenue section", "due": "Friday"}}
```

Create in a specific list:
```json
{"tool": "tasks_manage", "args": {"action": "create", "title": "Buy groceries", "list_id": "MTIzNDU2Nzg5"}}
```

### Step 4: Complete a Task
```json
{"tool": "tasks_manage", "args": {"action": "complete", "task_id": "dGFzay0xMjM0NTY3ODk"}}
```

### Step 5: Delete a Task
```json
{"tool": "tasks_manage", "args": {"action": "delete", "task_id": "dGFzay0xMjM0NTY3ODk"}}
```

### Update a Task
```json
{"tool": "tasks_manage", "args": {"action": "update", "task_id": "dGFzay0xMjM0NTY3ODk", "title": "Updated title", "due": "next Monday"}}
```

## Tips
- Tasks service is disabled by default — enable it in Google Suite plugin settings, then re-authorize
- If no `list_id` is specified, the default task list ("My Tasks") is used
- Due dates support natural language: "tomorrow", "next Friday", "March 20"
- Use task lists to organize by project or category
- The `notes` field supports multi-line text for additional details
