from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseReadModel(BaseModel):
    """Базовая схема для сущностей с полем id."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
