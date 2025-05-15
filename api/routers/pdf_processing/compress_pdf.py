from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorCollection
from services.pdf_processing.compress_pdf_service import compress_pdf_service
from utils.auth import verify_token
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/compress-pdf",
    response_class=StreamingResponse,
    summary="Compress a PDF file using Ghostscript",
    description="Accepts a PDF and returns a compressed version without reordering pages."
)
async def compress_pdf(
    request: Request,
    file: UploadFile = File(..., description="PDF file to compress (application/pdf)"
    ),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
 )-> StreamingResponse:
    """
    - **file**: source PDF to compress
    """
    try:
        result = await compress_pdf_service(file)
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action="PDF compression",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
