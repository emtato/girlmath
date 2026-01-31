# Description:
# Created by Emilia on 2026-01-31

from __future__ import annotations
from dataclasses import dataclass


class JournalEntry:
    """
    Entity for a single journal entry.

    Represents only the core business data:
    - `date`: unix timestamp
    - `content`: free-form user text
    """
    date: int
    content: str

    def __init__(self, id: str, user_ID: str, date: int, content: str):
        self.id = id
        self.date = date
        self.content = content

    def word_count(self) -> int:
        return len(self.content.split())

    def as_dict(self) -> dict:
        # convenient for persistence layers
        return {"date": self.date, "content": self.content}
