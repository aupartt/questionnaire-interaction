from app.models.common import StatusEnum
from pydantic import BaseModel


class Session(BaseModel):
    id: int
    user_id: int
    questionnaire_id: int
    status: StatusEnum
