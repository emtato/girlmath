# Description: retrieves individual quiz result from id
# Created by Emilia on 2026-01-31


from typing import Optional

from db.quiz_crud import get_quiz_entry_by_id
from entities.quiz import QuizEntry


async def retrieve_quiz_by_id(quiz_id: str) -> Optional[dict]:
    return await get_quiz_entry_by_id(quiz_id)



