from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.valid_keys = ["test-api-key"]

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key not in self.valid_keys:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        request.state.user_api_key = api_key
        response = await call_next(request)
        return response
