# Description:
# Created by Emilia on 2026-01-31
from db import persist_data
from entities.journal import JournalEntry
from use_case.ai_retrieve_keywords_journal_entry import prompt_ai


async def save_journal(data: dict):
    date = data["date"]
    title = data["title"]
    user_id = data["user_ID"]
    text = data["content"]
    id = ""
    #prompt_ai(JournalEntry(id, title, user_id, date, text))
    return await persist_data.save_journal(JournalEntry(id, title, user_id, date, text))

