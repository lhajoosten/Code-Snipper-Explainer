from pydantic import BaseModel


class ExplainResultDTO(BaseModel):
    """Data transfer object for code explanation results."""

    explanation: str
    line_count: int
    character_count: int
    provider: str
    placeholder: bool = False

    class Config:
        frozen = True
