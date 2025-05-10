from typing import Annotated
from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from pydantic import Field, HttpUrl
from services.pdf_processing.url_to_pdf_service import url_to_pdf_service

router = APIRouter(tags=["pdftools"])


@router.post(
    "/url-to-pdf",
    response_class=StreamingResponse,
    summary="Convert a web page URL to PDF",
    description="Accepts a valid HTTP/HTTPS URL and returns a PDF rendering of that page."
)
async def url_to_pdf(
    url: Annotated[
        HttpUrl,
        Field(
            ..., description="HTTP or HTTPS URL to convert to PDF"
        )
    ] = Form(...)
) -> StreamingResponse:
    """
    - **url**: must be a valid HTTP/HTTPS URL (Pydantic HttpUrl)
    """
    return await url_to_pdf_service(str(url))
