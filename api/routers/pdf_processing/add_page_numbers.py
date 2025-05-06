from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services.pdf_processing.add_page_numbers_service import add_page_numbers_service

router = APIRouter()


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
    )
) -> StreamingResponse:
    """
    - **file**: source PDF to which page numbers will be added.
    """
    try:
        return await add_page_numbers_service(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
