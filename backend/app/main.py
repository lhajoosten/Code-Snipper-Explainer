from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.v1 import explain, refactor, tests
from app.presentation.middleware.logging_middleware import RequestLoggingMiddleware
from app.presentation.exception_handlers import (
    domain_error_handler,
    validation_error_handler,
    ai_provider_error_handler,
    general_exception_handler,
)
from app.domain.exceptions import DomainError, ValidationError, AIProviderError
from app.infrastructure.settings import settings
import logging
from datetime import datetime, timezone


# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Register exception handlers
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(AIProviderError, ai_provider_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(explain.router, prefix="/api/v1", tags=["explain"])
app.include_router(refactor.router, prefix="/api/v1", tags=["refactor"])
app.include_router(tests.router, prefix="/api/v1", tags=["tests"])


@app.get("/health")
async def health_check():
    """Enhanced health check endpoint."""
    return {
        "status": "healthy",
        "api_version": settings.api_version,
        "ai_provider": settings.ai_provider,
        "environment": "development" if settings.debug is True else "production",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ping")
async def ping():
    """Health check endpoint."""
    from datetime import datetime

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.api_version,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": settings.api_description,
        "version": settings.api_version,
        "docs": "/docs",
    }
