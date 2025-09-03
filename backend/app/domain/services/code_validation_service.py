"""Code validation domain service."""

from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.exceptions import ValidationError


class CodeValidationService:
    """Domain service for validating code-related business rules."""

    @staticmethod
    def validate_code_content(code: str) -> None:
        """Validate code content according to business rules."""
        if not isinstance(code, str):
            raise ValidationError("Code must be a string")

        if not code.strip():
            raise ValidationError("Code cannot be empty")

        # Add more business validation rules as needed
        # e.g., max length, forbidden patterns, etc.

    @staticmethod
    def create_code_snippet(code: str, language: str | None = None) -> CodeSnippet:
        """Create a validated code snippet."""
        CodeValidationService.validate_code_content(code)
        return CodeSnippet(content=code, language=language)
