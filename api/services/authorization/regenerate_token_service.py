from typing import Dict, Any
from datetime import timedelta
from fastapi import HTTPException, status
from utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def regenerate_user_token_service(
    user: str
) -> Dict[str, Any]:
    """
    Regenerates a new access token for a given user.

    Args:
        user (str): The username for which to regenerate the access token.

    Returns:
        Dict[str, Any]: A dictionary containing the new access token and its type.

    Raises:
        HTTPException: If the provided username is empty or consists only of whitespace.
    """
    if not user.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        subject=user,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
