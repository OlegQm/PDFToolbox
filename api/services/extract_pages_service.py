# src/services/extract_pages_service.py
from fastapi import File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
from typing import List
import io, json

async def extract_pages_service(
    file: UploadFile = File(...),
    pages: str = Form(...)
) -> StreamingResponse:
    """
    Extract specified pages from a PDF and return them as a new PDF.

    Args:
        file (UploadFile): Uploaded PDF (content_type must be 'application/pdf').
        pages (str): JSON string like "[1,3,5]" — page numbers to extract (1-based).

    Returns:
        StreamingResponse: Newly created PDF with the extracted pages.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported.")

    try:
        raw = json.loads(pages)
        page_numbers: List[int] = [int(p) for p in raw]
    except Exception:
        raise HTTPException(400, "Invalid pages JSON. Use e.g. [1,3,5]")

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(400, "Cannot read PDF.")

    total = len(reader.pages)
    for p in page_numbers:
        if p < 1 or p > total:
            raise HTTPException(
                400,
                f"Page {p} out of range. PDF has pages 1...{total}."
            )

    writer = PdfWriter()
    for p in page_numbers:
        writer.add_page(reader.pages[p - 1])

    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=extracted.pdf"}
    )
