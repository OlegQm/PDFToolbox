import io
import os
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import pdfkit

async def url_to_pdf_service(
    url: str
) -> StreamingResponse:
    """
    Convert a web page URL to PDF using wkhtmltopdf via pdfkit.

    Requires wkhtmltopdf installed in the Docker container or specified via WKHTMLTOPDF_PATH env var.

    Args:
        url (str): HTTP or HTTPS URL of the page to convert.

    Returns:
        StreamingResponse: PDF bytes of the rendered page.

    Raises:
        HTTPException(500): if wkhtmltopdf is unavailable or PDF generation fails.
    """
    wk_path = os.getenv("WKHTMLTOPDF_PATH")
    options = {
        'enable-local-file-access': None,
        'no-outline': None,
    }
    try:
        if wk_path:
            config = pdfkit.configuration(wkhtmltopdf=wk_path)
            pdf_bytes = pdfkit.from_url(
                url,
                False,
                configuration=config,
                options=options
            )
        else:
            pdf_bytes = pdfkit.from_url(
                url,
                False,
                options=options
            )
    except OSError as e:
        raise HTTPException(500, f"wkhtmltopdf executable not found or not executable: {e}")
    except Exception as e:
        raise HTTPException(500, f"Error generating PDF from URL: {e}")

    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=page.pdf"}
    )
