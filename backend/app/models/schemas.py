from datetime import datetime

from pydantic import BaseModel

from app.models.common import QuestionType, StatusEnum


class Questionnaire(BaseModel):
    id: str
    name: str
    description: str
    order: int


class QuestionnaireStatus(Questionnaire):
    session_id: str | None = None
    status: StatusEnum | None = None
    is_next: bool = False


class ItemContent(BaseModel):
    type: str
    likert_value: list[str] | None = None


class ItemQuestion(BaseModel):
    type: QuestionType
    text: str
    value: str


class Item(BaseModel):
    id: str
    questionnaire_id: str
    name: str  # Permet d'afficher du texte même si la question est de type media
    question: ItemQuestion
    content: ItemContent
    order: int


class Session(BaseModel):
    id: str
    questionnaire_id: str
    api_key: str  # TODO: créer un User ?
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    id: str
    session_id: str
    item_id: str
    value: str | dict
