# Description:
# Created by Emilia on 2026-01-31
from datetime import datetime
from copy import deepcopy

def convert_unix_time(entry: dict) -> dict:
    """
    Takes a dict with a Unix timestamp under key 'date' and returns a copy
    with a human-readable date string.

    - Accepts int/float timestamps and numeric strings (e.g. "1706668800").
    - If 'date' is missing or not parseable as a unix timestamp, returns the entry unchanged.
    - Stores the original unix timestamp under 'date_unix' for progression/trends.
    - Stores the formatted string under 'date_str'.
    - Keeps backward-compatibility by also setting 'date' to the formatted string.
    """
    new_entry = deepcopy(entry)

    ts_raw = new_entry.get("date")
    if ts_raw is None:
        return new_entry

    # Some existing DB records may store unix time as a string.
    try:
        ts = int(ts_raw)
    except (TypeError, ValueError):
        return new_entry

    dt = datetime.fromtimestamp(ts)

    hour = dt.strftime("%I").lstrip("0")  # remove leading zero
    am_pm = dt.strftime("%p").lower()

    formatted = f"{dt.year}:{dt.month:02d}:{dt.day:02d} {hour}{am_pm}"

    # Preserve unix timestamp for trend/progression uses.
    new_entry["date_unix"] = ts
    new_entry["date_str"] = formatted

    # Backwards compatible: existing code expects `date` to be the display string.
    new_entry["date"] = formatted

    return new_entry
