from functools import lru_cache
from app.application.interfaces.ai_provider import AIProvider
from app.infrastructure.ai.fake_ai_provider import FakeAIProvider
from app.infrastructure.ai.openai_provider import OpenAIProvider
from app.infrastructure.settings import settings
from app.application.dispatch import CommandDispatcher
from app.application.handlers.explain_code_handler import ExplainCodeHandler
from app.application.commands.explain_code_command import ExplainCodeCommand


@lru_cache()
def get_ai_provider() -> AIProvider:
    """Get AI provider based on settings."""
    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        return OpenAIProvider(api_key=settings.openai_api_key)
    else:
        return FakeAIProvider()


@lru_cache()
def get_command_dispatcher() -> CommandDispatcher:
    """Get configured command dispatcher."""
    dispatcher = CommandDispatcher()

    # Register handlers
    ai_provider = get_ai_provider()
    explain_handler = ExplainCodeHandler(ai_provider)
    dispatcher.register(ExplainCodeCommand, explain_handler)

    return dispatcher
