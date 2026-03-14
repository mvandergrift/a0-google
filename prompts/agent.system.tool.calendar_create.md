## calendar_create

Create new calendar events. Supports setting time, duration, location, description, attendees, and recurrence rules.

**Arguments:**
- **title** (string, required): Event title/summary.
- **start** (string, required): Event start time. Format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD` for all-day events.
- **end** (string, optional): Event end time. Format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`. If omitted, `duration` is used.
- **duration** (integer, optional): Event duration in minutes. Used when `end` is not provided. Defaults to 60.
- **description** (string, optional): Event description or notes.
- **location** (string, optional): Event location (physical address or virtual meeting link).
- **attendees** (list of strings, optional): List of attendee email addresses to invite.
- **recurrence** (string, optional): Recurrence rule in RRULE format (e.g., `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR`).
- **calendar_id** (string, optional): Calendar to create the event in. Defaults to the primary calendar.

**Examples:**

Create a simple one-hour meeting:
~~~json
{
  "title": "Team standup",
  "start": "2026-03-15T09:00:00",
  "duration": 30
}
~~~

Create an event with attendees and location:
~~~json
{
  "title": "Q1 Review",
  "start": "2026-03-20T14:00:00",
  "end": "2026-03-20T15:30:00",
  "location": "Conference Room B",
  "description": "Quarterly review of project milestones and deliverables.",
  "attendees": ["alice@company.com", "bob@company.com"]
}
~~~

Create a recurring weekly event:
~~~json
{
  "title": "Weekly sync",
  "start": "2026-03-16T10:00:00",
  "duration": 45,
  "recurrence": "RRULE:FREQ=WEEKLY;BYDAY=MO",
  "attendees": ["team@company.com"]
}
~~~

Create an all-day event:
~~~json
{
  "title": "Company offsite",
  "start": "2026-04-01",
  "end": "2026-04-03",
  "location": "Mountain View Campus",
  "description": "Annual company offsite event."
}
~~~
