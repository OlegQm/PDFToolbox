from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from services.pdf_processing.split_pdf_service import split_pdf_service

router = APIRouter(tags=["pdftools"])


@router.post(
    "/split-pdf",
    response_class=StreamingResponse,
    summary="Split a PDF into two parts",
    description="""
Upload a PDF and an integer `split_at`. The first `split_at` pages go into `part1.pdf`,
the rest into `part2.pdf`. Both parts are returned as a ZIP archive.
"""
)
async def split_pdf(
    file: UploadFile = File(
        ...,
        description="The PDF file to split (content-type must be application/pdf)."
    ),
    split_at: int = Form(
        ...,
        gt=0,
        description="Number of pages to keep in the first PDF (must be >=1)."
    )
) -> StreamingResponse:
    """
    - **file**: source PDF  
    - **split_at**: how many pages to include in the first part  
    """
    try:
        return await split_pdf_service(file, split_at)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
