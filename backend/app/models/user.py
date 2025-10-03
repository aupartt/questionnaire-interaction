from app.models.common import StatusEnum
from pydantic import BaseModel


class User(BaseModel):
    id: int
    status: StatusEnum
