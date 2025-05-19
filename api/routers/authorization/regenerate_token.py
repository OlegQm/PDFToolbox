from typing import Dict, Any
from fastapi import APIRouter, Depends, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo
from utils.auth import verify_token
from services.authorization.regenerate_token_service import (
    regenerate_user_token_service
)

router = APIRouter(tags=["Authorization"])


@router.get(
    "/authorization/regenerate-token",
    summary="Regenerate user token",
    description="Regenerate user token if previous token was set."
)
async def register(
    request: Request,
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> Dict[str, Any]:
    """
    Endpoint to regenerate a user's token.

    This endpoint allows an authenticated user to regenerate their token if a previous token was set.
    It also logs the action along with the user's geolocation information.

    Args:
        request (Request): The incoming HTTP request object.
        user (str): The username of the authenticated user, obtained via token verification.
        history_collection (AsyncIOMotorCollection): The MongoDB collection for logging user actions.

    Returns:
        Dict[str, Any]: The result of the token regeneration process.

    Raises:
        HTTPException: If an error occurs during token regeneration or logging.
    """
    try:
        result = regenerate_user_token_service(user)
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action="Regenerate user token",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
