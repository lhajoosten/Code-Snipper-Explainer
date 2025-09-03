from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExplainCodeCommand:
    """Command to explain a piece of code."""

    code: str
    language: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.code, str):
            raise TypeError("Code must be a string")
        if not self.code.strip():
            raise ValueError("Code cannot be empty")
