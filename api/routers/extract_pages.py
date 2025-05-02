from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from services.extract_pages_service import extract_pages_service

router = APIRouter()

@router.post(
    "/extract-pages",
    response_class=StreamingResponse,
    summary="Extract specified pages from a PDF",
    description="""
Accepts a PDF file and a JSON‐encoded list of page numbers (1-based), extracts those
pages into a new PDF, and returns it as a downloadable file.
"""
)
async def extract_pages(
    file: UploadFile = File(
        ...,
        description="The PDF file to extract pages from. Content type must be 'application/pdf'."
    ),
    pages: str = Form(
        ...,
        description="A JSON‐encoded array of page numbers, e.g. `[1, 3, 5]`."
    )
) -> StreamingResponse:
    """
    Extract specified pages from the uploaded PDF.

    - **file**: the source PDF document
    - **pages**: JSON array of 1-based page indices to extract

    Raises:
        HTTPException(400): if content type is wrong, JSON is invalid, or page numbers out of range.
        HTTPException(500): on unexpected internal errors.
    """
    try:
        return await extract_pages_service(file, pages)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}"
        )
