import asyncio
from use_case.save_journal import save_journal
from use_case.save_quiz import save_quiz

test_dict = {
    "title": "migu",
    "content": "hello journal!",
    "date": 1706668800,
    "user_ID": "1adsa2aaf3",
}

async def main():
    result = await save_journal(test_dict)
    print(result)

    questionnaire_dict = {
        "quiz": {"question1": 6, "question2": 7},
        "date": 1706668800,
        "user_ID": "1adsa2aaf3",
        "yesterday_goal": 1,
        "tomorrow": "hi",
    }

    questionnaire_result = await save_quiz(questionnaire_dict)
    print(questionnaire_result)

asyncio.run(main())


