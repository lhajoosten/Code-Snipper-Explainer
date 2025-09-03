"""Code validation domain service."""

from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.exceptions import ValidationError


class CodeValidationService:
    """Domain service for validating code-related business rules."""

    # Business rule constants
    MAX_CODE_LENGTH = 50000
    MIN_CODE_LENGTH = 1
    SUSPICIOUS_PATTERNS = [
        # Add patterns for potentially malicious code if needed
        # "eval(", "exec(", etc.
    ]

    @staticmethod
    def validate_code_content(code: str) -> None:
        """Validate code content according to business rules."""
        if not isinstance(code, str):
            raise ValidationError("Code must be a string")

        if not code.strip():
            raise ValidationError("Code cannot be empty")

        if len(code) > CodeValidationService.MAX_CODE_LENGTH:
            raise ValidationError(
                f"Code exceeds maximum length of {CodeValidationService.MAX_CODE_LENGTH} characters"
            )

        # Additional business validations can be added here
        # For example, checking for suspicious patterns, forbidden imports, etc.

    @staticmethod
    def create_code_snippet(code: str, language: str | None = None) -> CodeSnippet:
        """Create a validated code snippet."""
        CodeValidationService.validate_code_content(code)

        # Normalize language hint
        normalized_language = None
        if language:
            normalized_language = language.strip().lower()
            if not normalized_language:
                normalized_language = None

        return CodeSnippet(content=code, language=normalized_language)
