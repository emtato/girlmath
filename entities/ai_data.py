from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional



class AiInfo:
    """
    Entity for an AI request.

    Holds exactly what the frontend sends: (to be modified to include specific info from db to send to ai?)
    - content: user prompt
    - date: unix timestamp
    - context: raw dict of retrieval options
    """
    content: str
    #date: int
    read_journal: bool
    read_quizzes: bool
    user_ID: str

    def __init__(self, user_ID: str, content: str, read_journal: bool, read_quizzes: bool):
        self.user_ID = user_ID
        self.content = content
        #self.date = date
        self.read_journal = read_journal
        self.read_quizzes = read_quizzes



