import logging

from sqlalchemy import select

from app.core.database import get_db
from app.models import SessionDB
from app.schema import SessionModel
from app.schema.common import StatusEnum

logger = logging.getLogger(__name__)


class SessionRepository:
    async def get_session_by_id(self, session_id: int) -> SessionModel | None:
        """Retourne la liste de sessions liées au user_id"""
        async with get_db() as session:
            stmt = select(SessionDB).where(SessionDB.id == session_id)
            result = await session.execute(stmt)
            db_sessions = result.scalar_one_or_none()

            if db_sessions is not None:
                return SessionModel.model_validate(db_sessions)

            return None

    async def get_sessions(self, user_id: int) -> list[SessionModel]:
        """Retourne la liste de sessions liées au user_id"""
        async with get_db() as session:
            stmt = select(SessionDB).where(SessionDB.user_id == user_id)
            results = await session.execute(stmt)
            db_sessions = results.scalars().all()
            return [SessionModel.model_validate(s) for s in db_sessions]

    async def get_session_questionnaire(self, user_id: int, questionnaire_id: int) -> SessionModel | None:
        """Retourne la session pour le questionnaire si elle existe
        Sinon crée une nouvelle session et la retourne"""
        async with get_db() as session:
            try:
                stmt = select(SessionDB).where(
                    SessionDB.user_id == user_id,
                    SessionDB.questionnaire_id == questionnaire_id,
                )
                result = await session.execute(stmt)
                db_session = result.scalar_one_or_none()

                if db_session is not None:
                    return SessionModel.model_validate(db_session)

                new_session = SessionDB(questionnaire_id=questionnaire_id, user_id=user_id, status=StatusEnum.ACTIVE)
                session.add(new_session)
                await session.commit()
                await session.refresh(new_session)
                return SessionModel.model_validate(new_session)

            except Exception as e:
                logger.error(
                    f"Failed to get session {e}",
                )
                await session.rollback()

    async def update_status(self, session_id: int, status: StatusEnum) -> None:
        """Mets à jours le status d'une Session"""
        async with get_db() as session:
            try:
                stmt = select(SessionDB).where(SessionDB.id == session_id)
                result = await session.execute(stmt)
                db_session = result.scalar_one_or_none()

                if db_session is not None:
                    db_session.status = status
                    session.add(db_session)
                    await session.commit()

            except Exception as e:
                logger.error(
                    f"Impossible de mettre à jours la session {e}",
                )
                await session.rollback()
