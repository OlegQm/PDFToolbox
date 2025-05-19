import os
import logging
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

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
    registration,
    regenerate_token
)
from services.authorization.logging_service import (
    get_history_collection,
    log_action
)
from services.authorization.registration_service import (
    get_users_collection,
    authenticate_user,
    create_user
)
from routers.database import (
    check_db_health,
    get_history_logs,
    clear_history_collection,
    export_history_to_csv
)
from utils.database import mongo_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

API_PREFIX = os.getenv("API_PREFIX", "")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_db.connect()
    admin_user = os.getenv("ADMIN_USER") or "admin"
    admin_password = os.getenv("ADMIN_PASSWORD") or "admin"
    try:
        users = await get_users_collection()
        history_collection = await get_history_collection()
        if await authenticate_user(admin_user, admin_password, users):
            logger.info("Admin user already exists.")
        else:
            await create_user(
                username=admin_user,
                password=admin_password,
                users=users,
                is_admin=True
            )
            try:
                await log_action(
                    username=admin_user,
                    action="Admin user creation",
                    city="Bratislava",
                    country="Slovakia",
                    history_collection=history_collection
                )
            except Exception as e:
                logger.error(
                    "Error during logging admin user creation: %s", e
                )
            logger.info("Created admin user.")
    except Exception as e:
        logger.error("Error during admin user creation: %s", e)
        try:
            await log_action(
                username=admin_user,
                action="Admin user creation failed",
                city="Admin secret city",
                country="Admin secret country",
                history_collection=history_collection
            )
        except Exception as e:
            logger.error(
                "Error during logging admin user creation failure: %s", e
            )
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
    ProxyHeadersMiddleware,
    trusted_hosts="*"
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
api_router.include_router(regenerate_token.router)

######## Database routers ########
api_router.include_router(check_db_health.router)
api_router.include_router(get_history_logs.router)
api_router.include_router(clear_history_collection.router)
api_router.include_router(export_history_to_csv.router)

app.include_router(api_router)
