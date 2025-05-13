from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from services.database.check_db_health_service import health_check_service
from utils.auth import verify_token
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)

router = APIRouter(tags=["database"])


@router.get("/database/health")
async def health_check(
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> Dict[str, str]:
    """
    Check the health of the database connection.
    Returns a JSON object with the status of the connection.
    """
    try:
        result = await health_check_service()
        await log_action(
            username=user,
            action="Database health check",
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
