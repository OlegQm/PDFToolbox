from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services.pdf_processing.merge_pdfs_service import merge_pdfs_service

router = APIRouter(tags=["pdftools"])


@router.post(
    "/merge-pdfs",
    response_class=StreamingResponse,
    summary="Merge multiple PDFs into one",
    description="""
Accepts multiple PDF files via multipart/form-data, concatenates them in the order
provided, and returns a single merged PDF.
"""
)
async def merge_pdfs(
    files: list[UploadFile] = File(
        ...,
        description="Upload two or more PDF files to merge."
    )
) -> StreamingResponse:
    """
    Merge PDFs endpoint.

    - **files**: list of PDF files (must be application/pdf)
    """
    try:
        return await merge_pdfs_service(files)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Internal error while merging: {e}")
