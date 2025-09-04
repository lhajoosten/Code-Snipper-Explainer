from abc import ABC, abstractmethod
from typing import Optional

from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.value_objects.code_explanation import CodeExplanation
from app.domain.value_objects.code_refactor import CodeRefactor
from app.domain.value_objects.test_scaffold import TestScaffold
from app.domain.exceptions import AIProviderError


class AIProvider(ABC):
    """Interface for AI providers that can explain, refactor, and generate tests for code."""

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

    @abstractmethod
    async def refactor_code(
        self, code_snippet: CodeSnippet, goal: Optional[str] = None
    ) -> CodeRefactor:
        """
        Suggest refactoring for the given code snippet.

        Args:
            code_snippet: The code snippet to refactor
            goal: Optional specific refactoring goal

        Returns:
            A code refactor suggestion with metadata

        Raises:
            AIProviderError: If the AI service fails
        """
        pass

    @abstractmethod
    async def generate_tests(
        self, code_snippet: CodeSnippet, test_framework: Optional[str] = None
    ) -> TestScaffold:
        """
        Generate unit test scaffold for the given code snippet.

        Args:
            code_snippet: The code snippet to generate tests for
            test_framework: Optional test framework preference

        Returns:
            A test scaffold with metadata

        Raises:
            AIProviderError: If the AI service fails
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the AI provider (e.g., 'openai', 'fake')."""
        pass
