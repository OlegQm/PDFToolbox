from fastapi import APIRouter, Depends, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.shemas import ClearCollectionResponse
from utils.auth import verify_token
from services.database.clear_history_collection_service import (
    clear_collection
)
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["Database"])


@router.delete(
    "/database/clear-history",
    response_model=ClearCollectionResponse,
    summary="Clear usage history",
    description="""
Permanently removes all documents from the `usage_history` collection in MongoDB.

- Requires a valid Bearer token in the `Authorization` header.
- Logs the action with username, city, and country information.
- Returns a status code and message upon successful completion.
"""
)
async def clear_mongo_collection(
    request: Request,
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> ClearCollectionResponse:
    """
    Clears the usage_history collection in MongoDB.

    Returns:
        ClearCollectionResponse: A status and a message indicating success.
    """
    try:
        result = await clear_collection(user=user, collection=history_collection)
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action="Clear history collection",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
