# Description:
# Created by Emilia on 2026-01-31
from ai.gemini import get_response
from entities.ai_data import AiInfo


def convert_ai(data: dict):
    """
    Converts raw request dict into AiInfo domain entity.
    """
    return AiInfo(data["content"], data["date"], data["read_journal"], data["create_quiz"])


def prompt_ai(data: AiInfo):
    return get_response(data)
