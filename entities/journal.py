# Description:
# Created by Emilia on 2026-01-31

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class JournalEntry:
    """
    Entity for a single journal entry.

    Represents only the core business data:
    - `date`: unix timestamp
    - `content`: free-form user text
    """
    date: int
    content: str

    def word_count(self) -> int:
        return len(self.content.split())

    def as_dict(self) -> dict:
        # convenient for persistence layers
        return {
            "date": self.date,
            "content": self.content
        }
