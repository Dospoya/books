from pydantic import BaseModel

from src.models import ContributorRole
from src.schemas.base import BaseReadModel


class ContributorLink(BaseReadModel):
    role: ContributorRole
