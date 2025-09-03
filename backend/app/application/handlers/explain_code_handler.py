from app.application.dispatch import Handler
from app.application.commands.explain_code_command import ExplainCodeCommand
from app.application.dto.explain_result_dto import ExplainResultDTO
from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import AIProviderError, ValidationError
from app.domain.value_objects.code_snippet import CodeSnippet
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
        # Validate command
        if not command.code or not command.code.strip():
            raise ValidationError("Code content is required")

        if len(command.code) > 50000:  # Max length from settings
            raise ValidationError("Code content is too long")

        try:
            logger.info(
                f"Explaining code using {self._ai_provider.provider_name} provider"
            )

            # Create code snippet value object
            code_snippet = CodeSnippet(content=command.code, language=command.language)

            # Get explanation from AI provider
            explanation = await self._ai_provider.explain_code(code_snippet)

            # Convert to DTO using the correct properties
            result = ExplainResultDTO(
                explanation=explanation.explanation,
                line_count=code_snippet.line_count,  # From code_snippet
                character_count=code_snippet.character_count,  # From code_snippet
                provider=explanation.provider,
                placeholder=explanation.is_placeholder,  # Note: placeholder not is_placeholder
            )

            logger.info(
                f"Successfully generated explanation using {explanation.provider} provider"
            )
            return result

        except AIProviderError:
            # Re-raise AI provider errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error in explain handler: {e}")
            raise AIProviderError(
                f"Failed to process explanation request: {str(e)}"
            ) from e
