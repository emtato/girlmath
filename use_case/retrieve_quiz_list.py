# Description: retrieves a list of quizzes's date info.
# Created by Emilia on 2026-01-31
from db.quiz_crud import get_user_quiz_entries


def retrieve_quiz_list(user_ID: str):
    return(get_user_quiz_entries(user_ID))
