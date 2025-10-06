from fastapi import Header, HTTPException, status

from app.config import EnvironmentType, settings


async def verify_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Vérifie la clé X-API-Key."""

    valid_keys = []
    if settings.ENVIRONMENT == EnvironmentType.DEV:
        valid_keys.append(settings.API_KEY_MOCK)

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return api_key
