# Description:
# Created by Emilia on 2026-01-31
from entities.journal import JournalEntry
from ai.gemini import ai_keywords

def prompt_ai(data: JournalEntry):
   keyphrase =  ai_keywords(data.title + "\n"+ data.content)
