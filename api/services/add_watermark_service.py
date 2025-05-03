import io
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color


async def add_watermark_service(
    file: UploadFile,
    text: str,
    font_name: str,
    bold: bool,
    italic: bool,
    font_size: int,
    color: str,
    alpha: float,
    position: str,
    offset_x: float,
    offset_y: float,
    angle: float
) -> StreamingResponse:
    """
    Add a single watermark text on each page at the specified position.
    All parameters are pre-validated in the router, но дублируем критичные проверки здесь.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported.")
    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(400, "Cannot read PDF.")
    total_pages = len(reader.pages)
    if total_pages == 0:
        raise HTTPException(400, "PDF has no pages.")

    if not text.strip():
        raise HTTPException(400, "Watermark text must not be empty")
    if font_size <= 0:
        raise HTTPException(400, "Font size must be > 0")
    if not (0.0 <= alpha <= 1.0):
        raise HTTPException(400, "Alpha must be between 0.0 and 1.0")
    allowed_positions = {"top-left", "top-right", "bottom-left", "bottom-right", "center"}
    if position not in allowed_positions:
        raise HTTPException(400, f"Position must be one of {allowed_positions}")
    if offset_x < 0 or offset_y < 0:
        raise HTTPException(400, "Offsets must be non-negative")
    if not (-360.0 <= angle <= 360.0):
        raise HTTPException(400, "Angle must be between -360 and 360")

    rl_font = font_name
    if bold and italic:
        rl_font += "-BoldOblique"
    elif bold:
        rl_font += "-Bold"
    elif italic:
        rl_font += "-Oblique"

    try:
        hexc = color.lstrip("#")
        r = int(hexc[0:2], 16) / 255
        g = int(hexc[2:4], 16) / 255
        b = int(hexc[4:6], 16) / 255
        rl_color = Color(r, g, b, alpha=alpha)
    except Exception:
        raise HTTPException(400, "Invalid color hex string")

    writer = PdfWriter()

    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        dx = offset_x * mm
        dy = offset_y * mm

        if position == "top-left":
            x = dx
            y = h - dy
        elif position == "top-right":
            x = w - dx
            y = h - dy
        elif position == "bottom-left":
            x = dx
            y = dy
        elif position == "bottom-right":
            x = w - dx
            y = dy
        else:
            x = w / 2
            y = h / 2

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(w, h))
        c.setFont(rl_font, font_size)
        c.setFillColor(rl_color)
        try:
            c.setFillAlpha(alpha)
        except AttributeError:
            pass

        c.saveState()
        c.translate(x, y)
        c.rotate(angle)

        if position == "center":
            text_width = c.stringWidth(text, rl_font, font_size)
            text_height = font_size
            c.translate(-text_width / 2, -text_height / 2)

        c.drawString(0, 0, text)
        c.restoreState()
        c.save()
        packet.seek(0)

        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    out = io.BytesIO()
    try:
        writer.write(out)
    except Exception as e:
        raise HTTPException(500, f"Error writing PDF: {e}")
    out.seek(0)

    return StreamingResponse(
        out,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=watermarked.pdf"}
    )
