from pydantic import BaseModel

from app.models.common import StatusEnum


class User(BaseModel):
    id: str
    status: StatusEnum
