from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorCollection
from utils.auth import verify_token
from services.database.get_history_logs_service import get_logs_service
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)

router = APIRouter(tags=["database"])

@router.get(
    "/database/get-history-logs",
    response_model=Dict[str, Any],
    summary="Get paginated history logs",
    description="Retrieve paginated history logs from the database."
)
async def get_logs(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip"
    ),
    limit: int = Query(
        50,
        ge=1,
        le=200,
        description="Max number of records to return"
    ),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> Dict[str, Any]:
    """
    Endpoint to retrieve paginated history logs.

    This endpoint allows users to fetch a paginated list of history logs from the database.
    The number of records to skip and the maximum number of records to return can be specified
    using query parameters.

    Args:
        skip (int): Number of records to skip. Must be greater than or equal to 0. Default is 0.
        limit (int): Maximum number of records to return. Must be between 1 and 200. Default is 50.
        user (str): The authenticated user, extracted from the token.
        history_collection (AsyncIOMotorCollection): The MongoDB collection for history logs.

    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - "total" (int): Total number of logs available.
            - "skip" (int): Number of records skipped.
            - "limit" (int): Maximum number of records returned.
            - "logs" (List[Dict[str, Any]]): List of history log entries.

    Raises:
        HTTPException: If an HTTP error occurs (e.g., authentication failure or internal error).
    """
    try:
        logs, total = await get_logs_service(
            user,
            history_collection,
            skip,
            limit
        )
        await log_action(user, "Got history logs", history_collection)
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "logs": logs
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
