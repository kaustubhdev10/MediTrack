import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv


class Database:
    """
    A singleton-like class to manage the MongoDB client and database instances.
    """
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """Returns the application's database instance."""
    load_dotenv()
    db.client = AsyncIOMotorClient(os.getenv("MONGO_URI"), maxPoolSize=10, minPoolSize=10)
    db.db = db.client.meditrack_db


async def close_mongo_connection():
    """Closes the MongoDB connection."""
    db.client.close()