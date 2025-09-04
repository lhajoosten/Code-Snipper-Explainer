from pydantic import BaseModel
from typing import List


class RefactorResultDTO(BaseModel):
    """DTO for refactor code result."""

    refactored_code: str
    explanation: str
    improvements: List[str]
    line_count: int
    character_count: int
    provider: str
    placeholder: bool
