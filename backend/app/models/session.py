from pydantic import BaseModel

from app.models.common import StatusEnum


class Session(BaseModel):
    id: str
    user_id: str
    questionnaire_id: int
    status: StatusEnum
