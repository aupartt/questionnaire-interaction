from pydantic import BaseModel

from app.schema.common import StatusEnum


class AnswerModel(BaseModel):
    id: int
    session_id: int
    item_id: int
    value: str | dict | None
    status: StatusEnum


class Answer(BaseModel):
    item_id: int
    value: str | dict | None
    status: StatusEnum
