import asyncio
from crud import create_user, get_user_by_id, update_user, delete_user

async def test_crud():
    print("Starting CRUD test...")

    # --- CREATE ---
    user_data = {"name": "Amanda", "email": "amanda@example.com"}
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

    print("CRUD test finished.")

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_crud())
