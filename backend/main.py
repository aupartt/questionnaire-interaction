import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.controller import questionnaire_controller
from app.middleware.api_key_middleware import APIKeyMiddleware

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Questionnaire Interaction api",
    version=settings.API_BASE_VERSION,
    docs_url=f"{settings.API_BASE_PATH}/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(APIKeyMiddleware)

app.include_router(questionnaire_controller.router, prefix=settings.API_BASE_PATH)


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting API on port {settings.API_PORT}")
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT)
