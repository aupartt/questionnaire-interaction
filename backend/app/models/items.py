from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .answers import Answer


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    question: Mapped[dict]
    content: Mapped[dict]
    order: Mapped[int]

    # Relations
    questionnaire_id: Mapped[int] = mapped_column(ForeignKey("questionnaires.id", ondelete="CASCADE"))
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        backref=backref("item"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
