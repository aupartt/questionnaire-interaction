from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import EnvironmentType, settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.valid_keys = []

        if settings.ENVIRONMENT == EnvironmentType.DEV:
            self.valid_keys.append(settings.API_KEY_MOCK)

        self.excluded_paths = [
            f"{settings.API_BASE_PATH}/docs",
            "/redoc",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response

        if request.url.path in self.excluded_paths:
            response = await call_next(request)
            return response

        try:
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key not in self.valid_keys:
                raise HTTPException(status_code=401, detail="Invalid API Key")

            request.state.api_key = api_key
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
