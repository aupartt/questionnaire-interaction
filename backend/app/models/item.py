from enum import Enum

from pydantic import BaseModel


class ItemType(Enum):
    TEXT = "text"


class Item(BaseModel):
    id: str
    type: ItemType
    question: str
    order: int
