import logging

from sqlalchemy import select

from app.core.database import get_db
from app.models import UserDB
from app.schema.users import User

logger = logging.getLogger(__name__)


class UserRepository:
    async def get_user_by_key(self, api_key: str) -> User | None:
        """Retourne un utilisateur par clé API"""
        async with get_db() as session:
            stmt = select(UserDB).where(UserDB.api_key == api_key)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()

            if db_user is not None:
                return User.model_validate(db_user)

            return None
