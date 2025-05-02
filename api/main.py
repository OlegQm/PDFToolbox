from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter

from routers import (
    rotate_pdf,
)

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/openapi.json",
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
