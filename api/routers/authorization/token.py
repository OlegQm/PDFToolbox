from typing import Dict, Any
from fastapi import APIRouter, Form, HTTPException, status, Depends, Request
from motor.motor_asyncio import AsyncIOMotorCollection
from services.authorization.token_service import login_for_access_token_service
from services.authorization.registration_service import get_users_collection
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["Authorization"])


@router.post(
    "/authorization/token",
    summary="Obtain access token",
    description="""
Authenticate user by username and password and return a JSON Web Token (JWT).

- **username**: user's login
- **password**: user's secret

On success returns `{ "access_token": "...", "token_type": "bearer" }`.  
On failure returns 401 Unauthorized.
"""
)
async def login_for_access_token(
    request: Request,
    username: str = Form(..., description="The user's username"),
    password: str = Form(..., description="The user's password"),
    users = Depends(get_users_collection),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> Dict[str, Any]:
    """
    Validate credentials and generate an access token.

    1. Verify that username & password are correct.
    2. Create a JWT with a ACCESS_TOKEN_EXPIRE_MINUTES‑minute expiration.
    3. Return the token and token_type.
    """
    try:
        result = await login_for_access_token_service(
            username=username,
            password=password,
            users=users
        )
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=username,
            action="User login",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
