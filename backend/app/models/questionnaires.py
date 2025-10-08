from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .items import Item
    from .sessions import Session


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    order: Mapped[int]

    # Relations
    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        backref=backref("questionnaire"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    items: Mapped[list["Item"]] = relationship(
        "Item",
        backref=backref("questionnaire"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
