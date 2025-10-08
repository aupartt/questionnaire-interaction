from pydantic import BaseModel

from app.schema.common import QuestionType, StatusEnum


class ItemContent(BaseModel):
    type: str
    value: str | list[str] | None = None


class ItemQuestion(BaseModel):
    type: QuestionType
    value: str


class ItemModel(BaseModel):
    id: int
    questionnaire_id: int
    name: str
    question: ItemQuestion
    content: ItemContent
    order: int


class Item(BaseModel):
    id: int
    name: str
    question: ItemQuestion
    content: ItemContent


class ItemShort(BaseModel):
    id: int
    name: str


class NextItemResponse(BaseModel):
    next_item: Item | None = None
    result_url: str | None = None
    session_status: StatusEnum
