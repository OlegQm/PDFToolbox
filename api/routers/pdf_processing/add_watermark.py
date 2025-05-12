from typing import Annotated, Literal
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import Field
from services.pdf_processing.add_watermark_service import add_watermark_service
from utils.auth import verify_token

router = APIRouter(tags=["pdftools"])


@router.post(
    "/add-watermark",
    response_class=StreamingResponse,
    summary="Add a single watermark to each PDF page",
    description="""
Accepts a PDF and watermark parameters, places exactly one watermark per page
at the chosen position.
"""
)
async def add_watermark(
    file: UploadFile = File(
        ..., description="PDF file to watermark (application/pdf)"
    ),
    text: Annotated[
        str,
        Field(..., min_length=1, description="Watermark text (non-empty)")
    ] = Form(...),
    font_name: Annotated[
        str,
        Field("Helvetica", min_length=1, description="Base font, e.g. Helvetica")
    ] = Form("Helvetica"),
    bold: bool = Form(False, description="Bold text?"),
    italic: bool = Form(False, description="Italic text?"),
    font_size: Annotated[
        int,
        Field(..., gt=0, description="Font size in points (must be >0)")
    ] = Form(40),
    color: Annotated[
        str,
        Field(
            "#FF6600",
            pattern=r"^#([0-9A-Fa-f]{6})$",
            description="Hex color string, e.g. #FF6600"
        )
    ] = Form("#FF6600"),
    alpha: Annotated[
        float,
        Field(..., ge=0.0, le=1.0, description="Transparency 0.0–1.0")
    ] = Form(0.4),
    position: Annotated[
        Literal["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        Field(
            "center",
            description="Position: top-left, top-right, bottom-left, bottom-right, center"
        )
    ] = Form("center"),
    offset_x: Annotated[
        float,
        Field(..., ge=0.0, description="Horizontal offset from edge in mm (>=0)")
    ] = Form(10.0),
    offset_y: Annotated[
        float,
        Field(..., ge=0.0, description="Vertical offset from edge in mm (>=0)")
    ] = Form(10.0),
    angle: Annotated[
        float,
        Field(..., ge=-360.0, le=360.0, description="Rotation angle in degrees (-360…360)")
    ] = Form(0.0),
    user: str = Depends(verify_token)
) -> StreamingResponse:
    """
    - **file**: source PDF  
    - **text**, **font_name**, **bold**, **italic**, **font_size**  
    - **color**, **alpha**, **position**, **offset_x**, **offset_y**, **angle**  
    """
    try:
        return await add_watermark_service(
            file,
            text,
            font_name,
            bold,
            italic,
            font_size,
            color,
            alpha,
            position,
            offset_x,
            offset_y,
            angle
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error: {e}")
