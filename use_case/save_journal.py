# Description:
# Created by Emilia on 2026-01-31
from db import persist_data
from entities.journal import JournalEntry

def save_journal(data: dict):
    date = data["date"]
    user_id = data["user_ID"]
    text = data["content"]
    id = ""
    persist_data.save_journal(JournalEntry(id, user_id, date, text))

