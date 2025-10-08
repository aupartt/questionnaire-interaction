import logging

from sqlalchemy import select

from app.core.database import get_db
from app.models import ItemDB
from app.schema import Item

logger = logging.getLogger(__name__)


class ItemRepository:
    async def get_items(self, questionnaire_id: int) -> list[Item]:
        """Retourne la liste d'item pour un questionnaire dans l'ordre"""
        async with get_db() as session:
            stmt = select(ItemDB).where(ItemDB.questionnaire_id == questionnaire_id)
            results = await session.execute(stmt)
            db_items = results.scalars().all()
            return [Item.model_validate(i) for i in db_items]
