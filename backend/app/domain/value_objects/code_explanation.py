from dataclasses import dataclass

from app.domain.value_objects.code_snippet import CodeSnippet


@dataclass(frozen=True)
class CodeExplanation:
    """Domain entity representing an explanation of code."""

    snippet: CodeSnippet
    explanation: str
    provider: str
    is_placeholder: bool = False

    def __post_init__(self):
        if not self.explanation.strip():
            raise ValueError("Explanation cannot be empty")
