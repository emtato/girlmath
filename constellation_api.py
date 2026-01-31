import os
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

# -----------------------------
# Configuration / Environment
# -----------------------------
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "constellation_db")

app = FastAPI(title="Constellation Map API")

# We'll attach the Motor client and collections to app.state in startup

# -----------------------------
# Pydantic models
# -----------------------------

class JournalEntryIn(BaseModel):
    """Request model for submitting a journal entry."""
    text: str = Field(..., min_length=1, description="The journal entry text")


class JournalEntryOut(BaseModel):
    """Response model for a saved or returned journal entry."""
    text: str
    constellation: str
    topics: List[str]
    confidence: int = Field(..., ge=1, le=5)
    created_at: datetime


# -----------------------------
# Utility functions
# -----------------------------

def normalize_topic(name: str) -> str:
    """Normalize a topic name to a canonical form for storage and lookup.

    Normalization strategy:
    - strip surrounding whitespace
    - collapse internal whitespace to single spaces
    - lower-case
    - optionally additional normalization rules can be added
    """
    if not isinstance(name, str):
        name = str(name)
    # Strip and collapse spaces
    parts = name.strip().split()
    normalized = " ".join(parts).lower()
    return normalized


# -----------------------------
# AI placeholder (Gemini)
# -----------------------------

async def gemini_placeholder_analyze(text: str) -> Dict[str, Any]:
    """Placeholder async AI function simulating an external model (Gemini).

    This function should be replaced with a real async call to the AI provider.
    For now it returns a deterministic example result based on simple heuristics.
    """
    # Simple heuristic: if certain keywords appear, choose an example constellation/topics
    text_lower = text.lower()
    if "star" in text_lower or "nebula" in text_lower:
        constellation = "Orion"
        topics = ["Stars", "Nebula"]
        confidence = 4
    elif "planet" in text_lower or "orbit" in text_lower:
        constellation = "Solar"
        topics = ["Planets", "Orbits"]
        confidence = 4
    else:
        constellation = "General"
        topics = ["Observation", "Reflection"]
        confidence = 3

    # Simulate async latency
    await asyncio.sleep(0.01)

    return {
        "constellation": constellation,
        "topics": topics,
        "confidence": int(confidence),
    }


async def analyze_entry(text: str) -> Dict[str, Any]:
    """Analyze a journal entry text using the AI placeholder function.

    Returns a dictionary containing:
    - constellation: guessed constellation name (str)
    - topics: list of normalized topic strings
    - confidence: an integer 1-5

    This function also normalizes the returned topics.
    """
    ai_result = await gemini_placeholder_analyze(text)

    constellation = ai_result.get("constellation", "Unknown")
    raw_topics = ai_result.get("topics", [])
    confidence = int(ai_result.get("confidence", 3))

    # Normalize topics to canonical form while preserving display form in storage
    normalized_topics = [normalize_topic(t) for t in raw_topics]

    return {
        "constellation": constellation,
        "topics": normalized_topics,
        "confidence": confidence,
    }


# -----------------------------
# Database helpers
# -----------------------------

async def connect_db() -> None:
    """Create the Motor client, attach DB and collections to app.state, and ensure indexes.

    Uses environment variables MONGODB_URI and MONGODB_DB.
    """
    # Create client and attach
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[MONGODB_DB]
    app.state._mongo_client = client
    app.state.db = db
    # Collections
    app.state.constellations = db.get_collection("constellations")
    app.state.topics = db.get_collection("topics")
    app.state.journal_entries = db.get_collection("journal_entries")

    # Ensure indexes:
    # - topics.normalized_name should be unique so a topic name maps to one document
    # - constellations.name unique
    await app.state.topics.create_index("normalized_name", unique=True)
    await app.state.constellations.create_index("name", unique=True)


async def close_db() -> None:
    """Close the Motor client on shutdown to clean up resources."""
    client: AsyncIOMotorClient = getattr(app.state, "_mongo_client", None)
    if client:
        client.close()


async def upsert_topic(topic_name: str, constellation_name: str) -> Dict[str, Any]:
    """Upsert a topic document ensuring the topic belongs to exactly one constellation.

    If the topic already exists and is associated with a different constellation,
    this function raises HTTPException(409).

    Returns the topic document (freshly inserted or updated).
    """
    normalized = normalize_topic(topic_name)
    topics_coll = app.state.topics

    # Check if topic exists
    existing = await topics_coll.find_one({"normalized_name": normalized})
    if existing:
        existing_const = existing.get("constellation")
        if existing_const != constellation_name:
            # Topic belongs to a different constellation -> conflict
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Topic '{topic_name}' (normalized '{normalized}') already belongs to constellation '{existing_const}'."
                ),
            )
        # Otherwise update the updated_at timestamp and return
        await topics_coll.update_one(
            {"_id": existing["_id"]},
            {"$set": {"updated_at": datetime.now(timezone.utc)}},
        )
        return await topics_coll.find_one({"_id": existing["_id"]})

    # Insert new topic document. Handle possible race with DuplicateKeyError.
    doc = {
        "name": topic_name,
        "normalized_name": normalized,
        "constellation": constellation_name,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    try:
        result = await topics_coll.insert_one(doc)
        return await topics_coll.find_one({"_id": result.inserted_id})
    except DuplicateKeyError:
        # Another process created the topic concurrently. Fetch and verify.
        existing = await topics_coll.find_one({"normalized_name": normalized})
        if existing and existing.get("constellation") != constellation_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Topic '{topic_name}' already exists and belongs to constellation '{existing.get('constellation')}'."
                ),
            )
        return existing


# -----------------------------
# FastAPI event handlers
# -----------------------------

@app.on_event("startup")
async def on_startup() -> None:
    """FastAPI startup event: connect to MongoDB and create required indexes."""
    await connect_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """FastAPI shutdown event: close MongoDB connection."""
    await close_db()


# -----------------------------
# Endpoint implementations
# -----------------------------

@app.post("/journal", response_model=JournalEntryOut, status_code=status.HTTP_201_CREATED)
async def save_journal(entry_in: JournalEntryIn):
    """Accept a journal entry text, analyze it with AI, upsert topics, and save the journal entry.

    Steps:
    1. Call analyze_entry(text) -> returns constellation, topics (normalized), confidence
    2. For each topic returned: upsert topic document (ensuring one-constellation constraint)
    3. Ensure the constellation document exists (insert if needed)
    4. Insert a journal_entries document referencing the topics and return JournalEntryOut
    """
    # Analyze the entry using the AI analyzer
    analysis = await analyze_entry(entry_in.text)
    constellation = analysis["constellation"]
    topics_normalized = analysis["topics"]
    confidence = int(analysis.get("confidence", 3))

    # Upsert constellation doc (idempotent). We store minimal info for now.
    const_coll = app.state.constellations
    await const_coll.update_one(
        {"name": constellation},
        {"$setOnInsert": {"name": constellation, "created_at": datetime.now(timezone.utc)}},
        upsert=True,
    )

    # Upsert topics and collect canonical stored names
    stored_topics = []
    for t_norm in topics_normalized:
        # We will store the display name as the normalized one for now
        try:
            topic_doc = await upsert_topic(t_norm, constellation)
        except HTTPException:
            # Re-raise so client gets the conflict
            raise
        stored_topics.append(topic_doc["normalized_name"])

    # Build journal entry document and insert
    journal_coll = app.state.journal_entries
    journal_doc = {
        "text": entry_in.text,
        "constellation": constellation,
        "topics": stored_topics,  # list of normalized topic names
        "confidence": confidence,
        "created_at": datetime.now(timezone.utc),
    }
    result = await journal_coll.insert_one(journal_doc)
    saved = await journal_coll.find_one({"_id": result.inserted_id})

    # Prepare response
    response = JournalEntryOut(
        text=saved["text"],
        constellation=saved["constellation"],
        topics=saved["topics"],
        confidence=int(saved["confidence"]),
        created_at=saved["created_at"],
    )
    return response


@app.get("/constellations")
async def list_constellations() -> List[Dict[str, Any]]:
    """Return all constellations and their topics.

    Response format: list of objects { name: str, topics: [str, ...] }
    """
    const_coll = app.state.constellations
    topics_coll = app.state.topics

    # Fetch all constellations
    const_cursor = const_coll.find({})
    constellations = []
    async for c in const_cursor:
        name = c["name"]
        # Fetch topics belonging to this constellation
        t_cursor = topics_coll.find({"constellation": name})
        topic_names = []
        async for t in t_cursor:
            topic_names.append(t.get("normalized_name"))
        constellations.append({"name": name, "topics": topic_names})

    return constellations


@app.get("/topics/{topic_name}/entries")
async def entries_for_topic(topic_name: str) -> List[JournalEntryOut]:
    """Return all journal entries that reference the given topic name.

    The topic_name parameter is normalized before lookup. Returns a list of JournalEntryOut.
    """
    normalized = normalize_topic(topic_name)
    journal_coll = app.state.journal_entries

    cursor = journal_coll.find({"topics": normalized}).sort("created_at", -1)
    results: List[JournalEntryOut] = []
    async for doc in cursor:
        results.append(
            JournalEntryOut(
                text=doc["text"],
                constellation=doc["constellation"],
                topics=doc["topics"],
                confidence=int(doc.get("confidence", 3)),
                created_at=doc["created_at"],
            )
        )
    return results


# Optional small root
@app.get("/")
async def root() -> Dict[str, str]:
    """Basic root endpoint returning a small health info object."""
    return {"status": "ok", "db": MONGODB_DB}
