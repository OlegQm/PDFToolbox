from fastapi import File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
import io
from typing import List

async def merge_pdfs_service(
    files: List[UploadFile] = File(
        ...,
        description="List of PDF files to merge. All must have content_type 'application/pdf'."
    )
) -> StreamingResponse:
    """
    Merge multiple PDF files into a single PDF, in the order they were uploaded.
    
    Args:
        files (List[UploadFile]): List of uploaded PDF files.
    
    Returns:
        StreamingResponse: Merged PDF (attachment; filename=merged.pdf).
    
    Raises:
        HTTPException(400): If any file is not a PDF or cannot be read.
    """
    if not files or len(files) < 2:
        raise HTTPException(400, "Please upload at least two PDF files to merge.")

    writer = PdfWriter()

    for upload in files:
        if upload.content_type != "application/pdf":
            raise HTTPException(400, f"File '{upload.filename}' is not a PDF.")
        try:
            reader = PdfReader(upload.file)
        except Exception:
            raise HTTPException(400, f"Cannot read PDF '{upload.filename}'.")
        for page in reader.pages:
            writer.add_page(page)

    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"}
    )
