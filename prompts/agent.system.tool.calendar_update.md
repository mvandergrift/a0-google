## calendar_update

Update existing calendar events. Modify the title, time, description, location, or attendees of an event.

**Arguments:**
- **event_id** (string, required): The ID of the event to update.
- **title** (string, optional): Updated event title/summary.
- **start** (string, optional): Updated start time. Format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`.
- **end** (string, optional): Updated end time. Format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`.
- **description** (string, optional): Updated event description or notes.
- **location** (string, optional): Updated event location.
- **attendees** (list of strings, optional): Updated list of attendee email addresses. Replaces the existing attendee list.
- **calendar_id** (string, optional): Calendar containing the event. Defaults to the primary calendar.

**Examples:**

Reschedule an event:
~~~json
{
  "event_id": "abc123def456",
  "start": "2026-03-18T15:00:00",
  "end": "2026-03-18T16:00:00"
}
~~~

Update title and add attendees:
~~~json
{
  "event_id": "abc123def456",
  "title": "Expanded planning session",
  "attendees": ["alice@company.com", "bob@company.com", "carol@company.com"]
}
~~~

Change location and description:
~~~json
{
  "event_id": "abc123def456",
  "location": "Virtual - Zoom",
  "description": "Moved to virtual format. Zoom link: https://zoom.us/j/123456"
}
~~~
