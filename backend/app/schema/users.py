from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    api_key: str
