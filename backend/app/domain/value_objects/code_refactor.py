"""Code refactor value object."""

from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.code_snippet import CodeSnippet


@dataclass(frozen=True)
class CodeRefactor:
    """Domain entity representing a code refactoring suggestion."""

    original_snippet: CodeSnippet
    refactored_code: str
    explanation: str
    improvements: list[str]
    provider: str
    is_placeholder: bool = False

    def __post_init__(self):
        if not self.refactored_code.strip():
            raise ValueError("Refactored code cannot be empty")

        if not self.explanation.strip():
            raise ValueError("Refactoring explanation cannot be empty")

        if not self.improvements:
            raise ValueError("At least one improvement must be specified")

    @property
    def line_count(self) -> int:
        """Calculate the number of lines in the refactored code."""
        return self.refactored_code.count("\n") + 1 if self.refactored_code else 0

    @property
    def character_count(self) -> int:
        """Calculate the number of characters in the refactored code."""
        return len(self.refactored_code)
