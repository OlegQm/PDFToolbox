from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from services.rotate_pdf_service import rotate_pdf as rotate_pdf_service

router = APIRouter()


@router.post(
    "/rotate-pdf",
    response_class=StreamingResponse,
    summary="Rotate PDF pages",
    description="Accepts a PDF file and a JSON‐encoded string of rotation instructions; "
                "returns the rotated PDF."
)
async def rotate_pdf_endpoint(
    file: UploadFile = File(...),
    rotations: str = Form(...)
) -> StreamingResponse:
    """
    Rotate pages of a PDF file based on the specified rotations JSON.

    This endpoint accepts multipart/form-data with:
      - file: UploadFile (must be application/pdf)
      - rotations: JSON string of [{ page: int, degrees: float }, ...]

    It delegates parsing, validation, rotation logic to the service layer
    and returns the resulting PDF as a streaming download.

    Raises:
        HTTPException: on invalid content type, unreadable PDF,
                       or malformed rotations JSON.
    """
    try:
        return await rotate_pdf_service(file, rotations)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
