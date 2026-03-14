"""Natural language date parsing helpers.

Converts human-friendly date/time expressions to ISO 8601 format.
"""

import re
from datetime import datetime, timedelta, time
from typing import Optional, Tuple
from zoneinfo import ZoneInfo


def parse_datetime(text: str, timezone: str = "America/New_York") -> Optional[str]:
    """Parse a natural language datetime expression to ISO 8601 string.

    Supports:
    - ISO 8601 (passthrough): "2026-03-15T14:00:00"
    - Date only: "2026-03-15" -> "2026-03-15"
    - "today", "tomorrow", "yesterday"
    - "next Monday", "this Friday"
    - "today at 2pm", "tomorrow at 14:00"
    - "in 2 hours", "in 30 minutes"
    """
    text = text.strip()

    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", text):
        return text
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return text

    try:
        now = datetime.now(ZoneInfo(timezone)).replace(tzinfo=None)
    except Exception:
        now = datetime.now()

    base_text, time_part = _split_time(text)

    dt = _parse_date_component(base_text, now)
    if dt is None:
        return None

    if time_part:
        parsed_time = _parse_time(time_part)
        if parsed_time:
            dt = dt.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0)
    elif dt.hour == 0 and dt.minute == 0 and "T" not in text:
        return dt.strftime("%Y-%m-%d")

    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def _split_time(text: str) -> Tuple[str, str]:
    """Split 'tomorrow at 2pm' into ('tomorrow', '2pm')."""
    match = re.search(r"\s+at\s+(.+)$", text, re.IGNORECASE)
    if match:
        return text[:match.start()].strip(), match.group(1).strip()
    return text, ""


def _parse_date_component(text: str, now: datetime) -> Optional[datetime]:
    """Parse the date portion of a natural language expression."""
    lower = text.lower().strip()

    if lower == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif lower == "tomorrow":
        return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif lower == "yesterday":
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    day_match = re.match(r"(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", lower)
    if day_match:
        prefix = day_match.group(1)
        target_day = _day_name_to_number(day_match.group(2))
        if target_day is not None:
            current_day = now.weekday()
            if prefix == "next":
                days_ahead = (target_day - current_day + 7) % 7
                if days_ahead == 0:
                    days_ahead = 7
            else:
                days_ahead = (target_day - current_day + 7) % 7
            dt = now + timedelta(days=days_ahead)
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    day_only = re.match(r"^(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", lower)
    if day_only:
        target_day = _day_name_to_number(day_only.group(1))
        if target_day is not None:
            current_day = now.weekday()
            days_ahead = (target_day - current_day + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            dt = now + timedelta(days=days_ahead)
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    relative = re.match(r"in\s+(\d+)\s+(hour|minute|min|day|week)s?", lower)
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
        if unit in ("hour",):
            return now + timedelta(hours=amount)
        elif unit in ("minute", "min"):
            return now + timedelta(minutes=amount)
        elif unit == "day":
            return now + timedelta(days=amount)
        elif unit == "week":
            return now + timedelta(weeks=amount)

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%B %d, %Y", "%B %d", "%b %d, %Y", "%b %d"):
        try:
            dt = datetime.strptime(text.strip(), fmt)
            if dt.year == 1900:
                dt = dt.replace(year=now.year)
            return dt
        except ValueError:
            continue

    return None


def _parse_time(text: str) -> Optional[time]:
    """Parse a time string like '2pm', '14:00', '2:30 PM'."""
    text = text.strip().lower()

    match = re.match(r"^(\d{1,2})\s*(am|pm)$", text)
    if match:
        hour = int(match.group(1))
        meridiem = match.group(2)
        if meridiem == "pm" and hour != 12:
            hour += 12
        elif meridiem == "am" and hour == 12:
            hour = 0
        return time(hour=hour, minute=0)

    match = re.match(r"^(\d{1,2}):(\d{2})\s*(am|pm)?$", text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        meridiem = match.group(3)
        if meridiem == "pm" and hour != 12:
            hour += 12
        elif meridiem == "am" and hour == 12:
            hour = 0
        return time(hour=hour, minute=minute)

    match = re.match(r"^(\d{1,2}):(\d{2})$", text)
    if match:
        return time(hour=int(match.group(1)), minute=int(match.group(2)))

    return None


def _day_name_to_number(name: str) -> Optional[int]:
    """Convert day name to weekday number (Monday=0)."""
    days = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
    }
    return days.get(name.lower())


def parse_duration(text: str) -> Optional[int]:
    """Parse a duration string into minutes.

    Supports: "1 hour", "30 minutes", "1.5 hours", "1h30m", "90min", "2h"
    """
    text = str(text).strip().lower()

    match = re.match(r"^(\d+)h\s*(?:(\d+)\s*m(?:in)?)?$", text)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes

    match = re.match(r"^(\d+)\s*m(?:in(?:ute)?s?)?$", text)
    if match:
        return int(match.group(1))

    match = re.match(r"^([\d.]+)\s*hours?$", text)
    if match:
        return int(float(match.group(1)) * 60)

    match = re.match(r"^(\d+)\s*(?:minutes?|mins?)$", text)
    if match:
        return int(match.group(1))

    if text.isdigit():
        return int(text)

    return None


def compute_end_time(start: str, duration_minutes: int) -> str:
    """Given an ISO start time and duration, compute the end time."""
    from dateutil.parser import isoparse
    start_dt = isoparse(start)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return end_dt.strftime("%Y-%m-%dT%H:%M:%S")
