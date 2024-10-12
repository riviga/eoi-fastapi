from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Máster EOI - FastAPI API wrapper Public API"
    api_key: str


settings = Settings()