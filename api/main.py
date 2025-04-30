import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from routers import test_endpoint

root_path = os.getenv("FASTAPI_ROOT_PATH", "")
# app = FastAPI(root_path=root_path)

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    root_path=root_path,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(test_endpoint.router)
app.include_router(api_router)
