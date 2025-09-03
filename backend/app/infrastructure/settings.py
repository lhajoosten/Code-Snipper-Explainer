from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    # API Settings
    app_name: str = "Code Snippet Explainer"
    app_version: str = "0.1.0"
    debug: bool = False

    # AI Provider Settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    ai_provider: str = "fake"  # "fake" or "openai"

    # Request Limits
    max_code_length: int = 50000
    request_timeout: int = 30

    # CORS Settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("ai_provider")
    @classmethod
    def validate_ai_provider(cls, v: str) -> str:
        allowed = ["fake", "openai"]
        if v not in allowed:
            raise ValueError(f"ai_provider must be one of {allowed}")
        return v

    @model_validator(mode="after")
    def validate_openai_key(self) -> "Settings":
        if self.ai_provider == "openai" and not self.openai_api_key:
            raise ValueError("openai_api_key is required when ai_provider is 'openai'")
        return self

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
