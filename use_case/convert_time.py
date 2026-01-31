# Description:
# Created by Emilia on 2026-01-31
from datetime import datetime
from copy import deepcopy

def convert_unix_time(entry: dict) -> dict:
    """
    Takes a dict with a Unix timestamp under key 'date'
    and returns the same dict with 'date' converted to
    'YYYY:MM:DD H(am/pm)' format.
    """
    new_entry = deepcopy(entry)

    ts = new_entry.get("date")
    if ts is None:
        return new_entry

    dt = datetime.fromtimestamp(ts)

    hour = dt.strftime("%I").lstrip("0")  # remove leading zero
    am_pm = dt.strftime("%p").lower()

    new_entry["date"] = f"{dt.year}:{dt.month:02d}:{dt.day:02d} {hour}{am_pm}"

    return new_entry
