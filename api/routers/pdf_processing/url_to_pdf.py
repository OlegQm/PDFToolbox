from typing import Annotated
from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import Field, HttpUrl
from motor.motor_asyncio import AsyncIOMotorCollection
from services.pdf_processing.url_to_pdf_service import url_to_pdf_service
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from utils.auth import verify_token
from services.authorization.geoip_service import resolve_geo

router = APIRouter(tags=["PDF tools"])


@router.post(
    "/url-to-pdf",
    response_class=StreamingResponse,
    summary="Convert a web page URL to PDF",
    description="Accepts a valid HTTP/HTTPS URL and returns a PDF rendering of that page."
)
async def url_to_pdf(
    request: Request,
    url: Annotated[
        HttpUrl,
        Field(
            ...,
            description="HTTP or HTTPS URL to convert to PDF"
        )
    ] = Form(...),
    user: str = Depends(verify_token),
    history_collection: AsyncIOMotorCollection = Depends(get_history_collection)
) -> StreamingResponse:
    """
    - **url**: must be a valid HTTP/HTTPS URL (Pydantic HttpUrl)
    """
    try:
        result = await url_to_pdf_service(str(url))
        city, country = await resolve_geo(request.client.host)
        await log_action(
            username=user,
            action=f"Converted URL {url} to PDF",
            city=city,
            country=country,
            history_collection=history_collection
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")