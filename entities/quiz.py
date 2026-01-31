# Description:
# Created by Emilia on 2026-01-31

from typing import Dict

class QuizEntry:
    """
    Domain Entity for a single quiz check-in
    """

    def __init__(self, id: int, date: int, quiz: Dict[str, int], yesterday_goal: bool, tomorrow: str):
        self.id = id
        self.date = date              # unix timestamp
        self.quiz = quiz         # e.g. {"confidence": 7, "motivation": 4}
        self.yesterday_goal = yesterday_goal
        self.tomorrow = tomorrow

    def get_metric(self, name: str) -> int | None:
        return self.quiz.get(name)

    def average_score(self) -> float:
        if not self.quiz:
            return 0.0
        return sum(self.quiz.values()) / len(self.quiz)

    def __repr__(self):
        return f"QuizEntry(date={self.date}, values={self.quiz})"
