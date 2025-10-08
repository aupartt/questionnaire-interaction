from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


class Item(BaseModel):
    id: int
    name: str
    question: ItemQuestion
    content: ItemContent

    model_config = ConfigDict(from_attributes=True)


class ItemShort(BaseModel):
    id: int
    name: str


class NextItemResponse(BaseModel):
    next_item: Item | None = None
    result_url: str | None = None
    session_status: StatusEnum
