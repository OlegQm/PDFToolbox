from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection
from services.pdf_processing.images_to_pdf_service import images_to_pdf_service
from utils.auth import verify_token
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo

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
    request: Request,
    files: list[UploadFile] = File(
        ...,
        description="Upload all images to include (content types must start with 'image/')"
    ),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> StreamingResponse:
    """
    - **files**: list of image files to convert into PDF
    """
    try:
        result = await images_to_pdf_service(files)
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action="Converted images to PDF",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
