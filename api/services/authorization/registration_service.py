from typing import Dict
from passlib.context import CryptContext
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from utils.database import mongo_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_users_collection() -> AsyncIOMotorCollection:
    """
    Asynchronously retrieves the "users" collection from the MongoDB database,
    creating it if it does not already exist. The collection is indexed on the
    "username" field with a unique constraint.

    Returns:
        AsyncIOMotorCollection: The "users" collection from the MongoDB database.
    """
    return await mongo_db.get_or_create_collection(
        "users",
        index_fields=[("username", 1)],
        unique=True
    )

async def create_user(
    username: str,
    password: str,
    users: AsyncIOMotorCollection,
    is_admin: bool = False
) -> Dict[str, str]:
    """
    Asynchronously creates a new user in the database.

    Args:
        username (str): The username of the new user.
        password (str): The plaintext password of the new user.
        users (AsyncIOMotorCollection): The MongoDB collection where user data is stored.
        is_admin (bool): Flag indicating if the user should have admin privileges.

    Returns:
        Dict[str, str]: A dictionary containing the username of the created user.

    Raises:
        HTTPException: If a user with the given username already exists (400 Bad Request).
        HTTPException: If there is an error while inserting the user into the database (500 Internal Server Error).
    """
    existing = await users.find_one({"username": username})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists."
        )
    username = username.strip()
    password = password.strip()
    if not username or len(username) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be a non-empty string."
        )
    if not password or len(password) < 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )
    hashed = pwd_context.hash(password)
    user_doc = {
        "username": username,
        "password": hashed,
        "is_admin": is_admin
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
    """
    Authenticate a user by verifying their username and password.

    Args:
        username (str): The username of the user attempting to authenticate.
        password (str): The password provided by the user for authentication.
        users (AsyncIOMotorCollection): The MongoDB collection containing user data.

    Returns:
        bool: True if the user is successfully authenticated, False otherwise.
    """
    user = await users.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return True
