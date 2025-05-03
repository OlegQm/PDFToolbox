import io
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

async def add_page_numbers_service(
    file: UploadFile
) -> StreamingResponse:
    """
    Add page numbers to each page of the uploaded PDF and return a new PDF.

    Args:
        file (UploadFile): PDF file to process (content_type must be 'application/pdf').

    Returns:
        StreamingResponse: A PDF with page numbers added at the bottom center of each page.

    Raises:
        HTTPException(400): If file is not a PDF or cannot be read.
        HTTPException(500): On any internal processing error.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported.")

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(400, "Cannot read PDF.")

    writer = PdfWriter()
    total_pages = len(reader.pages)

    for idx, page in enumerate(reader.pages, start=1):
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        can.setFont("Helvetica", 12)
        can.drawCentredString(width / 2, 10 * mm, str(idx))
        can.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        overlay_page = overlay_pdf.pages[0]
        page.merge_page(overlay_page)

        writer.add_page(page)

    output = io.BytesIO()
    try:
        writer.write(output)
    except Exception as e:
        raise HTTPException(500, f"Error writing PDF: {e}")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=numbered.pdf"}
    )
