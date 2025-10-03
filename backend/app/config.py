from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_base_path: str = "/api/v1"
    api_path_version: str = "v1"
    api_port: int = 8090


settings = Settings()
