from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.valid_keys = [settings.MOCK_API_KEY]
        self.excluded_paths = [
            f"{settings.api_base_path}/docs",
            "/redoc",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.excluded_paths:
            response = await call_next(request)
            return response

        api_key = request.headers.get(settings.API_KEY_NAME)
        if not api_key or api_key not in self.valid_keys:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        request.state.api_key = api_key
        response = await call_next(request)
        return response
