## calendar_availability

Check calendar availability. Find free time slots for scheduling or view busy periods across one or more calendars.

**Arguments:**
- **action** (string, required): The availability operation to perform. One of `free_slots` or `busy`.
  - `free_slots` — Find available time slots of a given duration within a date range.
  - `busy` — Show all busy periods within a date range.
- **date** (string, optional): Single date to check. Format: `YYYY-MM-DD`. Used for checking availability on a specific day.
- **start_date** (string, optional): Start of the date range. Format: `YYYY-MM-DD`. Used with `end_date` for multi-day queries.
- **end_date** (string, optional): End of the date range. Format: `YYYY-MM-DD`.
- **duration_minutes** (integer, optional): Minimum duration of free slots to find, in minutes. Used with `free_slots` action. Defaults to 30.
- **calendars** (list of strings, optional): List of calendar IDs to check. Defaults to the primary calendar only.

**Examples:**

Find 60-minute free slots today:
~~~json
{
  "action": "free_slots",
  "date": "2026-03-13",
  "duration_minutes": 60
}
~~~

Find free slots across a date range on multiple calendars:
~~~json
{
  "action": "free_slots",
  "start_date": "2026-03-15",
  "end_date": "2026-03-19",
  "duration_minutes": 45,
  "calendars": ["primary", "work@group.calendar.google.com"]
}
~~~

View busy periods for a specific day:
~~~json
{
  "action": "busy",
  "date": "2026-03-14"
}
~~~

View busy periods across multiple calendars for a week:
~~~json
{
  "action": "busy",
  "start_date": "2026-03-16",
  "end_date": "2026-03-20",
  "calendars": ["primary", "team@group.calendar.google.com"]
}
~~~
