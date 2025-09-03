from fastapi import Depends

from app.application.dispatch import CommandDispatcher, create_dispatcher
from app.application.handlers.explain_code_handler import ExplainCodeHandler
from app.application.interfaces.ai_provider import AIProvider
from app.infrastructure.ai.fake_ai_provider import FakeAIProvider
from app.infrastructure.ai.openai_provider import OpenAIProvider
from app.infrastructure.settings import settings


def get_ai_provider() -> AIProvider:
    """Dependency provider for AI service based on settings."""
    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is required when using OpenAI provider")
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=getattr(settings, "openai_model", "gpt-4o-mini"),
        )
    else:
        # Default to fake provider for development/testing
        return FakeAIProvider()


def get_explain_handler(
    ai_provider: AIProvider = Depends(get_ai_provider),
) -> ExplainCodeHandler:
    """Dependency provider for explain code handler."""
    return ExplainCodeHandler(ai_provider)


def get_command_dispatcher(
    explain_handler: ExplainCodeHandler = Depends(get_explain_handler),
) -> CommandDispatcher:
    """Dependency provider for command dispatcher."""
    return create_dispatcher(explain_handler)
