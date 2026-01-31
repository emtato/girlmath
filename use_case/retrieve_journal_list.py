# Description: retrieves a list of journals with id title, date, short preview of first bit.
# Created by Emilia on 2026-01-31
from db.journal_crud import get_user_journals



async def retrieve_journal_list(user_ID: str):
    return await get_user_journals(user_ID)

