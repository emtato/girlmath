from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class AiInfo:
    """
    Entity for an AI request.

    Holds exactly what the frontend sends: (to be modified to include specific info from db to send to ai?)
    - content: user prompt
    - date: unix timestamp
    - context: raw dict of retrieval options
    """
    content: str
    date: int
    context: Optional[Dict] = None

    def as_dict(self) -> dict:
        return {
            "content": self.content,
            "date": self.date,
            "context": self.context
        }
