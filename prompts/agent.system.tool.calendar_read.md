## calendar_read

Read calendar events. View today's schedule, upcoming events, events within a date range, a specific event's details, or list available calendars.

**Arguments:**
- **action** (string, required): The read operation to perform. One of `today`, `upcoming`, `range`, `event`, or `calendars`.
  - `today` — Get all events for today.
  - `upcoming` — Get upcoming events for the next N days.
  - `range` — Get events within a specific date range.
  - `event` — Get details of a specific event by ID.
  - `calendars` — List all available calendars.
- **calendar_id** (string, optional): Calendar to read from. Defaults to the primary calendar.
- **days** (integer, optional): Number of days to look ahead when `action` is `upcoming`. Defaults to 7.
- **start_date** (string, optional): Start of date range. Format: `YYYY-MM-DD`. Required when `action` is `range`.
- **end_date** (string, optional): End of date range. Format: `YYYY-MM-DD`. Required when `action` is `range`.
- **event_id** (string, optional): The event ID to retrieve. Required when `action` is `event`.
- **limit** (integer, optional): Maximum number of events to return. Defaults to 25.

**Examples:**

Get today's events:
~~~json
{
  "action": "today"
}
~~~

Get upcoming events for the next 14 days:
~~~json
{
  "action": "upcoming",
  "days": 14,
  "limit": 50
}
~~~

Get events in a specific date range from a specific calendar:
~~~json
{
  "action": "range",
  "start_date": "2026-03-15",
  "end_date": "2026-03-22",
  "calendar_id": "work@group.calendar.google.com"
}
~~~

List all available calendars:
~~~json
{
  "action": "calendars"
}
~~~
