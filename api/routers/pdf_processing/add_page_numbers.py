from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection
from services.pdf_processing.add_page_numbers_service import add_page_numbers_service
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from utils.auth import verify_token

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/add-page-numbers",
    response_class=StreamingResponse,
    summary="Add page numbers to a PDF",
    description="""
Accepts a PDF file via multipart/form-data, adds page numbers at the bottom center
of each page, and returns the new PDF as a downloadable file.
"""
)
async def add_page_numbers(
    file: UploadFile = File(
        ...,
        description="The PDF file to number. Content type must be 'application/pdf'."
    ),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> StreamingResponse:
    """
    - **file**: source PDF to which page numbers will be added.
    """
    try:
        result = await add_page_numbers_service(file)
        await log_action(
            username=user,
            action="Added page numbers to PDF",
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
