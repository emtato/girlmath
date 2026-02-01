from .database import users_collection
from bson import ObjectId

# helper to convert ObjectId to str
def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    return user

# CREATE

async def get_or_create_user(user_data: dict):
    email = user_data["email"]

    # 1. Try find existing user
    user = await users_collection.find_one({"email": email})
    if user:
        return serialize_user(user)

    # 2. Otherwise create new
    result = await users_collection.insert_one(user_data)
    user = await users_collection.find_one({"_id": result.inserted_id})
    return serialize_user(user)


async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    user = await users_collection.find_one({"_id": result.inserted_id})
    return serialize_user(user)

# READ
async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return serialize_user(user)
    return None

# UPDATE
async def update_user(user_id: str, update_data: dict):
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return serialize_user(user)
    return None

# DELETE
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
