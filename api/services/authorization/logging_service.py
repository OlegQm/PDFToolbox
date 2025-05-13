import logging
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorCollection
from utils.database import mongo_db

logger = logging.getLogger(__name__)

async def get_history_collection() -> AsyncIOMotorCollection:
    """
    Returns the 'usage_history' collection, creating it with
    an index on (username ASC, timestamp DESC) if needed.
    """
    return await mongo_db.get_or_create_collection(
        "usage_history",
        index_fields=[("username", 1), ("timestamp", -1)],
        unique=False
    )

async def log_action(
    username: str,
    action: str,
    history_collection: AsyncIOMotorCollection
) -> None:
    """
    Insert a usage action document into the history collection.
    """
    doc = {
        "username": username,
        "action": action,
        "timestamp": datetime.now(timezone.utc)
    }
    result = await history_collection.insert_one(doc)
    if result.acknowledged:
        logger.info("Logged action '%s' for user '%s'", action, username)
    else:
        logger.error("Failed to log action '%s' for user '%s'", action, username)
        raise RuntimeError("Failed to log action in DB")
