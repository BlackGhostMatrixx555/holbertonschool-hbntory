import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    product_api_url: str = os.getenv("PRODUCT_API_URL", "http://localhost:8001")
    backend_internal_url: str = os.getenv("BACKEND_INTERNAL_URL", "http://localhost:8000/internal")
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "change-internal-key")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
