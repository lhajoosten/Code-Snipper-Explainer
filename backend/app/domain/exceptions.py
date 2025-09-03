"""Domain and application exceptions."""


class DomainError(Exception):
    """Base domain exception."""

    pass


class ValidationError(DomainError):
    """Raised when domain validation fails."""

    pass


class AIProviderError(Exception):
    """Base exception for AI provider issues."""

    pass


class AIProviderTimeoutError(AIProviderError):
    """Raised when AI provider times out."""

    pass


class AIProviderQuotaError(AIProviderError):
    """Raised when AI provider quota is exceeded."""

    pass


class CodeTooLargeError(ValidationError):
    """Raised when code exceeds maximum allowed size."""

    def __init__(self, actual_size: int, max_size: int):
        self.actual_size = actual_size
        self.max_size = max_size
        super().__init__(f"Code size {actual_size} exceeds maximum {max_size}")
