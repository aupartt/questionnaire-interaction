from datetime import datetime

from pydantic import BaseModel

from app.schema.answers import Answer
from app.schema.common import StatusEnum
from app.schema.items import Item, ItemShort


class SessionModel(BaseModel):
    id: int
    questionnaire_id: int
    api_key: str
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class Session(BaseModel):
    id: int
    questionnaire_id: int
    items: list[ItemShort]
    answers: list[Answer]
    current_item: Item
