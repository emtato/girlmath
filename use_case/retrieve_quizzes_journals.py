# Description: retrieve every single journal and quiz in database. combines other functions:
# first uses retrieve journal and quiz list for id list, then individually retrieves each via id.
# Created by Emilia on 2026-01-31
from . import retrieve_journal_list
from . import retrieve_quiz_list

async def retrieve_all_quizzes_and_journals(user_ID: str):
    journal_list = await retrieve_journal_list.retrieve_journal_list(user_ID)
    quiz_list = await retrieve_quiz_list.retrieve_quiz_list(user_ID)
    return journal_list + quiz_list
