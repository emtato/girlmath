import asyncio
from use_case.save_journal import save_journal

test_dict = {
    "title": "migu",
    "content": "hello journal!",
    "date": 1706668800,
    "user_ID": "1adsa2aaf3",
}

async def main():
    result = await save_journal(test_dict)
    print(result)

asyncio.run(main())
