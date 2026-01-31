# Description:
# Created by Emilia on 2026-01-31


from entities.ai_data import AiInfo

def convert_ai(data: dict):
    """
    Converts raw request dict into AiInfo domain entity.
    """
    return AiInfo(
        content=data["content"],
        date = data["date"],
        context=data.get("context")
    )


def prompt_ai(data: AiInfo):
    return "meow"
