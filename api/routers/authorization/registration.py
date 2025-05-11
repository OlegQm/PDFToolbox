from typing import Dict
from fastapi import APIRouter, Form, Depends
from services.authorization.registration_service import (
    create_user,
    get_users_collection
)
router = APIRouter(tags=["auth"])

@router.post(
    "/authorization/register",
    summary="Register a new user",
    description="Create a new user account with username & password."
)
async def register(
    username: str = Form(..., description="Desired username"),
    password: str = Form(..., description="Desired password"),
    users=Depends(get_users_collection)
) -> Dict[str, str]:
    """
    - **username**: must be unique  
    - **password**: will be hashed before storage  
    """
    user = await create_user(username, password, users)
    return {"msg": f"User '{user['username']}' created."}