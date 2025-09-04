from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    # API Settings
    api_title: str = "AI Code Assistant"
    api_description: str = "AI-powered code explanation and analysis"
    api_version: str = "1.0.0"
    debug: bool = True

    # AI Provider Settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    ai_provider: str = "openai"
    ai_timeout: int = 60

    # Application Settings
    max_code_length: int = 50000
    log_level: str = "INFO"
    request_timeout: int = 30

    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["*"]

    @field_validator("ai_provider")
    @classmethod
    def validate_ai_provider(cls, v: str) -> str:
        if v != "openai":
            raise ValueError("Only 'openai' is supported as ai_provider")
        return v

    @model_validator(mode="after")
    def validate_openai_key(self) -> "Settings":
        if not self.openai_api_key:
            raise ValueError("openai_api_key is required")
        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
