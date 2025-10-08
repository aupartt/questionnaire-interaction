from pydantic import BaseModel

from app.schema.common import StatusEnum


class QuestionnaireModel(BaseModel):
    id: int
    name: str
    description: str
    order: int

    class model_config:
        from_attributes = True


class QuestionnaireStatus(BaseModel):
    id: int
    name: str
    description: str
    session_id: int | None = None
    status: StatusEnum | None = None
    is_next: bool = False
