from datetime import datetime

from pydantic import BaseModel

from app.models.common import QuestionType, ResultStatus, StatusEnum


class QuestionnaireModel(BaseModel):
    id: str
    name: str
    description: str
    order: int


class QuestionnaireStatus(BaseModel):
    id: str
    name: str
    description: str
    session_id: str | None = None
    status: StatusEnum | None = None
    is_next: bool = False


class ItemContent(BaseModel):
    type: str
    likert_value: list[str] | None = None


class ItemQuestion(BaseModel):
    type: QuestionType
    value: str


class ItemModel(BaseModel):
    id: str
    questionnaire_id: str
    name: str  # Permet d'afficher du texte même si la question est de type media
    question: ItemQuestion
    content: ItemContent
    order: int


class Item(BaseModel):
    id: str
    name: str
    question: ItemQuestion
    content: ItemContent


class ItemShort(BaseModel):
    id: str
    name: str


class SessionModel(BaseModel):
    id: str
    questionnaire_id: str
    api_key: str  # TODO: créer un User ?
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class AnswerModel(BaseModel):
    id: str
    session_id: str
    item_id: str
    value: str | dict | None
    status: StatusEnum


class Answer(BaseModel):
    item_id: str
    value: str | dict | None
    status: StatusEnum


class NextItemResponse(BaseModel):
    next_item: Item | None = None
    result_url: str | None = None
    session_status: StatusEnum


class Session(BaseModel):
    id: str
    questionnaire_id: str
    items: list[ItemShort]
    answers: list[Answer]
    current_item: Item


class Result(BaseModel):
    status: ResultStatus
    message: str
