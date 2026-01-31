import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGODB_DB")

client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]

# Example collections
users_collection = db["users"]
journals_collection = db["journals"]
checkins_collection = db["checkins"]
