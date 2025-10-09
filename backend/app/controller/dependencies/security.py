from fastapi import Depends, Header, HTTPException, status

from app.adapter.user_repository import UserRepository
from app.core.config import settings


async def verify_api_key(
    api_key: str = Header(..., alias=settings.API_KEY_NAME), repo: UserRepository = Depends(UserRepository)
) -> int:
    """Vérifie la clé X-API-Key."""

    user_id = await repo.get_user_id(api_key=api_key)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return user_id
