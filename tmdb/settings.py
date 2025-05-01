from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Máster EOI - API wrapper Public API"
    api_key: str


settings = Settings()