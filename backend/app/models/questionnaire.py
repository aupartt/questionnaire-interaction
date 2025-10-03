from pydantic import BaseModel


class Questionnaire(BaseModel):
    id: str
    name: str
    description: str
    order: int
