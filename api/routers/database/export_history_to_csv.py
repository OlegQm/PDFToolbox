from fastapi import APIRouter, Depends, Query, HTTPException, Request
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection

from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo
from utils.auth import verify_token
from services.database.export_history_to_csv_service import logs_in_csv

router = APIRouter(tags=["Database"])


@router.get(
    "/database/history-export-to-csv",
    summary="Export logs to CSV",
    description="""
Streams usage history logs as a CSV file.

- Requires a valid Bearer token in the `Authorization` header.
- Supports pagination via `skip` and `limit` query parameters.
- Returns a `text/csv` response with a downloadable filename.
- Records the export action along with the requester's city and country.
""",
    response_class=StreamingResponse
)
async def export_logs_to_csv(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> StreamingResponse:
    """
    Exports user logs to a CSV file.

    This endpoint allows a user to export their logs from the database in CSV format.
    The logs can be filtered using pagination parameters.

    Args:
        request (Request): The HTTP request object, used to retrieve client information.
        skip (int, optional): Number of records to skip. Defaults to 0. Must be greater than or equal to 0.
        limit (int, optional): Number of records to return. Defaults to 100. Must be between 1 and 1000.
        user (str): The username of the authenticated user, retrieved via token verification.
        history_collection (AsyncIOMotorCollection): The MongoDB collection containing the user's history logs.

    Returns:
        StreamingResponse: A streaming response containing the CSV file.

    Raises:
        HTTPException: If an HTTP-related error occurs.
        HTTPException: If an internal server error occurs.
    """
    try:
        csv_stream = await logs_in_csv(
            user=user,
            history_collection=history_collection,
            skip=skip,
            limit=limit
        )
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action="Exported logs to CSV",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return csv_stream
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
