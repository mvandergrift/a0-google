---
name: "google-schedule"
description: "View your calendar, create events with natural language dates, and find open time slots for scheduling."
version: "1.0.0"
author: "AgentZero Google Suite Plugin"
license: "MIT"
tags: ["google", "calendar", "schedule", "events", "meetings"]
triggers:
  - "schedule a meeting"
  - "check my calendar"
  - "what's on my calendar"
  - "create an event"
  - "find a free time"
  - "am I free"
  - "book a meeting"
  - "when am I available"
allowed_tools:
  - calendar_read
  - calendar_create
  - calendar_update
  - calendar_delete
  - calendar_availability
  - contacts_search
metadata:
  complexity: "intermediate"
  category: "productivity"
---

# Google Calendar Scheduling Skill

View your schedule, create events, check availability, and find open meeting slots.

## Workflow

### Step 1: Check Current Schedule
```json
{"tool": "calendar_read", "args": {"action": "list", "date_range": "today"}}
```

Or for a specific range:
```json
{"tool": "calendar_read", "args": {"action": "list", "date_range": "next 3 days"}}
```

### Step 2: Check Availability Before Scheduling
```json
{"tool": "calendar_availability", "args": {"action": "check", "date_range": "tomorrow"}}
```

### Find Open Slots
```json
{"tool": "calendar_availability", "args": {"action": "find_slots", "date_range": "next week", "duration": "1 hour"}}
```

### Step 3: Create an Event
```json
{"tool": "calendar_create", "args": {"title": "Team Sync", "start": "tomorrow at 2pm", "duration": "1 hour"}}
```

### Create with Attendees
Look up attendee email if needed:
```json
{"tool": "contacts_search", "args": {"query": "Sarah"}}
```

Then create with attendees:
```json
{"tool": "calendar_create", "args": {"title": "1:1 with Sarah", "start": "Friday at 10am", "duration": "30 minutes", "attendees": "sarah@example.com", "description": "Weekly sync"}}
```

### Create Recurring Events
```json
{"tool": "calendar_create", "args": {"title": "Daily Standup", "start": "Monday at 9am", "duration": "15 minutes", "recurrence": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"}}
```

### Update an Existing Event
```json
{"tool": "calendar_update", "args": {"event_id": "abc123def456", "start": "3pm", "duration": "45 minutes"}}
```

### Cancel an Event
```json
{"tool": "calendar_delete", "args": {"event_id": "abc123def456", "notify": true}}
```

## Tips
- Natural language dates work: "tomorrow at 2pm", "next Tuesday", "March 15 at 10:30"
- Always check availability before scheduling to avoid conflicts
- The calendar uses the configured timezone (default: America/New_York)
- Duration supports: "30 minutes", "1 hour", "1.5 hours", "90 minutes"
- Use `contacts_search` to find attendee emails when the user says "invite Sarah"
