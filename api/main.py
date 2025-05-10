import os
import logging
from contextlib import asynccontextmanager

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
from routers.authorization import (
    token,
    registration
)
from routers.database import check_db_health
from utils.database import mongo_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

API_PREFIX = os.getenv("API_PREFIX", "")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_db.connect()
    yield
    await mongo_db.close()

app = FastAPI(
    root_path=API_PREFIX,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
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
api_router.include_router(registration.router)

######## Database routers ########
api_router.include_router(check_db_health.router)

app.include_router(api_router)
