from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .sessions import Session


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    api_key: Mapped[str] = mapped_column(unique=True)

    # Relations
    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        backref=backref("user"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
