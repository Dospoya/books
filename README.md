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


## Запуск через Docker Compose
```
# сборка и старт
docker compose up -d --build

# применить миграции внутри контейнера api
docker compose exec api alembic upgrade head
```


## API

Базовый префикс: /api
Swagger: http://localhost:8000/docs

### HealthCheck
```
GET /api/ping
```

Пример:
```
curl -s http://localhost:8000/api/ping
# {"status":"ok"}
```

### Список книг
```
GET /api/v1/books
```

Параметры запроса:
- page — номер страницы (>=1), по умолчанию 1
- page_size — размер страницы [1..100], по умолчанию 10
- sort — поле сортировки: title|rating|published_year (по умолчанию title)
- order — порядок: asc|desc (по умолчанию asc)
- q — подстрока в названии (поиск по title)
- genre_id — UUID жанра
- published_year — год публикации
- rating_min, rating_max — диапазон рейтинга (0.0..10.0)

Ответ:
```
{
  "items": [
    {
      "title": "The Lord of the Rings",
      "rating": 9.3,
      "description": "…",
      "published_year": 1954
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

Примеры запросов:
```
# Базовый запрос (первая страница, 10 элементов)
curl -G "http://localhost:8000/api/v1/books"

# Поиск по подстроке в названии + сортировка по рейтингу (DESC)
curl -G "http://localhost:8000/api/v1/books" \
  --data-urlencode "q=ring" \
  --data-urlencode "sort=rating" \
  --data-urlencode "order=desc"

# Фильтр по жанру и году публикации + пагинация
curl -G "http://localhost:8000/api/v1/books" \
  --data-urlencode "genre_id=<UUID-жанра>" \
  --data-urlencode "published_year=2021" \
  --data-urlencode "page=2" \
  --data-urlencode "page_size=5"

# Диапазон рейтинга
curl -G "http://localhost:8000/api/v1/books" \
  --data-urlencode "rating_min=7.5" \
  --data-urlencode "rating_max=9.0"
```
