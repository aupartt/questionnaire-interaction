import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware.api_key_middleware import APIKeyMiddleware

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Questionnaire Interaction api",
    version=settings.api_path_version,
    docs_url=f"{settings.api_base_path}/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(APIKeyMiddleware)


@app.get("/")
def hello():
    return "Hello world !"


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting API on port {settings.api_port}")
    uvicorn.run("main:app", host="0.0.0.0", port=settings.api_port)
