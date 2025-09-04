from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RefactorCodeCommand:
    """Command to refactor a piece of code."""

    code: str
    language: Optional[str] = None
    goal: Optional[str] = None
