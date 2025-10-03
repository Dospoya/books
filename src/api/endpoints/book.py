from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.crud.book import book_crud
from src.schemas.book import BookResponse
from src.schemas.book_query import BookQuery


router = APIRouter()

@router.get(
    '',
    response_model=BookResponse,
)
async def get_books(
    params: Annotated[BookQuery, Depends()],
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список книг с фильтрацией, сортировкой и пагинацией.

    Args:
        params: Параметры фильтрации, сортировки и пагинации.
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        Объект с книгами и метаданными пагинации.
    """
    items, total, page, page_size = await book_crud.get_multi(params=params, session=session)
    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size
    }
