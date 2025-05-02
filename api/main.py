import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter

from routers import (
    rotate_pdf,
)

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
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(rotate_pdf.router)

app.include_router(api_router)
