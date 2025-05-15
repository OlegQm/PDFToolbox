from typing import List, Dict, Any, Tuple
import os
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

async def get_logs_service(
    user: str,
    history_collection: AsyncIOMotorCollection,
    skip: int,
    limit: int
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Fetches history logs from the database with pagination support.

    This service retrieves logs from the specified MongoDB collection, ensuring
    that only the admin user has access to the logs. The logs are sorted in
    descending order by timestamp.

    Args:
        user (str): The username of the requesting user.
        history_collection (AsyncIOMotorCollection): The MongoDB collection containing the history logs.
        skip (int): The number of logs to skip for pagination.
        limit (int): The maximum number of logs to retrieve.

    Returns:
        Tuple[List[Dict[str, Any]], int]: A tuple containing a list of logs and the total count of logs.

    Raises:
        HTTPException: If the admin user environment variable is not set (500).
        HTTPException: If the requesting user is not authorized (403).
    """
    admin_user = os.getenv("ADMIN_USER")
    if not admin_user:
        raise HTTPException(500, "Admin user not set")
    if user != admin_user:
        raise HTTPException(403, "Not authorized")

    total = await history_collection.count_documents({})

    cursor = history_collection.find({}, {"_id": 0}).sort("timestamp", -1)
    logs = await cursor.skip(skip).limit(limit).to_list(length=limit)
    return logs, total
