# Description:
# Created by Emilia on 2026-01-31
from entities.quiz import QuizEntry


def save_quiz(data: dict):
    date = data["date"]
    quiz_values = data["quiz"]
    yesterday_goal = bool(data["yesterday_goal"])
    tomorrow = data["tomorrow"]

    quiz = QuizEntry(date, quiz_values, yesterday_goal, tomorrow)
    #Database.save(quiz) @amande
