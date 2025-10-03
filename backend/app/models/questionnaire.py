from pydantic import BaseModel


class Questionnaire(BaseModel):
    id: int
    name: str
    description: str
    order: int
