import os

from fastapi import status, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.shemas import ClearCollectionResponse

async def clear_collection(
    user: str,
    collection: AsyncIOMotorCollection
) -> ClearCollectionResponse:
    """
    This function is intended to be used by an admin user to clear the contents
    of a MongoDB collection. It verifies the user's identity against the 
    `ADMIN_USER` environment variable before proceeding with the deletion.

    user (str): The username of the user attempting to clear the collection.

    HTTPException: If the `ADMIN_USER` environment variable is not set (500) or 
                    if the user is not authorized (403).
    """
    admin_user = os.getenv("ADMIN_USER")
    if not admin_user:
        raise HTTPException(500, "Admin user not set")
    if user != admin_user:
        raise HTTPException(403, "Not authorized")
    result = await collection.delete_many({})
    return ClearCollectionResponse(
        status=status.HTTP_200_OK,
        message=f"Deleted {result.deleted_count} records from history."
    )
