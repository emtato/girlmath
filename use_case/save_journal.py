# Description:
# Created by Emilia on 2026-01-31

from entities.journal import JournalEntry

def save_journal(data: dict):
    date = data["date"]
    text = data["content"]
    id = 0
    journal = JournalEntry(id, date, text)
    #Database.save(journal) @amande
