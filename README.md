Books Catalog (FastAPI + PostgreSQL)

Сервис каталога книг с фильтрацией, сортировкой и пагинацией.
Стек: Python 3.10+, FastAPI, SQLAlchemy 2.0 ORM, PostgreSQL, Pydantic v2, Alembic, pytest.


## Требования
- Python 3.10+
- Docker + Docker Compose


## Переменные окружения
Создай файл .env в корне проекта:
```
  # PostgreSQL
  POSTGRES_USER=user
  POSTGRES_PASSWORD=pass
  POSTGRES_DB=booksdb

  # База данных для sqlalchemy
  DATABASE_URL="postgresql+asyncpg://user:pass@db:5432/booksdb"

  # Приложение
  API_URL=http://localhost:8000
```
