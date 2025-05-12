from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import Field
from services.pdf_processing.remove_pages_service import remove_pages_service
from utils.auth import verify_token

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/remove-pages",
    response_class=StreamingResponse,
    summary="Remove specified pages from a PDF",
    description="""
Accepts a PDF file and a JSON-encoded list of 1-based page numbers to remove,
returns a new PDF with those pages removed.
"""
)
async def remove_pages(
    file: UploadFile = File(
        ..., description="PDF file to process (application/pdf)"
    ),
    pages: Annotated[
        str,
        Field(..., description="JSON array of page numbers to remove, e.g. [2,5]")
    ] = Form(...),
    user: str = Depends(verify_token)
) -> StreamingResponse:
    """
    - **file**: source PDF
    - **pages**: JSON array of pages (1-based) to remove
    """
    try:
        return await remove_pages_service(file, pages)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
