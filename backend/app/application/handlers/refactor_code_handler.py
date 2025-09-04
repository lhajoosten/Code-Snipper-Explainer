from app.application.dispatch import Handler
from app.application.commands.refactor_code_command import RefactorCodeCommand
from app.application.dto.refactor_result_dto import RefactorResultDTO
from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import AIProviderError, ValidationError
from app.domain.services.code_validation_service import CodeValidationService
import logging

logger = logging.getLogger(__name__)


class RefactorCodeHandler(Handler[RefactorCodeCommand, RefactorResultDTO]):
    """Handler for refactoring code snippets."""

    def __init__(self, ai_provider: AIProvider) -> None:
        """
        Initialize the handler with an AI provider.

        Args:
            ai_provider: The AI provider to use for refactoring
        """
        self._ai_provider = ai_provider

    async def handle(self, command: RefactorCodeCommand) -> RefactorResultDTO:
        """
        Handle the refactor code command.

        Args:
            command: The command containing code to refactor

        Returns:
            The refactor result

        Raises:
            ValidationError: If the command is invalid
            AIProviderError: If the AI service fails
        """
        try:
            logger.info(
                f"Refactoring code using {self._ai_provider.provider_name} provider"
            )

            # Create validated code snippet using domain service
            code_snippet = CodeValidationService.create_code_snippet(
                command.code, command.language
            )

            # Get refactor from AI provider
            refactor = await self._ai_provider.refactor_code(code_snippet, command.goal)

            # Convert to DTO
            result = RefactorResultDTO(
                refactored_code=refactor.refactored_code,
                explanation=refactor.explanation,
                improvements=refactor.improvements,
                line_count=refactor.line_count,
                character_count=refactor.character_count,
                provider=refactor.provider,
                placeholder=refactor.is_placeholder,
            )

            logger.info(
                f"Successfully generated refactor using {refactor.provider} provider"
            )
            return result

        except (ValidationError, AIProviderError):
            # Re-raise domain and AI provider errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error in refactor handler: {e}")
            raise AIProviderError(
                f"Failed to process refactor request: {str(e)}"
            ) from e
