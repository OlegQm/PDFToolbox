from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from services.pdf_processing.rotate_pdf_service import rotate_pdf as rotate_pdf_service
from utils.auth import verify_token

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/rotate-pdf",
    response_class=StreamingResponse,
    summary="Rotate PDF pages",
    description="Accepts a PDF file and a JSON‐encoded string of rotation instructions; "
                "returns the rotated PDF."
)
async def rotate_pdf_endpoint(
    file: UploadFile = File(...),
    rotations: str = Form(...),
    user: str = Depends(verify_token)
) -> StreamingResponse:
    """
    Rotate pages of a PDF file based on the specified rotations JSON.

    This endpoint accepts multipart/form-data with:
    - **file**: source PDF  
    - **rotations**: JSON list of rotations, e.g. `[{"page":1,"degrees":90}]`  
    - **user**: current user (automatically provided after token verification)

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
