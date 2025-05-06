from typing import Dict, Any
from fastapi import APIRouter, Form, HTTPException, status
from services.authorization.token_service import login_for_access_token_service

router = APIRouter()


@router.post(
    "/token",
    summary="Obtain access token",
    description="""
Authenticate user by username and password and return a JSON Web Token (JWT).

- **username**: user's login
- **password**: user's secret

On success returns `{ "access_token": "...", "token_type": "bearer" }`.  
On failure returns 401 Unauthorized.
"""
)
def login_for_access_token(
    username: str = Form(..., description="The user's username"),
    password: str = Form(..., description="The user's password")
) -> Dict[str, Any]:
    """
    Validate credentials and generate an access token.

    1. Verify that username & password are correct.
    2. Create a JWT with a ACCESS_TOKEN_EXPIRE_MINUTES‑minute expiration.
    3. Return the token and token_type.
    """
    try:
        return login_for_access_token_service(
            username=username,
            password=password
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
