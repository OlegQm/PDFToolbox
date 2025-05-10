from typing import Dict
from fastapi import APIRouter, HTTPException
from services.database.check_db_health_service import health_check_service

router = APIRouter(tags=["database"])


@router.get("/database/health")
async def health_check() -> Dict[str, str]:
    """
    Check the health of the database connection.
    Returns a JSON object with the status of the connection.
    """
    try:
        return await health_check_service()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
