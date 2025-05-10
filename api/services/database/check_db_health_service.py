from typing import Dict
from fastapi import HTTPException

from utils.database import mongo_db

async def health_check_service() -> Dict[str, str]:
    ok = await mongo_db.verify_connection()
    if not ok:
        raise HTTPException(503, "Database connection failed")
    return {"status": "ok"}
