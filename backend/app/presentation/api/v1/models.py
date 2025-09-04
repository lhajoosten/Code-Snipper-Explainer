from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ExplainCodeRequest(BaseModel):
    """Request model for code explanation."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,  # Add max_length at Pydantic level
        description="Code to explain",
    )
    language: Optional[str] = Field(
        None,
        max_length=50,  # Reasonable limit for language names
        description="Programming language hint",
    )

    @field_validator("code")
    @classmethod
    def validate_code_content(cls, v: str) -> str:
        """Validate code content."""
        if not v.strip():
            raise ValueError("Code cannot be empty or only whitespace")
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language hint."""
        if v and not v.strip():
            return None  # Convert empty string to None
        return v.lower() if v else None


class ErrorResponse(BaseModel):
    """Standard error response model."""

    type: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")


class RefactorCodeRequest(BaseModel):
    """Request model for code refactoring."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,  # Add max_length at Pydantic level
        description="Code to refactor",
    )
    language: Optional[str] = Field(
        None,
        max_length=50,  # Reasonable limit for language names
        description="Programming language hint",
    )
    goal: Optional[str] = Field(
        None,
        max_length=200,  # Reasonable limit for goal descriptions
        description="Specific refactoring goal or focus area",
    )

    @field_validator("code")
    @classmethod
    def validate_code_content(cls, v: str) -> str:
        """Validate code content."""
        if not v.strip():
            raise ValueError("Code cannot be empty or only whitespace")
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language hint."""
        if v and not v.strip():
            return None  # Convert empty string to None
        return v.lower() if v else None

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: Optional[str]) -> Optional[str]:
        """Validate refactoring goal."""
        if v and not v.strip():
            return None  # Convert empty string to None
        return v


class GenerateTestsRequest(BaseModel):
    """Request model for test generation."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50000,  # Add max_length at Pydantic level
        description="Code to generate tests for",
    )
    language: Optional[str] = Field(
        None,
        max_length=50,  # Reasonable limit for language names
        description="Programming language hint",
    )
    test_framework: Optional[str] = Field(
        None,
        max_length=50,  # Reasonable limit for framework names
        description="Preferred test framework (e.g., pytest, unittest, jest)",
    )

    @field_validator("code")
    @classmethod
    def validate_code_content(cls, v: str) -> str:
        """Validate code content."""
        if not v.strip():
            raise ValueError("Code cannot be empty or only whitespace")
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language hint."""
        if v and not v.strip():
            return None  # Convert empty string to None
        return v.lower() if v else None

    @field_validator("test_framework")
    @classmethod
    def validate_test_framework(cls, v: Optional[str]) -> Optional[str]:
        """Validate test framework."""
        if v and not v.strip():
            return None  # Convert empty string to None
        return v.lower() if v else None
