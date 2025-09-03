from app.application.dispatch import Handler
from app.application.commands.explain_code_command import ExplainCodeCommand
from app.application.dto.explain_result_dto import ExplainResultDTO
from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import AIProviderError, ValidationError
from app.domain.services.code_validation_service import CodeValidationService
import logging

logger = logging.getLogger(__name__)


class ExplainCodeHandler(Handler[ExplainCodeCommand, ExplainResultDTO]):
    """Handler for explaining code snippets."""

    def __init__(self, ai_provider: AIProvider) -> None:
        """
        Initialize the handler with an AI provider.

        Args:
            ai_provider: The AI provider to use for explanations
        """
        self._ai_provider = ai_provider

    async def handle(self, command: ExplainCodeCommand) -> ExplainResultDTO:
        """
        Handle the explain code command.

        Args:
            command: The command containing code to explain

        Returns:
            The explanation result

        Raises:
            ValidationError: If the command is invalid
            AIProviderError: If the AI service fails
        """
        try:
            logger.info(
                f"Explaining code using {self._ai_provider.provider_name} provider"
            )

            # Create validated code snippet using domain service
            code_snippet = CodeValidationService.create_code_snippet(
                command.code, command.language
            )

            # Get explanation from AI provider
            explanation = await self._ai_provider.explain_code(code_snippet)

            # Convert to DTO
            result = ExplainResultDTO(
                explanation=explanation.explanation,
                line_count=code_snippet.line_count,
                character_count=code_snippet.character_count,
                provider=explanation.provider,
                placeholder=explanation.is_placeholder,
            )

            logger.info(
                f"Successfully generated explanation using {explanation.provider} provider"
            )
            return result

        except (ValidationError, AIProviderError):
            # Re-raise domain and AI provider errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error in explain handler: {e}")
            raise AIProviderError(
                f"Failed to process explanation request: {str(e)}"
            ) from e
