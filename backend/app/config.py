from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Const
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEV
    API_KEY_MOCK: str = "foo"
    API_KEY_NAME: str = "X-API-Key"

    # Base app settings
    API_BASE_PATH: str = "/api/v1"
    API_BASE_VERSION: str = "v1"
    API_PORT: int = 8090
    FRONT_URL: str = "*"

    # Postgres
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "questionnaire"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
