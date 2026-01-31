import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGODB_DB")

client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]

# collections
#  user specific:
users_collection = db["users"]
journals_collection = db["journals"]
topics_collection = db["topics"]
quiz_entries_collection = db["quiz"]
#  non-user specific
constellations_collection = db["constellations"]
