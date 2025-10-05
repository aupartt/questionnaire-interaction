from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Const
    API_KEY_NAME: str = "QUESTIONNAIRE_API_KEY"
    MOCK_API_KEY: str = "bestapikey123"

    # Base app settings
    api_base_path: str = "/api/v1"
    api_path_version: str = "v1"
    api_port: int = 8090


settings = Settings()
