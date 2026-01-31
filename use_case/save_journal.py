# Description:
# Created by Emilia on 2026-01-31

from entities.journal import JournalEntry

def save_journal(data: dict):
    date = data["date"]
    text = data["content"]

    journal = JournalEntry(date, text)
    #Database.save(journal) @amande
