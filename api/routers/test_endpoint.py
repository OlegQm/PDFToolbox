from fastapi import APIRouter
from services.test_endpoint_service import get_message

router = APIRouter()

@router.get("/ping")
def pong():
    """
    Handles a GET request to the /ping endpoint.

    Returns:
        dict: A JSON response containing a "message" key with the value "pong!".
    """
    return get_message()

