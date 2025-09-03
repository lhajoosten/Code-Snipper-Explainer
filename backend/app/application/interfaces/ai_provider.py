from abc import ABC, abstractmethod

from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.value_objects.code_explanation import CodeExplanation
from app.domain.exceptions import AIProviderError


class AIProvider(ABC):
    """Interface for AI providers that can explain code."""

    @abstractmethod
    async def explain_code(self, code_snippet: CodeSnippet) -> CodeExplanation:
        """
        Explain the given code snippet.

        Args:
            code_snippet: The code snippet to explain

        Returns:
            A code explanation with metadata

        Raises:
            AIProviderError: If the AI service fails
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the AI provider (e.g., 'openai', 'fake')."""
        pass
