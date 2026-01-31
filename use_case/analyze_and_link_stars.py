# Description: Use case for analyzing journal entries and linking stars (topics)
# Created on 2026-01-31

from typing import Dict, Any, Optional
from db import star_crud, constellation_crud, journal_crud
from ai.gemini import analyze_text_for_topics


async def analyze_and_link_stars(
    user_id: str,
    journal_id: str,
    journal_text: str
) -> Dict[str, Any]:
    """
    Analyze a journal entry to extract topics (stars), link them to the journal,
    and organize them into constellations.

    Flow:
    1. Call AI (Gemini) to extract topics from journal text
    2. For each extracted topic:
       - Determine which constellation it belongs to
       - Create or find existing star with that topic name
       - Link the star to the journal (bidirectional)
    3. Return summary of linked stars and constellations

    Args:
        user_id: The user who wrote the journal
        journal_id: The journal entry ID
        journal_text: The journal entry text content

    Returns:
        Dictionary with:
        - stars: List of linked star documents
        - constellations: Set of constellation names
        - success: Boolean
    """
    try:
        # Step 1: Extract topics using AI
        # This should return: {topics: [{name: str, constellation: str, confidence: int}]}
        ai_result = await analyze_text_for_topics(journal_text)
        extracted_topics = ai_result.get("topics", [])

        if not extracted_topics:
            return {
                "stars": [],
                "constellations": set(),
                "success": True,
                "message": "No topics extracted from journal"
            }

        linked_stars = []
        constellation_names = set()

        # Step 2: Process each extracted topic
        for topic_data in extracted_topics:
            topic_name = topic_data.get("name", "").strip()
            constellation_name = topic_data.get("constellation", "General")

            if not topic_name:
                continue

            # Get or create constellation
            constellation = await constellation_crud.create_constellation(
                name=constellation_name,
                description=f"Auto-generated constellation for {constellation_name} topics",
                is_global=True
            )
            constellation_id = constellation["_id"]
            constellation_names.add(constellation_name)

            # Get or create star for this topic
            existing_star = await star_crud.get_star_by_name(user_id, topic_name)

            if existing_star:
                star_id = existing_star["_id"]

                # Check if star belongs to different constellation
                if existing_star.get("constellation_id") != constellation_id:
                    # Update star's constellation if confidence is high enough
                    confidence = topic_data.get("confidence", 3)
                    if confidence >= 4:  # Only update if we're very confident
                        await star_crud.update_star_constellation(star_id, constellation_id)
            else:
                # Create new star
                star = await star_crud.create_star(
                    user_id=user_id,
                    name=topic_name,
                    constellation_id=constellation_id
                )
                star_id = star["_id"]

            # Link star to journal (bidirectional)
            await star_crud.link_star_to_journal(star_id, journal_id)

            # Fetch updated star
            star = await star_crud.get_star_by_id(star_id)
            linked_stars.append(star)

        return {
            "stars": linked_stars,
            "constellations": list(constellation_names),
            "success": True,
            "message": f"Linked {len(linked_stars)} stars to journal"
        }

    except Exception as e:
        print(f"Error in analyze_and_link_stars: {e}")
        return {
            "stars": [],
            "constellations": [],
            "success": False,
            "error": str(e)
        }


async def get_journal_with_stars(journal_id: str) -> Dict[str, Any]:
    """
    Get a journal entry with all its linked stars populated.

    Args:
        journal_id: The journal entry ID

    Returns:
        Dictionary with journal data and stars array
    """
    journal = await journal_crud.get_journal_by_id(journal_id)
    if not journal:
        return None

    star_ids = journal.get("star_ids", [])
    stars = []

    for star_id in star_ids:
        star = await star_crud.get_star_by_id(star_id)
        if star:
            stars.append(star)

    journal["stars"] = stars
    return journal


async def get_constellation_map(user_ID: str) -> Dict[str, Any]:
    """
    Get the complete constellation map for a user showing all constellations,
    their stars, and the count of journals for each star.

    This provides a hierarchical view:
    Constellation -> Stars -> Journal Count

    Args:
        user_ID: The user ID

    Returns:
        Dictionary with constellation hierarchy
    """
    constellations = await constellation_crud.get_all_constellations(
        user_ID=user_ID,
        include_stars=True
    )

    # Enhance with statistics
    map_data = []
    for constellation in constellations:
        stars = constellation.get("stars", [])

        # Add journal counts to stars
        for star in stars:
            star["journal_count"] = len(star.get("journal_ids", []))

        # Sort stars by journal count (descending)
        stars.sort(key=lambda s: s["journal_count"], reverse=True)

        map_data.append({
            "constellation_id": constellation["_id"],
            "constellation_name": constellation["name"],
            "description": constellation.get("description", ""),
            "star_count": len(stars),
            "total_journals": sum(s["journal_count"] for s in stars),
            "stars": stars
        })

    # Sort constellations by total journals (descending)
    map_data.sort(key=lambda c: c["total_journals"], reverse=True)

    return {
        "user_ID": user_ID,
        "total_constellations": len(map_data),
        "total_stars": sum(c["star_count"] for c in map_data),
        "constellations": map_data
    }


async def expand_star_to_journals(star_id: str) -> Dict[str, Any]:
    """
    Get all journals associated with a specific star (topic).

    Args:
        star_id: The star ID

    Returns:
        Dictionary with star info and all linked journals
    """
    star = await star_crud.get_star_by_id(star_id)
    if not star:
        return None

    journal_ids = star.get("journal_ids", [])
    journals = []

    for journal_id in journal_ids:
        journal = await journal_crud.get_journal_by_id(journal_id)
        if journal:
            journals.append(journal)

    # Sort journals by date (most recent first)
    journals.sort(key=lambda j: j.get("date", 0), reverse=True)

    return {
        "star_id": star_id,
        "star_name": star["name"],
        "constellation_id": star["constellation_id"],
        "journal_count": len(journals),
        "journals": journals
    }
