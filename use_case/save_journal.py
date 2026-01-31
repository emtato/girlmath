# Description:
# Created by Emilia on 2026-01-31
from db import persist_data
from entities.journal import JournalEntry

async def save_journal(data: dict):
    date = data["date"]
    title = data["title"]
    user_id = data["user_ID"]
    text = data["content"]
    id = ""
    return await persist_data.save_journal(JournalEntry(id, title, user_id, date, text))

