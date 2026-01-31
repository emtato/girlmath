# Description: Database index setup for optimal query performance
# Created on 2026-01-31

from db.database import (
    users_collection,
    journals_collection,
    stars_collection,
    quiz_entries_collection,
    constellations_collection
)


async def create_indexes():
    """
    Create all necessary indexes for the database collections.

    This should be run once during application initialization or deployment.
    Indexes improve query performance for common lookup patterns.
    """
    print("Creating database indexes...")

    # Users collection
    await users_collection.create_index("email", unique=True)
    print("✓ Users indexes created")

    # Journals collection
    await journals_collection.create_index("user_ID")
    await journals_collection.create_index([("user_ID", 1), ("date", -1)])
    await journals_collection.create_index([("user_ID", 1), ("star_IDs", 1)])  # Scoped to user
    print("✓ Journals indexes created")

    # Stars collection
    await stars_collection.create_index([("user_ID", 1), ("name", 1)], unique=True)
    await stars_collection.create_index([("user_ID", 1), ("constellation_ID", 1)])
    await stars_collection.create_index([("user_ID", 1), ("journal_IDs", 1)])  # Scoped to user
    print("✓ Stars indexes created")

    # Constellations collection (global)
    await constellations_collection.create_index("name", unique=True)  # "Mathematics", "Programming", etc.
    print("✓ Constellations indexes created")

    # Quiz collection
    await quiz_entries_collection.create_index("user_ID")
    await quiz_entries_collection.create_index([("user_ID", 1), ("date", -1)])
    print("✓ Quiz indexes created")

    print("All indexes created successfully!")


async def drop_all_indexes():
    """
    Drop all custom indexes (useful for testing or rebuilding).
    Note: This will not drop the default _id index.
    """
    print("Dropping all custom indexes...")

    await users_collection.drop_indexes()
    await journals_collection.drop_indexes()
    await stars_collection.drop_indexes()
    await constellations_collection.drop_indexes()
    await quiz_entries_collection.drop_indexes()

    print("All custom indexes dropped!")


if __name__ == "__main__":
    import asyncio

    async def main():
        await create_indexes()

    asyncio.run(main())
