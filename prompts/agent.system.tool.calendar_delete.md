## calendar_delete

Delete a calendar event. Optionally send cancellation notifications to attendees.

**Arguments:**
- **event_id** (string, required): The ID of the event to delete.
- **calendar_id** (string, optional): Calendar containing the event. Defaults to the primary calendar.
- **send_notifications** (boolean, optional): Whether to send cancellation notifications to attendees. Defaults to `true`.

**Examples:**

Delete an event and notify attendees:
~~~json
{
  "event_id": "abc123def456"
}
~~~

Delete an event without notifying attendees:
~~~json
{
  "event_id": "abc123def456",
  "send_notifications": false
}
~~~

Delete an event from a specific calendar:
~~~json
{
  "event_id": "abc123def456",
  "calendar_id": "work@group.calendar.google.com",
  "send_notifications": true
}
~~~
