import io
import zipfile

from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter


async def split_pdf_service(
    file: UploadFile,
    split_at: int
) -> StreamingResponse:
    """
    Split uploaded PDF into two PDFs at page `split_at`.
    Returns a ZIP containing part1.pdf (pages 1...split_at)
    and part2.pdf (pages split_at+1...end).

    Raises HTTPException(400) on any validation error.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are supported.")

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(400, "Cannot read PDF.")

    total = len(reader.pages)

    if split_at < 1 or split_at >= total:
        raise HTTPException(
            400,
            f"split_at must be between 1 and {total-1}, got {split_at}."
        )

    writer1 = PdfWriter()
    writer2 = PdfWriter()

    for i in range(split_at):
        writer1.add_page(reader.pages[i])
    for i in range(split_at, total):
        writer2.add_page(reader.pages[i])

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, mode="w") as z:
        buf1 = io.BytesIO()
        writer1.write(buf1)
        buf1.seek(0)
        z.writestr("part1.pdf", buf1.read())

        buf2 = io.BytesIO()
        writer2.write(buf2)
        buf2.seek(0)
        z.writestr("part2.pdf", buf2.read())

    zip_buf.seek(0)
    return StreamingResponse(
        zip_buf,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=split.zip"}
    )
