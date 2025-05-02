from fastapi import File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
from typing import List
import io, json
from utils.shemas import Rotation

async def rotate_pdf(
    file: UploadFile = File(...),
    rotations: str = Form(...)
) -> StreamingResponse:
    """
    Rotate pages of a PDF file based on the specified rotations JSON.

    This asynchronous endpoint accepts a PDF file via multipart/form-data and a JSON‑encoded
    string of rotation instructions. It parses the JSON into Rotation models, applies each
    rotation to the corresponding page, and returns the resulting PDF as a streaming response.

    Args:
        file (UploadFile): The uploaded PDF file to be rotated. Must have content type
            "application/pdf".
        rotations (str): A JSON string representing a list of rotation instructions.
            Each instruction must match the Rotation schema (page: int, degrees: float).

    Returns:
        StreamingResponse: The rotated PDF, served with a Content-Disposition header
            to prompt download as "rotated.pdf".

    Raises:
        HTTPException: If the file is not a PDF, cannot be read, or the rotations JSON is invalid.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:
        raw_list = json.loads(rotations)
        rotations_list: List[Rotation] = [Rotation(**item) for item in raw_list]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid rotations JSON")

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot read PDF.")

    total_pages = len(reader.pages)

    for rot in rotations_list:
        if rot.page < 1 or rot.page > total_pages:
            raise HTTPException(
                status_code=400,
                detail=f"Page {rot.page} is out of range. PDF has {total_pages} pages."
            )

    writer = PdfWriter()
    rot_map = {r.page: r.degrees for r in rotations_list}

    for idx, page in enumerate(reader.pages, start=1):
        if idx in rot_map:
            rotation_angle = int(rot_map[idx])
            if rotation_angle % 90 != 0:
                raise HTTPException(
                    status_code=400,
                    detail="Rotation must be a multiple of 90 degrees."
                )
            page.rotate(int(rot_map[idx]))
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=rotated.pdf"}
    )
