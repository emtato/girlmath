import asyncio
from db.user_crud import create_user, get_user_by_id, update_user
from db.journal_crud import create_journal, get_journal_by_id, update_journal
from db.quiz_crud import create_quiz_entry, get_quiz_entry_by_id, update_quiz_entry


async def test_crud():
    print("Starting user CRUD test...")

    # --- CREATE ---
    user_data = {"name": "Emilia", "email": "emilia@example.com"}
    user = await create_user(user_data)
    print("Created user:", user)

    user_id = user["_id"]

    # --- READ ---
    fetched_user = await get_user_by_id(user_id)
    print("Fetched user:", fetched_user)

    # --- UPDATE ---
    updated_user = await update_user(user_id, {"email": "amanda.new@example.com"})
    print("Updated user:", updated_user)

    # --- DELETE ---
    #success = await delete_user(user_id)
    #print("Deleted user:", success)

    print("user CRUD test finished.")

    print("Starting journal CRUD test...")

    # --- CREATE ---
    journal_data = {"user_ID": user_id, "date": 67, "content": "BWAHHHHHseven"}
    journal = await create_journal(journal_data)
    print("Created journal:", journal)

    journal_id = journal["_id"]

    # --- READ ---
    fetched_journal = await get_journal_by_id(journal_id)
    print("Fetched journal:", fetched_journal)

    # --- UPDATE ---
    updated_journal = await update_journal(journal_id, {"content": "bleh"})
    print("Updated journal:", updated_journal)

    # --- DELETE ---
    # success = await delete_journal(journal_id)
    # print("Deleted journal:", success)

    print("journal CRUD test finished.")

    print("Starting quiz entry CRUD test...")

    # --- CREATE ---
    entry_data = {"user_ID": user_id, "date": 67, "content": "six seven"}
    entry = await create_quiz_entry(entry_data)
    print("Created entry:", entry)

    entry_id = entry["_id"]

    # --- READ ---
    fetched_entry = await get_quiz_entry_by_id(entry_id)
    print("Fetched entry:", fetched_entry)

    # --- UPDATE ---
    updated_entry = await update_quiz_entry(entry_id, {"content": "bleh"})
    print("Updated entry:", updated_entry)

    # --- DELETE ---
    # success = await delete_entry(entry_id)
    # print("Deleted entry:", success)

    print("entry CRUD test finished.")

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_crud())
