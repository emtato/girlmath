from db.setup_indexes import create_indexes
from db.user_crud import create_user
from db.journal_crud import create_journal, get_journal_by_id, add_stars_to_journal, get_journals_by_star, get_journal_stars
from db.constellation_crud import create_constellation, get_constellation_by_id, get_constellation_with_stars, get_all_constellations, delete_constellation
from db.star_crud import (
    create_star, get_star_by_id, get_star_by_name, get_stars_by_constellation,
    get_all_user_stars, get_journals_for_star, link_star_to_journal,
    unlink_star_from_journal, update_star_constellation, delete_star
)


async def test_stars_and_constellations():
    print("Starting Stars & Constellations Test Suite")

    # Setup: Create a test user with unique email
    import time
    timestamp = int(time.time())
    print("\n[SETUP] Creating test user...")
    user_data = {"name": "Test User", "email": f"test{timestamp}@example.com"}
    user = await create_user(user_data)
    user_id = user["_id"]
    print(f"✓ Created user: {user_id}")

    # ========================================
    # CONSTELLATION CRUD TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("CONSTELLATION CRUD TESTS")
    print("=" * 60)

    # --- CREATE CONSTELLATIONS ---
    print("\n[TEST] Creating constellations...")
    math_const = await create_constellation({"name": f"Mathematics{timestamp}"})
    print(f"✓ Created constellation: {math_const['name']} (ID: {math_const['_id']})")

    programming_const = await create_constellation({"name": f"Programming{timestamp}"})
    print(f"✓ Created constellation: {programming_const['name']} (ID: {programming_const['_id']})")

    science_const = await create_constellation({"name": f"Science{timestamp}"})
    print(f"✓ Created constellation: {science_const['name']} (ID: {science_const['_id']})")

    math_const_id = math_const["_id"]

    # --- READ CONSTELLATION ---
    print("\n[TEST] Reading constellation by ID...")
    fetched_const = await get_constellation_by_id(math_const_id)
    print(f"✓ Fetched constellation: {fetched_const['name']}")
    assert fetched_const["name"] == f"Mathematics{timestamp}", "Constellation name mismatch"

    # --- GET ALL CONSTELLATIONS ---
    print("\n[TEST] Getting all constellations...")
    all_consts = await get_all_constellations()
    print(f"✓ Found {len(all_consts)} constellations")
    assert len(all_consts) >= 3, "Should have at least 3 constellations"

    # ========================================
    # STAR CRUD TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("STAR CRUD TESTS")
    print("=" * 60)

    # --- CREATE STARS ---
    print("\n[TEST] Creating stars...")
    calculus_star = await create_star({"user_ID":user_id, "name":"calculus", "constellation_id":math_const_id})
    print(f"✓ Created star: {calculus_star['name']} (ID: {calculus_star['_id']})")
    calculus_star_id = calculus_star["_id"]

    # --- READ STAR BY ID ---
    print("\n[TEST] Reading star by ID...")
    fetched_star = await get_star_by_id(calculus_star_id)
    print(f"✓ Fetched star: {fetched_star['name']}")
    assert fetched_star["name"] == "calculus", "Star name should be normalized to lowercase"

    # --- READ STAR BY NAME ---
    print("\n[TEST] Reading star by name...")
    found_star = await get_star_by_name(user_id, "calculus")
    print(f"✓ Found star by name: {found_star['name']}")
    assert found_star["_id"] == calculus_star_id, "Should find same star regardless of case"

    # --- GET STARS BY CONSTELLATION ---
    print("\n[TEST] Getting stars by constellation...")
    math_stars = await get_stars_by_constellation(user_id, math_const_id)
    print(f"✓ Found {len(math_stars)} stars in Mathematics constellation")
    assert len(math_stars) == 1, "Should have 1 math star (calculus)"

    # --- GET ALL USER STARS ---
    print("\n[TEST] Getting all user stars...")
    all_user_stars = await get_all_user_stars(user_id)
    print(f"✓ User has {len(all_user_stars)} total stars")
    assert len(all_user_stars) == 1, "User should have 1 star total"

    # ========================================
    # JOURNAL CREATION FOR LINKING TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("JOURNAL CREATION")
    print("=" * 60)

    print("\n[TEST] Creating test journals...")
    journal1_data = {"user_ID": user_id, "date": 1738368000, "content": "Today I studied calculus derivatives"}
    journal1 = await create_journal(journal1_data)
    journal1_id = journal1["_id"]
    print(f"✓ Created journal 1: {journal1_id}")

    journal2_data = {"user_ID": user_id, "date": 1738368100, "content": "Working on Python programming"}
    journal2 = await create_journal(journal2_data)
    journal2_id = journal2["_id"]
    print(f"✓ Created journal 2: {journal2_id}")

    journal3_data = {"user_ID": user_id, "date": 1738368200, "content": "Algebra and calculus review"}
    journal3 = await create_journal(journal3_data)
    journal3_id = journal3["_id"]
    print(f"✓ Created journal 3: {journal3_id}")

    # ========================================
    # STAR-JOURNAL LINKING TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("STAR-JOURNAL LINKING TESTS")
    print("=" * 60)

    # --- LINK STAR TO JOURNAL ---
    print("\n[TEST] Linking stars to journals...")
    success = await link_star_to_journal(calculus_star_id, journal1_id)
    print(f"✓ Linked calculus star to journal 1: {success}")
    assert success, "Link should succeed"

    # Link multiple stars to one journal
    success = await link_star_to_journal(calculus_star_id, journal3_id)
    print(f"✓ Linked calculus star to journal 3: {success}")


    # --- GET JOURNALS FOR STAR ---
    print("\n[TEST] Getting journals for a star...")
    calculus_journals = await get_journals_for_star(calculus_star_id)
    print(f"✓ Calculus star is linked to {len(calculus_journals)} journals")
    assert len(calculus_journals) == 2, "Calculus should be linked to 2 journals (journal1, journal3)"


    # --- GET STARS FOR JOURNAL ---
    print("\n[TEST] Getting stars for a journal...")
    journal3_stars = await get_journal_stars(journal3_id)
    print(f"✓ Journal 3 has {len(journal3_stars)} stars linked")
    assert len(journal3_stars) == 1, "Journal 3 should have 1 stars (calculus)"

    # --- GET JOURNALS BY STAR (via journal_crud) ---
    print("\n[TEST] Getting journals by star...")
    journals_with_calculus = await get_journals_by_star(calculus_star_id)
    print(f"✓ Found {len(journals_with_calculus)} journals containing calculus star")
    assert len(journals_with_calculus) == 2, "Should find 2 journals"

    # ========================================
    # CONSTELLATION WITH STARS
    # ========================================
    print("\n" + "=" * 60)
    print("CONSTELLATION WITH STARS TESTS")
    print("=" * 60)

    print("\n[TEST] Getting constellation with stars...")
    math_with_stars = await get_constellation_with_stars(math_const_id, user_id)
    print(f"✓ Mathematics constellation has {len(math_with_stars['stars'])} stars")
    assert len(math_with_stars["stars"]) == 1, "Should have 1 math stars"
    for star in math_with_stars["stars"]:
        print(f"  - {star['name']}: {len(star['journal_ids'])} journal(s)")

    # --- GET ALL CONSTELLATIONS WITH STARS ---
    print("\n[TEST] Getting all constellations with stars...")
    all_with_stars = await get_all_constellations(user_id, include_stars=True)
    print(f"✓ Retrieved {len(all_with_stars)} constellations with stars")
    for const in all_with_stars:
        print(f"  - {const['name']}: {len(const.get('stars', []))} stars")

    # ========================================
    # STAR UPDATE TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("STAR UPDATE TESTS")
    print("=" * 60)

    # ========================================
    # UNLINK TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("UNLINK TESTS")
    print("=" * 60)

    print("\n[TEST] Unlinking star from journal...")
    success = await unlink_star_from_journal(calculus_star_id, journal1_id)
    print(f"✓ Unlinked calculus from journal 1: {success}")

    calculus_journals_after = await get_journals_for_star(calculus_star_id)
    print(f"✓ Calculus now linked to {len(calculus_journals_after)} journals")
    assert len(calculus_journals_after) == 1, "Should have 1 journal after unlinking"

    # ========================================
    # DELETE TESTS
    # ========================================
    print("\n" + "=" * 60)
    print("DELETE TESTS")
    print("=" * 60)

    # --- DELETE STAR ---
    print("\n[TEST] Deleting a star...")
    deleted = await delete_star(calculus_star["_id"])
    print(f"✓ Deleted calc star: {deleted}")
    assert deleted, "Delete should succeed"

    # Verify it's removed from constellation
    math_stars_final = await get_stars_by_constellation(user_id, math_const_id)
    print(f"✓ Mathematics now has {len(math_stars_final)} stars (after deletion)")

    # Verify it's removed from journals
    journal3_stars_after = await get_journal_stars(journal3_id)
    print(f"✓ Journal 3 now has {len(journal3_stars_after)} stars (calculus removed)")
    assert calculus_star["_id"] not in journal3_stars_after, "calc should be removed from journal"

    # --- DELETE CONSTELLATION ---
    print("\n[TEST] Deleting a constellation...")
    deleted_const = await delete_constellation(math_const_id)
    print(f"✓ Deleted math constellation: {deleted_const}")
    assert deleted_const, "Delete should succeed"

    all_consts_final = await get_all_constellations()
    print(f"✓ Now have {len(all_consts_final)} constellations")

    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("\n✅ All tests passed successfully!")
    print("\nFinal state:")

    all_user_stars_final = await get_all_user_stars(user_id)
    print(f"  - User has {len(all_user_stars_final)} stars")

    all_consts_summary = await get_all_constellations(user_id, include_stars=True)
    print(f"  - {len(all_consts_summary)} constellations:")
    for const in all_consts_summary:
        print(f"    • {const['name']}: {len(const.get('stars', []))} stars")

    print("\n" + "=" * 60)


# Run the async test
if __name__ == "__main__":
    import asyncio

    async def main():
        await create_indexes()
        await test_stars_and_constellations()

    asyncio.run(main())
