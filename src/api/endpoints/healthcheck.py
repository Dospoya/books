from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.schemas.healthcheck import HealthCheck


router = APIRouter()


@router.get(
    '',
    response_model=HealthCheck
)
async def get_health(db: AsyncSession = Depends(get_async_session)):
    """Проверка доступности базы данных.

    Args:
        db: Асинхронная сессия SQLAlchemy.

    Returns:
        Объект HealthCheck со статусом "ok", если база доступна.

    Raises:
        HTTPException: Если не удалось подключиться к базе данных.
    """
    try:
        await db.scalar(select(1))
        return {'status': 'ok'}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Ошибка подключения к базе данных {e}'
        )
