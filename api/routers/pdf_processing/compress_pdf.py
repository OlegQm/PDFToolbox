from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services.pdf_processing.compress_pdf_service import compress_pdf_service

router = APIRouter()


@router.post(
    "/compress-pdf",
    response_class=StreamingResponse,
    summary="Compress a PDF file using Ghostscript",
    description="Accepts a PDF and returns a compressed version without reordering pages."
)
async def compress_pdf(
    file: UploadFile = File(..., description="PDF file to compress (application/pdf)")
) -> StreamingResponse:
    """
    - **file**: source PDF to compress
    """
    try:
        return await compress_pdf_service(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
