from .database import quiz_entries_collection
from bson import ObjectId

# helper to convert ObjectId to str
def serialize_quiz_entry(entry) -> dict:
    entry["_id"] = str(entry["_id"])
    return entry

# CREATE
async def create_quiz_entry(entry_data: dict):
    result = await quiz_entries_collection.insert_one(entry_data)
    entry = await quiz_entries_collection.find_one({"_id": result.inserted_id})
    return serialize_quiz_entry(entry)

# READ
async def get_quiz_entry_by_id(entry_id: str):
    entry = await quiz_entries_collection.find_one({"_id": ObjectId(entry_id)})
    if entry:
        return serialize_quiz_entry(entry)
    return None

# UPDATE
async def update_quiz_entry(entry_id: str, update_data: dict):
    await quiz_entries_collection.update_one({"_id": ObjectId(entry_id)}, {"$set": update_data})
    entry = await quiz_entries_collection.find_one({"_id": ObjectId(entry_id)})
    if entry:
        return serialize_quiz_entry(entry)
    return None

# DELETE
async def delete_quiz_entry(entry_id: str):
    result = await quiz_entries_collection.delete_one({"_id": ObjectId(entry_id)})
    return result.deleted_count > 0

async def get_user_quiz_entries(user_ID: str):
    """Get all quiz entries for a specific user."""
    cursor = quiz_entries_collection.find({"user_ID": user_ID}).sort("date", -1)
    quiz_entries = []
    async for entry in cursor:
        quiz_entries.append(serialize_quiz_entry(entry))
    return quiz_entries
