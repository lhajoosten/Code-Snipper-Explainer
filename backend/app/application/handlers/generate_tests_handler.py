from app.application.dispatch import Handler
from app.application.commands.generate_tests_command import GenerateTestsCommand
from app.application.dto.test_scaffold_result_dto import TestScaffoldResultDTO
from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import AIProviderError, ValidationError
from app.domain.services.code_validation_service import CodeValidationService
import logging

logger = logging.getLogger(__name__)


class GenerateTestsHandler(Handler[GenerateTestsCommand, TestScaffoldResultDTO]):
    """Handler for generating unit tests for code snippets."""

    def __init__(self, ai_provider: AIProvider) -> None:
        """
        Initialize the handler with an AI provider.

        Args:
            ai_provider: The AI provider to use for test generation
        """
        self._ai_provider = ai_provider

    async def handle(self, command: GenerateTestsCommand) -> TestScaffoldResultDTO:
        """
        Handle the generate tests command.

        Args:
            command: The command containing code to generate tests for

        Returns:
            The test scaffold result

        Raises:
            ValidationError: If the command is invalid
            AIProviderError: If the AI service fails
        """
        try:
            logger.info(
                f"Generating tests using {self._ai_provider.provider_name} provider"
            )

            # Create validated code snippet using domain service
            code_snippet = CodeValidationService.create_code_snippet(
                command.code, command.language
            )

            # Get test scaffold from AI provider
            test_scaffold = await self._ai_provider.generate_tests(
                code_snippet, command.test_framework
            )

            # Convert to DTO
            result = TestScaffoldResultDTO(
                test_code=test_scaffold.test_code,
                test_framework=test_scaffold.test_framework,
                test_cases=test_scaffold.test_cases,
                setup_instructions=test_scaffold.setup_instructions,
                line_count=test_scaffold.line_count,
                character_count=test_scaffold.character_count,
                provider=test_scaffold.provider,
                placeholder=test_scaffold.is_placeholder,
            )

            logger.info(
                f"Successfully generated test scaffold using {test_scaffold.provider} provider"
            )
            return result

        except (ValidationError, AIProviderError):
            # Re-raise domain and AI provider errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error in test generation handler: {e}")
            raise AIProviderError(
                f"Failed to process test generation request: {str(e)}"
            ) from e
