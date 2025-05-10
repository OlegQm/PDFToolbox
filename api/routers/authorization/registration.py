from fastapi import APIRouter, Form
from typing import Dict
from services.authorization.registration_service import create_user

router = APIRouter(tags=["auth"])


@router.post(
    "/authorization/register",
    summary="Register a new user",
    description="Create a new user account with username & password."
)
def register(
    username: str = Form(..., description="Desired username"),
    password: str = Form(..., description="Desired password")
) -> Dict[str, str]:
    """
    - **username**: must be unique  
    - **password**: will be hashed before storage  
    """
    user = create_user(username, password)
    return {"msg": f"User '{user['username']}' created."}