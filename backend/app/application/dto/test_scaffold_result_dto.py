from pydantic import BaseModel
from typing import List, Optional


class TestScaffoldResultDTO(BaseModel):
    """DTO for test generation result."""

    test_code: str
    test_framework: str
    test_cases: List[str]
    setup_instructions: Optional[str]
    line_count: int
    character_count: int
    provider: str
    placeholder: bool
