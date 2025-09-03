import httpx
import logging

from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import (
    AIProviderError,
    AIProviderTimeoutError,
    AIProviderQuotaError,
)
from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.value_objects.code_explanation import CodeExplanation
from app.infrastructure.ai.prompts.explain_prompts import ExplainPrompts

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI implementation of the AI provider interface."""

    def __init__(
        self, api_key: str, model: str = "gpt-4o-mini", timeout: int = 30
    ) -> None:
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model to use for completions
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        self._base_url = "https://api.openai.com/v1"
        self._prompts = ExplainPrompts()

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "openai"

    async def explain_code(self, code_snippet: CodeSnippet) -> CodeExplanation:
        """
        Generate an explanation for the given code snippet using OpenAI.

        Args:
            code_snippet: The code snippet to explain

        Returns:
            A code explanation with metadata

        Raises:
            AIProviderError: If the API call fails
            AIProviderTimeoutError: If the request times out
            AIProviderQuotaError: If quota is exceeded
        """
        try:
            logger.info(
                f"Requesting explanation from OpenAI for {len(code_snippet.content)} characters"
            )

            # Prepare the prompt using centralized prompts
            system_prompt = self._prompts.get_system_prompt()
            user_prompt = self._prompts.get_user_prompt(code_snippet)

            # Make API request to chat completions (not responses API)
            response_data = await self._make_completion_request(
                system_prompt, user_prompt
            )

            # Extract explanation from response
            explanation_content = response_data["choices"][0]["message"]["content"]

            if not explanation_content:
                raise AIProviderError("Empty response from OpenAI")

            logger.info("Successfully received explanation from OpenAI")

            # Create code explanation value object with correct constructor
            return CodeExplanation(
                snippet=code_snippet,  # Required parameter
                explanation=explanation_content,
                provider=self.provider_name,
                is_placeholder=False,
            )

        except httpx.TimeoutException as e:
            logger.error(f"OpenAI request timed out: {e}")
            raise AIProviderTimeoutError(
                f"Request timed out after {self._timeout} seconds"
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.error("OpenAI quota exceeded")
                raise AIProviderQuotaError("OpenAI API quota exceeded")
            elif e.response.status_code >= 500:
                logger.error(f"OpenAI server error: {e.response.status_code}")
                raise AIProviderError(f"OpenAI server error: {e.response.status_code}")
            else:
                logger.error(
                    f"OpenAI API error: {e.response.status_code} - {e.response.text}"
                )
                raise AIProviderError(f"OpenAI API error: {e.response.status_code}")

        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI: {e}")
            raise AIProviderError(f"Failed to get explanation from OpenAI: {str(e)}")

    async def _make_completion_request(
        self, system_prompt: str, user_prompt: str
    ) -> dict:
        """Make a completion request to OpenAI Chat Completions API."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,  # Deterministic-ish for explanations
            "max_tokens": 2000,
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",  # Correct endpoint
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
