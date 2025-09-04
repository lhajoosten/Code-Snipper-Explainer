from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GenerateTestsCommand:
    """Command to generate unit tests for a piece of code."""

    code: str
    language: Optional[str] = None
    test_framework: Optional[str] = None
