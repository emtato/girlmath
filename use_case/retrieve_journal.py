# Description: retrieve specific journal full info by id
# Created by Emilia on 2026-01-31
from typing import Optional

from db.journal_crud import get_journal_by_id


async def retrieve_journal_by_id(journal_id: str) -> dict:
      return await get_journal_by_id(journal_id)
