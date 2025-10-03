from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Схема ответа для эндпоинта /ping."""

    status: str = 'ok'
