# Description: CRUD operations for Constellations
# Created on 2026-01-31

from db.database import constellations_collection, stars_collection
from bson import ObjectId
from typing import List, Optional, Dict, Any
from datetime import datetime


def serialize_constellation(constellation) -> dict:
    """Convert MongoDB constellation document to JSON-serializable dict."""
    constellation["_id"] = str(constellation["_id"])
    return constellation


async def create_constellation(constellation_data: dict) -> dict:
    result = await constellations_collection.insert_one(constellation_data)
    constellation = await constellations_collection.find_one({"_id": result.inserted_id})
    return serialize_constellation(constellation)


async def get_constellation_by_id(constellation_id: str) -> Optional[dict]:
    """Get a constellation by its ID."""
    constellation = await constellations_collection.find_one({"_id": ObjectId(constellation_id)})
    return serialize_constellation(constellation) if constellation else None


async def get_constellation_with_stars(constellation_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Get a constellation with all its stars for a specific user."""
    try:
        constellation = await constellations_collection.find_one({"_id": ObjectId(constellation_id)})
        if not constellation:
            return None

        constellation["_id"] = str(constellation["_id"])

        # Get user's stars for this constellation
        cursor = stars_collection.find({
            "user_id": user_id,
            "constellation_id": constellation_id
        })

        stars = []
        async for star in cursor:
            star["_id"] = str(star["_id"])
            stars.append(star)

        constellation["stars"] = stars
        return constellation

    except Exception as e:
        print(f"Error getting constellation with stars: {e}")
        return None


async def get_all_constellations(user_id: Optional[str] = None, include_stars: bool = False) -> List[dict]:
    """Get all constellations, optionally with user's stars populated."""
    cursor = constellations_collection.find().sort("name", 1)
    constellations = []

    async for constellation in cursor:
        constellation["_id"] = str(constellation["_id"])

        if include_stars and user_id:
            # Get user's stars for this constellation
            stars_cursor = stars_collection.find({
                "user_id": user_id,
                "constellation_id": str(constellation["_id"])
            })

            stars = []
            async for star in stars_cursor:
                star["_id"] = str(star["_id"])
                stars.append(star)

            constellation["stars"] = stars

        constellations.append(constellation)

    return constellations


async def delete_constellation(constellation_id: str, reassign_stars_to: Optional[str] = None) -> bool:
    """Delete a constellation, optionally reassigning its stars to another constellation."""
    try:
        if reassign_stars_to:
            await stars_collection.update_many(
                {"constellation_id": constellation_id},
                {"$set": {"constellation_id": reassign_stars_to}}
            )

        result = await constellations_collection.delete_one({"_id": ObjectId(constellation_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting constellation: {e}")
        return False
