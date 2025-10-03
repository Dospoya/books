from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.types import PositiveInt

from src.schemas.base import BaseReadModel
from src.schemas.contributor import ContributorLink
from src.schemas.validators import (
    validate_rating,
)


class BookBase(BaseModel):
    """Базовая схема книги.

    Содержит обязательные данные: название, рейтинг, описание и год публикации.
    """

    title: str
    rating: Decimal | None
    description: str | None
    published_year: PositiveInt | None = Field(None, ge=1450, le=2100)

    @field_validator('rating')
    def _validate_rating_nullable(cls, v):
        return validate_rating(v, allow_none=True)


class BookCreate(BookBase):
    """Схема создания книги."""

    genre_ids: list[UUID] = []
    contributors: list[ContributorLink] = []


class BookUpdate(BaseModel):
    """Схема обновления книги.

    Все поля опциональны, лишние поля запрещены.
    """

    model_config = ConfigDict(extra='forbid')
    title: str | None = None
    rating: Decimal | None = None
    description: str | None = None
    published_year: PositiveInt | None = Field(None, ge=1450, le=2100)

    @field_validator('rating')
    def _validate_rating_nullable(cls, v):
        return validate_rating(v, allow_none=True)


class BookDB(BaseReadModel, BookCreate):
    """Схема книги в БД."""


class BookResponse(BaseModel):
    """Схема ответа со списком книг и параметрами пагинации."""

    items: list[BookDB]
    total: int
    page: int
    page_size: int
