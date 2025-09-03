from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CodeSnippet:
    """Domain entity representing a piece of code to be analyzed."""

    content: str
    language: Optional[str] = None

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError("Code content cannot be empty")

    @property
    def line_count(self) -> int:
        """Calculate the number of lines in the code snippet."""
        return self.content.count("\n") + 1 if self.content else 0

    @property
    def character_count(self) -> int:
        """Calculate the number of characters in the code snippet."""
        return len(self.content)
