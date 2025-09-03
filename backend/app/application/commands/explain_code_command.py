from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExplainCodeCommand:
    """Command to explain a piece of code."""

    code: str
    language: Optional[str] = None
