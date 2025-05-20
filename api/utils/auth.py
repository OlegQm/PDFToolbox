import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY_FOR_TOKEN", "default_env_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

class TokenData(BaseModel):
    sub: Optional[str] = None

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a JSON Web Token (JWT) for a given subject with an optional expiration time.

    Args:
        subject (str): The subject (e.g., user identifier) to include in the token payload.
        expires_delta (Optional[timedelta]): The time duration after which the token will expire.
            If not provided, a default expiration time is used.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        jwt.PyJWTError: If there is an error during token encoding.

    Notes:
        - The token payload includes the subject ("sub") and expiration time ("exp").
        - The expiration time is calculated based on the current UTC time.
        - The token is signed using the SECRET_KEY and the specified ALGORITHM.
    """
    to_encode = {"sub": subject}
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency — extracts the token from Authorization: Bearer <token>,
    verifies the signature and expiration, and returns the sub field (username/user_id).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return sub
