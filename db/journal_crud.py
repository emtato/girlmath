from database import journals_collection
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


# STAR RELATIONSHIPS
async def add_stars_to_journal(journal_id: str, star_ids: list) -> dict:
    """
    Add multiple star IDs to a journal's star_ids array.
    Uses $addToSet to avoid duplicates.
    """
    await journals_collection.update_one(
        {"_id": ObjectId(journal_id)},
        {"$addToSet": {"star_ids": {"$each": star_ids}}}
    )
    journal = await journals_collection.find_one({"_id": ObjectId(journal_id)})
    return serialize_journal(journal) if journal else None


async def get_journals_by_star(star_id: str):
    """
    Get all journals that reference a specific star.
    """
    cursor = journals_collection.find({"star_ids": star_id})
    journals = []
    async for journal in cursor:
        journals.append(serialize_journal(journal))
    return journals


async def get_journal_stars(journal_id: str):
    """
    Get the list of star IDs associated with a journal.
    """
    journal = await journals_collection.find_one({"_id": ObjectId(journal_id)})
    if journal:
        return journal.get("star_ids", [])
    return []
