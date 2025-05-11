from typing import Dict
from passlib.context import CryptContext
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from utils.database import mongo_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_users_collection() -> AsyncIOMotorCollection:
    return await mongo_db.get_or_create_collection(
        "users",
        index_fields=[("username", 1)],
        unique=True
    )

async def create_user(
    username: str,
    password: str,
    users: AsyncIOMotorCollection
) -> Dict[str, str]:
    existing = await users.find_one({"username": username})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists."
        )
    hashed = pwd_context.hash(password)
    user_doc = {
        "username": username,
        "password": hashed,
        "is_admin": False
    }
    result = await users.insert_one(user_doc)
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user."
        )
    return {"username": username}

async def authenticate_user(
    username: str,
    password: str,
    users: AsyncIOMotorCollection
) -> bool:
    user = await users.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return True
