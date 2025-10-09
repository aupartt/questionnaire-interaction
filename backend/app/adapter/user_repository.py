import logging

from sqlalchemy import select

from app.core.database import get_db
from app.models import UserDB

logger = logging.getLogger(__name__)


class UserRepository:
    async def get_user_id(self, api_key: str) -> int | None:
        """Retourne un utilisateur par clé API"""
        async with get_db() as session:
            stmt = select(UserDB.id).where(UserDB.api_key == api_key)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
