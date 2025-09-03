from pydantic import BaseModel, Field, validator
from typing import Optional


class ExplainCodeRequest(BaseModel):
    """Request model for code explanation."""

    code: str = Field(..., min_length=1, description="Code to explain")
    language: Optional[str] = Field(None, description="Programming language hint")

    @validator("code")
    def validate_code_length(cls, v):
        from app.infrastructure.settings import settings

        if len(v) > settings.max_code_length:
            from app.domain.exceptions import CodeTooLargeError

            raise CodeTooLargeError(len(v), settings.max_code_length)
        return v


class ErrorResponse(BaseModel):
    """Standard error response model."""

    type: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")
