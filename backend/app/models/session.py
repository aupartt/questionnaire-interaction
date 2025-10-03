from pydantic import BaseModel

from app.models.common import StatusEnum


class Session(BaseModel):
    id: str
    user_id: int
    questionnaire_id: int
    status: StatusEnum
