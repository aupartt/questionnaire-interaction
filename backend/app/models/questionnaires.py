from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .items import ItemDB
    from .sessions import SessionDB


class QuestionnaireDB(Base):
    __tablename__ = "questionnaires"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    order: Mapped[int]

    # Relations
    sessions: Mapped[list["SessionDB"]] = relationship(
        "Session",
        backref=backref("questionnaire"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    items: Mapped[list["ItemDB"]] = relationship(
        "Item",
        backref=backref("questionnaire"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
