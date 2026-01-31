# Description: overall file to save every type of data
# Created by Emilia on 2026-01-31

from entities.quiz import QuizEntry
from entities.journal import JournalEntry
from db import quiz_crud
from db import journal_crud


async def save_quiz(quiz_data: QuizEntry) -> dict:
    """Convert a QuizEntry domain entity into the MongoDB document format and persist it."""

    # Database JSON format:
    # {
    #   "quiz": {"confidence": 7, "motivation": 4, ...},
    #   "user_id": "...",
    #   "yesterday_goal": 1|0,
    #   "tomorrow": "...",
    #   "date": 1706668800
    # }

    quiz_dict = {
        "quiz": dict(quiz_data.quiz),
        "user_id": quiz_data.user_ID,
        "yesterday_goal": 1 if quiz_data.yesterday_goal else 0,
        "tomorrow": quiz_data.tomorrow,
        "date": quiz_data.date,
    }

    created_quiz = await quiz_crud.create_quiz_entry(quiz_dict)
    return created_quiz


async def save_journal(journal_data: JournalEntry) -> dict:
    """Convert a JournalEntry domain entity into the MongoDB document format and persist it."""

    # Database JSON format:
    # {
    #   "title": "...",
    #   "content": "...",
    #   "user_id": "...",
    #   "date": 1706668800
    # }

    journal_dict = {
        "title": getattr(journal_data, "title", None),
        "content": journal_data.content,
        "user_id": journal_data.user_ID,
        "date": journal_data.date,
    }

    created_journal = await journal_crud.create_journal(journal_dict)
    return created_journal
