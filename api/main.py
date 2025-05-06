import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter

from routers.pdf_processing import (
    rotate_pdf,
    extract_pages,
    merge_pdfs,
    split_pdf,
    images_to_pdf,
    add_page_numbers,
    add_watermark,
    remove_pages,
    compress_pdf,
    url_to_pdf
)
from routers.authorization import token

API_PREFIX = os.getenv("API_PREFIX", "")

app = FastAPI(
    root_path=API_PREFIX,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

######## PDF processing routers ########
api_router.include_router(rotate_pdf.router)
api_router.include_router(extract_pages.router)
api_router.include_router(merge_pdfs.router)
api_router.include_router(split_pdf.router)
api_router.include_router(images_to_pdf.router)
api_router.include_router(add_page_numbers.router)
api_router.include_router(add_watermark.router)
api_router.include_router(remove_pages.router)
api_router.include_router(url_to_pdf.router)
api_router.include_router(compress_pdf.router)

######## Authentication routers ########
api_router.include_router(token.router)

app.include_router(api_router)
