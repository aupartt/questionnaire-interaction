from fastapi import Depends, Header, HTTPException, status

from app.core.config import settings
from app.service.user_service import UserService


async def verify_api_key(
    api_key: str = Header(..., alias=settings.API_KEY_NAME), service: UserService = Depends(UserService)
) -> int:
    """Vérifie la clé X-API-Key."""

    result = await service.get_user_id(api_key=api_key)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return result
