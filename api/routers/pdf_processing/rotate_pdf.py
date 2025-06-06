from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection
from services.pdf_processing.rotate_pdf_service import rotate_pdf as rotate_pdf_service
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from utils.auth import verify_token
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/rotate-pdf",
    response_class=StreamingResponse,
    summary="Rotate PDF pages",
    description="Accepts a PDF file and a JSON‐encoded string of rotation instructions; "
                "returns the rotated PDF."
)
async def rotate_pdf_endpoint(
    request: Request,
    file: UploadFile = File(...),
    rotations: str = Form(...),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
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
        result = await rotate_pdf_service(file, rotations)
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action=f"Rotated PDF with rotations: {rotations}",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
