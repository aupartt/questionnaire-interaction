from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .answers import AnswerDB


class SessionDB(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relations
    questionnaire_id: Mapped[int] = mapped_column(ForeignKey("questionnaires.id", ondelete="CASCADE"))
    answers: Mapped[list["AnswerDB"]] = relationship(
        "AnswerDB",
        backref=backref("session"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
