from typing import Dict
from fastapi import APIRouter, Form, Depends, Request
from motor.motor_asyncio import AsyncIOMotorCollection
from services.authorization.registration_service import (
    create_user,
    get_users_collection
)
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["Authorization"])


@router.post(
    "/authorization/register",
    summary="Register a new user",
    description="Create a new user account with username & password."
)
async def register(
    request: Request,
    username: str = Form(..., description="Desired username"),
    password: str = Form(..., description="Desired password"),
    users = Depends(get_users_collection),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> Dict[str, str]:
    """
    - **username**: must be unique  
    - **password**: will be hashed before storage  
    """
    user = await create_user(username, password, users)
    city, country = await resolve_geo(request.client.host)
    await log_action(
        username=username,
        action="User registration",
        city=city,
        country=country,
        history_collection=history_collection
    )
    return {"msg": f"User '{user['username']}' created."}
