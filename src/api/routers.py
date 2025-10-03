from fastapi import APIRouter

from src.api.endpoints import book_router, health_router


main_router = APIRouter(prefix='/api')
main_router.include_router(book_router, prefix='/v1/books', tags=['Book'])
main_router.include_router(health_router, prefix='/ping', tags=['HealthCheck'])
