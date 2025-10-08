from pydantic import BaseModel, ConfigDict

from app.schema.common import StatusEnum


class QuestionnaireModel(BaseModel):
    id: int
    name: str
    description: str
    order: int

    model_config = ConfigDict(from_attributes=True)


class QuestionnaireStatus(BaseModel):
    id: int
    name: str
    description: str
    session_id: int | None = None
    status: StatusEnum | None = None
    is_next: bool = False
