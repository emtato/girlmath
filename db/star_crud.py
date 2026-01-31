# Description: CRUD operations for Stars (topics)
# Created on 2026-01-31
from bson import ObjectId

from db.database import journals_collection, stars_collection
from typing import List, Optional
from datetime import datetime


# Helper to convert ObjectId to str
def serialize_star(star) -> dict:
    """Convert MongoDB star document to JSON-serializable dict."""
    star["_id"] = str(star["_id"])
    return star


# CREATE
async def create_star(star_data: dict) -> dict:
    result = await stars_collection.insert_one(star_data)
    star = await stars_collection.find_one({"_id": result.inserted_id})
    return serialize_star(star)


# READ
async def get_star_by_id(star_id: str) -> Optional[dict]:
    """Get a star by its ID."""
    star = await stars_collection.find_one({"_id": ObjectId(star_id)})
    return serialize_star(star) if star else None


async def get_star_by_name(user_id: str, name: str) -> Optional[dict]:
    """
    Find a star by user ID and normalized name.

    Args:
        user_id: The user who owns the star
        name: Normalized topic name

    Returns:
        Star document if found, None otherwise
    """
    star = await stars_collection.find_one({
        "user_id": user_id,
        "name": name
    })
    return serialize_star(star) if star else None


async def get_stars_by_constellation(user_id: str, constellation_id: str) -> List[dict]:
    """
    Get all stars belonging to a constellation for a specific user.

    Args:
        user_id: The user who owns the stars
        constellation_id: The constellation to filter by

    Returns:
        List of star documents
    """
    cursor = stars_collection.find({
        "user_id": user_id,
        "constellation_id": constellation_id
    })
    stars = []
    async for star in cursor:
        stars.append(serialize_star(star))
    return stars


async def get_all_user_stars(user_id: str) -> List[dict]:
    """Get all stars for a specific user."""
    cursor = stars_collection.find({"user_id": user_id})
    stars = []
    async for star in cursor:
        stars.append(serialize_star(star))
    return stars


async def get_journals_for_star(star_id: str) -> List[str]:
    """
    Get all journal IDs that reference this star.

    Args:
        star_id: The star's ID

    Returns:
        List of journal IDs
    """
    star = await stars_collection.find_one({"_id": ObjectId(star_id)})
    if star:
        return star.get("journal_ids", [])
    return []


# UPDATE
async def link_star_to_journal(star_id: str, journal_id: str) -> bool:
    """
    Create a bidirectional link between a star and a journal.

    This updates both the star's journal_ids array and the journal's star_ids array
    using atomic $addToSet operations.

    Args:
        star_id: The star's ID
        journal_id: The journal's ID

    Returns:
        True if successful, False otherwise
    """
    try:
        # Add journal_id to star's journal_ids array (if not already present)
        await stars_collection.update_one(
            {"_id": ObjectId(star_id)},
            {"$addToSet": {"journal_ids": journal_id}}
        )

        # Add star_id to journal's star_ids array (if not already present)
        await journals_collection.update_one(
            {"_id": ObjectId(journal_id)},
            {"$addToSet": {"star_ids": star_id}}
        )

        return True
    except Exception as e:
        print(f"Error linking star to journal: {e}")
        return False


async def unlink_star_from_journal(star_id: str, journal_id: str) -> bool:
    """
    Remove the bidirectional link between a star and a journal.

    Args:
        star_id: The star's ID
        journal_id: The journal's ID

    Returns:
        True if successful, False otherwise
    """
    try:
        # Remove journal_id from star's journal_ids array
        await stars_collection.update_one(
            {"_id": ObjectId(star_id)},
            {"$pull": {"journal_ids": journal_id}}
        )

        # Remove star_id from journal's star_ids array
        await journals_collection.update_one(
            {"_id": ObjectId(journal_id)},
            {"$pull": {"star_ids": star_id}}
        )

        return True
    except Exception as e:
        print(f"Error unlinking star from journal: {e}")
        return False


async def update_star_constellation(star_id: str, new_constellation_id: str) -> Optional[dict]:
    """
    Move a star to a different constellation.

    Args:
        star_id: The star's ID
        new_constellation_id: The new constellation ID

    Returns:
        Updated star document if successful, None otherwise
    """
    result = await stars_collection.update_one(
        {"_id": ObjectId(star_id)},
        {"$set": {"constellation_id": new_constellation_id}}
    )

    if result.modified_count > 0:
        star = await stars_collection.find_one({"_id": ObjectId(star_id)})
        return serialize_star(star)
    return None


# DELETE
async def delete_star(star_id: str) -> bool:
    """
    Delete a star and remove all references from journals.

    Args:
        star_id: The star's ID

    Returns:
        True if deleted, False otherwise
    """
    try:
        # First remove this star_id from all journals that reference it
        await journals_collection.update_many(
            {"star_ids": star_id},
            {"$pull": {"star_ids": star_id}}
        )

        # Then delete the star document
        result = await stars_collection.delete_one({"_id": ObjectId(star_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting star: {e}")
        return False
