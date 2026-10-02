import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Agentic Fulfillment Recovery Planner"
    api_prefix: str = "/api"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    database_url: str = "sqlite://"
    redis_url: str = "redis://localhost:6379/0"
    chroma_persist_directory: str = str(BASE_DIR / "app" / "data" / "chroma")
    app_env: str = Field(
        default_factory=lambda: "production" if os.getenv("VERCEL") == "1" else "development"
    )
    clerk_issuer: str | None = None
    clerk_jwks_url: str | None = None
    clerk_approver_roles: str = "org:admin"
    frontend_origin: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
