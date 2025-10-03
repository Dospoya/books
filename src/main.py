import logging

from fastapi import FastAPI

from src.api.routers import main_router
from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_title)

app.include_router(main_router)
