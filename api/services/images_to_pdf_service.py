import io
from typing import List
from PIL import Image

from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse

async def images_to_pdf_service(
    files: List[UploadFile]
) -> StreamingResponse:
    """
    Merge uploaded images into a single PDF.

    Args:
        files (List[UploadFile]): List of files – images (JPEG, PNG, etc.)

    Returns:
        StreamingResponse: PDF document with all images, one per page.

    Raises:
        HTTPException(400): If no files are provided, invalid file type, or read error.
    """
    if not files:
        raise HTTPException(400, "Please upload at least one image.")

    images = []
    for upload in files:
        ct = upload.content_type or ""
        if not ct.startswith("image/"):
            raise HTTPException(400, f"File '{upload.filename}' is not an image.")
        try:
            img = Image.open(upload.file)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)
        except Exception:
            raise HTTPException(400, f"Cannot process image '{upload.filename}'.")

    first, rest = images[0], images[1:]

    buf = io.BytesIO()
    try:
        first.save(
            buf,
            format="PDF",
            save_all=True,
            append_images=rest,
        )
    except Exception as e:
        raise HTTPException(500, f"Error generating PDF: {e}")

    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=images.pdf"}
    )
