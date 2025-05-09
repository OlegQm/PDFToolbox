import io
import json
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter

async def remove_pages_service(
    file: UploadFile,
    pages_str: str
) -> StreamingResponse:
    """
    Remove specified pages from the uploaded PDF and return the new PDF.

    Args:
        file (UploadFile): PDF file to process (content_type must be 'application/pdf').
        pages_str (str): JSON string representing a list of 1-based page numbers to remove.

    Returns:
        StreamingResponse: PDF with specified pages removed.

    Raises:
        HTTPException(400): on invalid input or PDF errors.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported.")

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(400, "Cannot read PDF.")

    total = len(reader.pages)
    if total == 0:
        raise HTTPException(400, "PDF contains no pages.")

    try:
        raw = json.loads(pages_str)
        pages_to_remove = sorted({int(p) for p in raw})
    except Exception:
        raise HTTPException(400, "Invalid pages JSON. Use a JSON array of integers, e.g. [1,3,5].")

    if not pages_to_remove:
        raise HTTPException(400, "No pages specified for removal.")
    for p in pages_to_remove:
        if p < 1 or p > total:
            raise HTTPException(400, f"Page {p} out of range (1..{total}).")

    if len(pages_to_remove) >= total:
        raise HTTPException(400, "Cannot remove all pages; at least one page must remain.")

    writer = PdfWriter()
    for idx, page in enumerate(reader.pages, start=1):
        if idx not in pages_to_remove:
            writer.add_page(page)

    buf = io.BytesIO()
    try:
        writer.write(buf)
    except Exception as e:
        raise HTTPException(500, f"Error writing PDF: {e}")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=trimmed.pdf"}
    )
