from fastapi import Depends

from app.adapter.user_repository import UserRepository
from app.schema.common import VerifyResult


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)):
        self.user_repo = user_repo

    async def verify_api_key(self, api_key: str) -> VerifyResult:
        """Vérifie si la clé API est bien rattaché à un utilisateur."""
        user_id = await self.user_repo.get_user_by_key(api_key=api_key)
        return VerifyResult(is_valid=bool(user_id))

    async def get_user_id(self, api_key: str) -> int | None:
        """Récupère un utilisateur avec la clé api et retourne son ID"""
        user = await self.user_repo.get_user_by_key(api_key=api_key)
        if user is not None:
            return user.id
