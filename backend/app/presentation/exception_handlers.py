from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.domain.exceptions import (
    DomainError,
    ValidationError,
    AIProviderError,
    CodeTooLargeError,
)
from app.presentation.api.v1.models import ErrorResponse
import logging

logger = logging.getLogger(__name__)


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    """Handle domain layer errors."""
    logger.warning(f"Domain error: {exc}")

    error_response = ErrorResponse(type="domain_error", message=str(exc))

    return JSONResponse(status_code=400, content=error_response.dict())


async def validation_error_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc}")

    details = None
    if isinstance(exc, CodeTooLargeError):
        details = {"actual_size": exc.actual_size, "max_size": exc.max_size}

    error_response = ErrorResponse(
        type="validation_error", message=str(exc), details=details
    )

    return JSONResponse(status_code=422, content=error_response.dict())


async def ai_provider_error_handler(
    request: Request, exc: AIProviderError
) -> JSONResponse:
    """Handle AI provider errors."""
    logger.error(f"AI provider error: {exc}")

    error_response = ErrorResponse(
        type="ai_provider_error", message="AI service temporarily unavailable"
    )

    return JSONResponse(status_code=503, content=error_response.dict())


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    error_response = ErrorResponse(
        type="internal_error", message="An unexpected error occurred"
    )

    return JSONResponse(status_code=500, content=error_response.dict())
