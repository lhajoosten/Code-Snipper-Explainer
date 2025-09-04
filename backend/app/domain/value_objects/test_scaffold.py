"""Test scaffold value object."""

from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.code_snippet import CodeSnippet


@dataclass(frozen=True)
class TestScaffold:
    """Domain entity representing a generated test scaffold."""

    original_snippet: CodeSnippet
    test_code: str
    test_framework: str
    test_cases: list[str]
    setup_instructions: Optional[str]
    provider: str
    is_placeholder: bool = False

    def __post_init__(self):
        if not self.test_code.strip():
            raise ValueError("Test code cannot be empty")

        if not self.test_framework.strip():
            raise ValueError("Test framework cannot be empty")

        if not self.test_cases:
            raise ValueError("At least one test case must be specified")

    @property
    def line_count(self) -> int:
        """Calculate the number of lines in the test code."""
        return self.test_code.count("\n") + 1 if self.test_code else 0

    @property
    def character_count(self) -> int:
        """Calculate the number of characters in the test code."""
        return len(self.test_code)
