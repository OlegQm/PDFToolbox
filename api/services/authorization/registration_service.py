from typing import Dict
from passlib.context import CryptContext
from fastapi import HTTPException, status

_users: Dict[str, str] = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(username: str, password: str):
    if username in _users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists."
        )
    hashed = pwd_context.hash(password)
    _users[username] = hashed
    return {"username": username}


def authenticate_user(username: str, password: str) -> bool:
    hashed = _users.get(username)
    if not hashed or not pwd_context.verify(password, hashed):
        return False
    return True
