import logging

from sqlalchemy import select

from app.core.database import get_db
from app.models import QuestionnaireDB
from app.schema import QuestionnaireModel

logger = logging.getLogger(__name__)


class QuestionnaireRepository:
    async def get_questionnaires(self) -> list[QuestionnaireModel]:
        """Retourne la liste de questionnaires dans l'ordre de passage."""
        async with get_db() as session:
            stmt = select(QuestionnaireDB).order_by(QuestionnaireDB.order)
            result = await session.execute(stmt)
            db_questionnaires = result.scalars().all()
            return [QuestionnaireModel.model_validate(q) for q in db_questionnaires]

    async def get_questionnaire_by_id(self, questionnaire_id: str) -> QuestionnaireModel | None:
        """Retourne un questionnaire par son ID"""
        async with get_db() as session:
            stmt = select(QuestionnaireDB).where(QuestionnaireDB.id == questionnaire_id)
            result = await session.execute(stmt)
            questionnaire = result.scalar_one_or_none()

            if questionnaire is not None:
                return QuestionnaireModel.model_validate(questionnaire)

            return None
