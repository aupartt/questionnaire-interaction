from pydantic import BaseModel, ConfigDict

from app.schema.common import StatusEnum


class AnswerModel(BaseModel):
    id: int | None
    session_id: int
    item_id: int
    value: str | dict | None
    status: StatusEnum

    model_config = ConfigDict(from_attributes=True)


class Answer(BaseModel):
    item_id: int
    value: str | dict | None
    status: StatusEnum

    model_config = ConfigDict(from_attributes=True)
