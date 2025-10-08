from datetime import datetime

from pydantic import BaseModel

from app.models.common import QuestionType, ResultStatus, StatusEnum


class QuestionnaireModel(BaseModel):
    id: int
    name: str
    description: str
    order: int


class QuestionnaireStatus(BaseModel):
    id: int
    name: str
    description: str
    session_id: int | None = None
    status: StatusEnum | None = None
    is_next: bool = False


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


class SessionModel(BaseModel):
    id: int
    questionnaire_id: int
    api_key: str  # TODO: créer un User ?
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


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


class NextItemResponse(BaseModel):
    next_item: Item | None = None
    result_url: str | None = None
    session_status: StatusEnum


class Session(BaseModel):
    id: int
    questionnaire_id: int
    items: list[ItemShort]
    answers: list[Answer]
    current_item: Item


class Result(BaseModel):
    status: ResultStatus
    message: str


class VerifyResult(BaseModel):
    is_valid: bool
