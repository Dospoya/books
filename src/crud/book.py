from typing import Sequence

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book, BookGenre
from src.schemas.book import BookCreate
from src.schemas.book_query import BookQuery


class BookCRUD():
    async def get_multi(
        self,
        params: BookQuery,
        session: AsyncSession
    ) -> tuple[Sequence[Book], int, int, int]:
        stmt = select(Book)
        if params.q:
            stmt = stmt.where(Book.title.ilike(f'%{params.q}%'))
        if params.published_year is not None:
            stmt = stmt.where(Book.published_year == params.published_year)
        if params.rating_min is not None:
            stmt = stmt.where(Book.rating >= params.rating_min)
        if params.rating_max is not None:
            stmt = stmt.where(Book.rating <= params.rating_max)
        if params.genre_id:
            stmt = stmt.join(BookGenre, BookGenre.book_id == Book.id).where(
                BookGenre.genre_id == params.genre_id
            )
        stmt = stmt.order_by(
            desc(params.sort) if params.order == 'desc' else asc(params.sort)
        )
        total: int | None = await session.scalar(
            select(func.count()).select_from(stmt.subquery())
        )

        stmt = stmt.offset(
            (params.page -  1) * params.page_size
        ).limit(params.page_size)

        return (
            (await session.execute(stmt)).scalars().all(),
            total if isinstance(total, int) else 0,
            params.page,
            params.page_size
        )

    # async def create(
    #     self,
    #     obj_in: BookCreate,
    #     session: AsyncSession,
    # ) -> Book:
    #     ...

    # async def update(self):
    #     ...

    # async def remove(self):
    #     ...


book_crud = BookCRUD()
