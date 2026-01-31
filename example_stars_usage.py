"""
Example script demonstrating the Stars & Constellations system usage.

Run this to see how to:
1. Create constellations
2. Analyze a journal entry
3. Link stars to journals
4. Query the constellation map
"""

import asyncio
from db.setup_indexes import create_indexes
from db import star_crud, constellation_crud, journal_crud
from use_case.analyze_and_link_stars import (
    analyze_and_link_stars,
    get_constellation_map,
    expand_star_to_journals
)


async def example_usage():
    """Demonstrate the stars and constellations system."""

    print("=" * 60)
    print("Stars & Constellations System Example")
    print("=" * 60)

    # Setup: Create indexes (run once)
    print("\n1. Setting up database indexes...")
    await create_indexes()

    # Example user and test data
    user_id = "test_user_123"

    # Step 1: Create some global constellations
    print("\n2. Creating example constellations...")
    ml_const = await constellation_crud.create_constellation(
        name="Machine Learning",
        description="Topics related to ML and AI",
        is_global=True
    )
    web_const = await constellation_crud.create_constellation(
        name="Web Development",
        description="Web technologies and frameworks",
        is_global=True
    )
    print(f"   ✓ Created: {ml_const['name']}")
    print(f"   ✓ Created: {web_const['name']}")

    # Step 2: Create a journal entry
    print("\n3. Creating a journal entry...")
    journal_data = {
        "user_id": user_id,
        "date": 1738368000,  # Example timestamp
        "content": """Today I learned about neural networks and how backpropagation 
        works. I also built a simple web app using FastAPI and connected it to a 
        MongoDB database. The async/await patterns in Python made it really clean."""
    }
    journal = await journal_crud.create_journal(journal_data)
    print(f"   ✓ Created journal: {journal['_id']}")

    # Step 3: Analyze journal and link stars
    print("\n4. Analyzing journal entry and extracting topics...")
    result = await analyze_and_link_stars(
        user_id=user_id,
        journal_id=journal["_id"],
        journal_text=journal_data["content"]
    )

    if result["success"]:
        print(f"   ✓ Successfully linked {len(result['stars'])} stars")
        print(f"   ✓ Constellations: {', '.join(result['constellations'])}")
        for star in result["stars"]:
            print(f"     - {star['name']}")
    else:
        print(f"   ✗ Error: {result.get('error', 'Unknown error')}")

    # Step 4: View constellation map
    print("\n5. Viewing constellation map...")
    map_data = await get_constellation_map(user_id)

    print(f"\n   Total Constellations: {map_data['total_constellations']}")
    print(f"   Total Stars (Topics): {map_data['total_stars']}")

    for constellation in map_data["constellations"]:
        if constellation["star_count"] > 0:
            print(f"\n   📚 {constellation['constellation_name']}")
            print(f"      Stars: {constellation['star_count']}, "
                  f"Journals: {constellation['total_journals']}")
            for star in constellation["stars"][:5]:  # Show first 5
                print(f"        • {star['name']}: "
                      f"{star['journal_count']} journal(s)")

    # Step 5: Expand a star to see journals
    if result["success"] and result["stars"]:
        first_star = result["stars"][0]
        print(f"\n6. Expanding star '{first_star['name']}' to see journals...")

        expanded = await expand_star_to_journals(first_star["_id"])
        if expanded:
            print(f"   Found {expanded['journal_count']} journal(s):")
            for journal_entry in expanded["journals"]:
                preview = journal_entry["content"][:80].replace("\n", " ")
                print(f"     - {preview}...")

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(example_usage())
