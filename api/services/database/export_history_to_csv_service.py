from io import StringIO
import csv
import os

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection

from services.database.get_history_logs_service import get_logs_service

async def logs_in_csv(
    user: str,
    history_collection: AsyncIOMotorCollection,
    skip: int,
    limit: int
) -> StreamingResponse:
    """
    Asynchronously generates a CSV file containing user logs and returns it as a streaming response.

    Args:
        user (str): The username of the requesting user.
        history_collection (AsyncIOMotorCollection): The MongoDB collection containing the logs.
        skip (int): The number of logs to skip for pagination.
        limit (int): The maximum number of logs to include in the response.

    Returns:
        StreamingResponse: A streaming response containing the CSV file with logs.

    Raises:
        HTTPException: If no logs are found (404).
        HTTPException: If the admin user environment variable is not set (500).
        HTTPException: If the requesting user is not authorized (403).
    """
    logs, _ = await get_logs_service(
        user, history_collection, skip, limit
    )
    if not logs:
        raise HTTPException(404, "No logs found")
    admin_user = os.getenv("ADMIN_USER")
    if not admin_user:
        raise HTTPException(500, "Admin user not set")
    if user != admin_user:
        raise HTTPException(403, "Not authorized")

    csv_file = StringIO()
    fieldnames = logs[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for log in logs:
        writer.writerow(log)

    csv_file.seek(0)
    return StreamingResponse(csv_file, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=logs.csv"
    })
