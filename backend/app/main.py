from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.v1 import explain
from app.presentation.exception_handlers import (
    domain_error_handler,
    validation_error_handler,
    ai_provider_error_handler,
    general_exception_handler,
)
from app.domain.exceptions import DomainError, ValidationError, AIProviderError
from app.infrastructure.settings import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
    handlers=[logging.StreamHandler()],
)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
)

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


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


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
