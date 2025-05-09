from typing import Dict, Any
from fastapi import HTTPException, status
from utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

def login_for_access_token_service(
    username: str,
    password: str
) -> Dict[str, Any]:
    """
    Validate credentials and generate an access token.
    - Checks that the provided username and password match a valid user.
    - Creates a JWT with a ACCESS_TOKEN_EXPIRE_MINUTES‑minute expiration.
    - Returns the token and its type.
    """
    # TODO ANTONIO: Добавить проверку пользователя в БД
    if not (username == "admin" and password == "secret"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=username,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
