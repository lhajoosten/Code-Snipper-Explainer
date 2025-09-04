from functools import lru_cache
from app.application.interfaces.ai_provider import AIProvider
from app.infrastructure.ai.openai_provider import OpenAIProvider
from app.infrastructure.settings import settings
from app.application.dispatch import CommandDispatcher
from app.application.handlers.explain_code_handler import ExplainCodeHandler
from app.application.handlers.refactor_code_handler import RefactorCodeHandler
from app.application.handlers.generate_tests_handler import GenerateTestsHandler
from app.application.commands.explain_code_command import ExplainCodeCommand
from app.application.commands.refactor_code_command import RefactorCodeCommand
from app.application.commands.generate_tests_command import GenerateTestsCommand


@lru_cache()
def get_ai_provider() -> AIProvider:
    """Get AI provider based on settings."""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    return OpenAIProvider(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        timeout=settings.ai_timeout,
    )


@lru_cache()
def get_command_dispatcher() -> CommandDispatcher:
    """Get configured command dispatcher."""
    dispatcher = CommandDispatcher()

    # Register handlers
    ai_provider = get_ai_provider()
    explain_handler = ExplainCodeHandler(ai_provider)
    refactor_handler = RefactorCodeHandler(ai_provider)
    generate_tests_handler = GenerateTestsHandler(ai_provider)

    dispatcher.register(ExplainCodeCommand, explain_handler)
    dispatcher.register(RefactorCodeCommand, refactor_handler)
    dispatcher.register(GenerateTestsCommand, generate_tests_handler)

    return dispatcher
