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


class Item(BaseModel):
    id: str
    questionnaire_id: str
    question_type: QuestionType  # Permettra de choisir entre text ou media
    question: str  # Question ou url
    item_content: ItemContent
    order: int


class Session(BaseModel):
    id: str
    questionnaire_id: str
    api_key: str
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    id: str
    session_id: str
    item_id: str
    value: str | dict
