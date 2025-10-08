from pydantic import BaseModel, ConfigDict

from app.schema.answers import Answer
from app.schema.common import StatusEnum
from app.schema.items import Item, ItemShort


class SessionModel(BaseModel):
    id: int | None
    questionnaire_id: int
    user_id: int
    status: StatusEnum

    model_config = ConfigDict(from_attributes=True)


class Session(BaseModel):
    id: int
    questionnaire_id: int
    items: list[ItemShort]
    answers: list[Answer]
    current_item: Item
