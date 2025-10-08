import logging

from fastapi import Depends
from sqlalchemy import select

from app.adapter.session_repository import SessionRepository
from app.core.database import get_db
from app.models import AnswerDB
from app.schema import Answer
from app.schema.common import Result, ResultStatus, StatusEnum

logger = logging.getLogger(__name__)


class AnswerRepository:
    def __init__(self, repo: SessionRepository = Depends(SessionRepository)) -> None:
        self.repo = repo

    async def get_answers(self, session_id: int) -> list[Answer]:
        """Retourne toutes les réponse liées à une session"""
        async with get_db() as session:
            stmt = select(AnswerDB).where(AnswerDB.session_id == session_id)
            results = await session.execute(stmt)
            db_answers = results.scalars().all()
            return [Answer.model_validate(a) for a in db_answers]

    async def save_answer(self, session_id: int, answer: Answer, session_status: StatusEnum | None) -> Result:
        """Sauvegarde la réponse et update le status de la session"""
        q_session = await self.repo.get_session_by_id(session_id)

        if q_session is None:
            logger.warning(f"La session {session_id} n'existe pas.")
            return Result(status=ResultStatus.ERROR, message="ID de session introuvable")

        try:
            async with get_db() as session:
                new_answer = AnswerDB(
                    session_id=session_id,
                    item_id=answer.item_id,
                    value=answer.value,
                    status=answer.status,
                )

                session.add(new_answer)
                await session.commit()
                await session.refresh(new_answer)

            if session_status is not None:
                await self.repo.update_status(session_id, session_status)

        except Exception as e:
            logger.error(
                f"Failed to save answer {e}",
            )
            await session.rollback()
