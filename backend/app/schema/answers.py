from pydantic import BaseModel

from app.schema.common import StatusEnum


class AnswerModel(BaseModel):
    id: int | None
    session_id: int
    item_id: int
    value: str | dict | None
    status: StatusEnum

    class model_config:
        from_attributes = True


class Answer(BaseModel):
    item_id: int
    value: str | dict | None
    status: StatusEnum
