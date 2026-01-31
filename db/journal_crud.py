from .database import journals_collection
from bson import ObjectId

# helper to convert ObjectId to str
def serialize_journal(journal) -> dict:
    journal["_id"] = str(journal["_id"])
    return journal

# CREATE
async def create_journal(journal_data: dict):
    result = await journals_collection.insert_one(journal_data)
    journal = await journals_collection.find_one({"_id": result.inserted_id})
    return serialize_journal(journal)

# READ
async def get_journal_by_id(journal_id: str):
    journal = await journals_collection.find_one({"_id": ObjectId(journal_id)})
    if journal:
        return serialize_journal(journal)
    return None

# UPDATE
async def update_journal(journal_id: str, update_data: dict):
    await journals_collection.update_one({"_id": ObjectId(journal_id)}, {"$set": update_data})
    journal = await journals_collection.find_one({"_id": ObjectId(journal_id)})
    if journal:
        return serialize_journal(journal)
    return None

# DELETE
async def delete_journal(journal_id: str):
    result = await journals_collection.delete_one({"_id": ObjectId(journal_id)})
    return result.deleted_count > 0
