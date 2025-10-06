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

    # Base app settings
    API_BASE_PATH: str = "/api/v1"
    API_BASE_VERSION: str = "v1"
    API_PORT: int = 8090
    FRONT_URL: str = "*"


settings = Settings()
