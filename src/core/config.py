from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    """Глобальные настройки приложения.

    Читает значения из переменных окружения и файла .env.
    """
    app_title: str = 'Book Catalog'

    database_url: str = 'DATABASE_URL'
    api_url: str = 'http://localhost:8000'

    postgres_user: str = 'user'
    postgres_password: str = 'pass'
    postgres_db: str = 'db_name'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
