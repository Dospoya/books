from decimal import Decimal
from enum import Enum
from typing_extensions import Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    PositiveInt
)


class SortField(str, Enum):
    """Доступные поля для сортировки списка книг."""

    TITLE = 'title'
    RATING = 'rating'
    PUBLISHED_YEAR = 'published_year'


class Order(str, Enum):
    """Порядок сортировки."""

    ASC = 'asc'
    DESC = 'desc'


class BookQuery(BaseModel):
    """Схема параметров фильтрации, сортировки и пагинации списка книг."""

    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    sort: SortField = SortField.TITLE
    order: Order = Order.ASC
    rating_max: Decimal | None = None
    rating_min: Decimal | None = None
    published_year: PositiveInt | None = Field(None, ge=1450, le=2100)
    genre_id: UUID | None = None
    q: str | None = None

    @model_validator(mode='after')
    def _check_rating(self) -> Self:
        """Валидатор: rating_max должен быть больше или равен rating_min."""
        if self.rating_max is not None and self.rating_min is not None:
            if self.rating_max < self.rating_min:
                raise ValueError('rating_max должен быть >= rating_min')
        return self
