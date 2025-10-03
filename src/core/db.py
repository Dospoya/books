from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from src.core.config import settings


class TableNameMixin():
    """Миксин, автоматически задающий __tablename__ по имени класса."""
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Base(DeclarativeBase, TableNameMixin):
    """Базовый класс для всех ORM-моделей."""


class UUIDMixin:
    """Миксин с UUID первичным ключом."""
    id: Mapped[UUID] = mapped_column(
        PG_UUID,
        primary_key=True,
        default=uuid4
    )


class TimeStampMixin:
    """Миксин с аудитными полями created_at / updated_at."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )


engine: AsyncEngine = create_async_engine(
    url=settings.database_url,
    echo=True
)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    """Возвращает асинхронную сессию SQLAlchemy для FastAPI зависимостей.

    Yields:
        Экземпляр асинхронной сессии.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
