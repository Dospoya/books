from decimal import Decimal
from enum import Enum
from uuid import UUID


from sqlalchemy import (
    CheckConstraint,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base, TimeStampMixin, UUIDMixin


class ContributorRole(str, Enum):
    """Роль участника: автор, редактор или иллюстратор."""

    AUTHOR = 'author'
    ILLUSTRATOR = 'illustrator'
    EDITOR = 'editor'


class Book(UUIDMixin, TimeStampMixin, Base):
    """Модель книги.

    Содержит основную информацию о книге, включая название, рейтинг,
    описание, год публикации и связи с жанрами и участниками.
    """

    title: Mapped[str] = mapped_column(
        String, nullable=False
    )
    rating: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1), nullable=True
    )
    description: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    published_year: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    book_genres: Mapped[list['BookGenre']] = relationship(
        'BookGenre',
        back_populates='book',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    book_contributors: Mapped[list['BookContributor']] = relationship(
        'BookContributor',
        back_populates='book',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    __table_args__ = (
        CheckConstraint(
            '1450 <= published_year <= 2100', name='book_year_range'
        ),
        CheckConstraint(
            '0.0 <= rating <= 10.0', name='book_rating_range'
        ),
    )

    def __repr__(self):
        return f'{self.title} {self.rating} {self.description}'


class Genre(UUIDMixin, TimeStampMixin, Base):
    """Модель жанра.

    Хранит уникальное название жанра и связь с книгами.
    """

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    genre_books: Mapped[list['BookGenre']] = relationship(
        'BookGenre',
        back_populates='genre',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    def __repr__(self):
        return f'{self.name}'


class BookGenre(TimeStampMixin, Base):
    """Связь книги и жанра (многие-ко-многим).

    Таблица ассоциаций для связи книг и жанров.
    """

    book_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey('book.id', ondelete='CASCADE'),
        primary_key=True
    )
    genre_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey('genre.id', ondelete='CASCADE'),
        primary_key=True
    )
    book: Mapped['Book'] = relationship(
        'Book', back_populates='book_genres'
    )
    genre: Mapped['Genre'] = relationship(
        'Genre', back_populates='genre_books'
    )


class Contributor(UUIDMixin, TimeStampMixin, Base):
    """Модель участника.

    Хранит полное имя автора, редактора или иллюстратора и связи с книгами.
    """

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    book_contributions: Mapped[list['BookContributor']] = relationship(
        'BookContributor',
        back_populates='contributor',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )


class BookContributor(TimeStampMixin, Base):
    """Связь книги и участника (многие-ко-многим с ролью).

    Таблица ассоциаций для связи книги с её участниками и их ролями.
    """

    book_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey('book.id', ondelete='CASCADE'),
        primary_key=True
    )
    contributor_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey('contributor.id', ondelete='CASCADE'),
        primary_key=True
    )
    role: Mapped[ContributorRole] = mapped_column(
        SAEnum(
            ContributorRole,
            name='contributor_role',
            values_callable=lambda e: [m.value for m in e],
            create_type=False,
        ),
        nullable=False,
        default=ContributorRole.AUTHOR,
        primary_key=True
    )
    book: Mapped['Book'] = relationship(
        'Book', back_populates='book_contributors'
    )
    contributor: Mapped['Contributor'] = relationship(
        'Contributor', back_populates='book_contributions'
    )
