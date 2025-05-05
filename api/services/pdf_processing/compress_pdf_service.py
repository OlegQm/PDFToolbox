import io
import tempfile
import subprocess
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse

async def compress_pdf_service(
    file: UploadFile
) -> StreamingResponse:
    """
    Compress a PDF using Ghostscript without reordering pages.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as infile:
        infile.write(data)
        infile_path = infile.name

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as outfile:
        outfile_path = outfile.name

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={outfile_path}",
        infile_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        err = result.stderr.decode(errors="ignore")
        raise HTTPException(status_code=500, detail=f"Ghostscript error: {err}")

    with open(outfile_path, "rb") as f:
        compressed_data = f.read()

    buf = io.BytesIO(compressed_data)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=compressed.pdf"}
    )
