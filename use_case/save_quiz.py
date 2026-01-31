# Description:
# Created by Emilia on 2026-01-31
from entities.quiz import QuizEntry
from db import persist_data

async def save_quiz(data: dict):
    id = ""
    date = data["date"]
    user_id = data["user_ID"]
    quiz_values = data["quiz"]
    yesterday_goal = bool(data["yesterday_goal"])
    tomorrow = data["tomorrow"]

    await persist_data.save_quiz(QuizEntry(id, user_id, date, quiz_values, yesterday_goal, tomorrow))




