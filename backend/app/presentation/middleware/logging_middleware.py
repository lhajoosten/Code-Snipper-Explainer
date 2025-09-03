"""Request logging and correlation middleware."""

import time
import uuid
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and adding correlation IDs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with logging and correlation ID."""
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())

        # Add to request state for use in handlers
        request.state.correlation_id = correlation_id

        # Start timing
        start_time = time.time()

        # Log request
        logger.info(
            "Request started",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "url": str(request.url),
                "user_agent": request.headers.get("user-agent", ""),
                "content_length": request.headers.get("content-length", 0),
            },
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        # Log response
        logger.info(
            "Request completed",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "response_size": response.headers.get("content-length", 0),
            },
        )

        return response
