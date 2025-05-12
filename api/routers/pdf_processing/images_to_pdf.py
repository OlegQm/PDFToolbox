from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from services.pdf_processing.images_to_pdf_service import images_to_pdf_service
from utils.auth import verify_token

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/images-to-pdf",
    response_class=StreamingResponse,
    summary="Convert multiple images to a single PDF",
    description="""
Accepts one or more image files (JPEG, PNG, etc.), merges them into a single PDF 
(one image per page), and returns that PDF.
"""
)
async def images_to_pdf(
    files: list[UploadFile] = File(
        ...,
        description="Upload all images to include (content types must start with 'image/')"
    ),
    user: str = Depends(verify_token)
) -> StreamingResponse:
    """
    - **files**: list of image files to convert into PDF
    """
    try:
        return await images_to_pdf_service(files)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
