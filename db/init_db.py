from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

db_client: AsyncIOMotorClient = AsyncIOMotorClient()


async def connect_db():
    """Create database connection."""
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGO_DETAILS)


async def close_db():
    """Close database connection."""
    db_client.close()


async def get_collection_client(
        collection_name: str,
        database_name: str = settings.DATABASE_NAME) -> AsyncIOMotorCollection:
    global db_client
    """Return database client instance."""
    return db_client[database_name][collection_name]
