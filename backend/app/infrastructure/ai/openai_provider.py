import httpx
import logging
from typing import Optional

from app.application.interfaces.ai_provider import AIProvider
from app.domain.exceptions import (
    AIProviderError,
    AIProviderTimeoutError,
    AIProviderQuotaError,
)
from app.domain.value_objects.code_snippet import CodeSnippet
from app.domain.value_objects.code_explanation import CodeExplanation
from app.domain.value_objects.code_refactor import CodeRefactor
from app.domain.value_objects.test_scaffold import TestScaffold
from app.infrastructure.ai.prompts.explain_prompts import ExplainPrompts
from app.infrastructure.ai.prompts.refactor_prompts import RefactorPrompts
from app.infrastructure.ai.prompts.test_generation_prompts import TestGenerationPrompts

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI implementation of the AI provider interface."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model to use for completions
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        self._max_retries = max_retries
        self._base_url = "https://api.openai.com/v1"
        self._prompts = ExplainPrompts()
        self._refactor_prompts = RefactorPrompts()
        self._test_prompts = TestGenerationPrompts()

        # Initialize HTTP client with connection pooling
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with connection pooling."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self._timeout),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

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

    async def refactor_code(
        self, code_snippet: CodeSnippet, goal: Optional[str] = None
    ) -> CodeRefactor:
        """
        Generate refactoring suggestions for the given code snippet using OpenAI.

        Args:
            code_snippet: The code snippet to refactor
            goal: Optional specific refactoring goal

        Returns:
            A code refactor suggestion with metadata

        Raises:
            AIProviderError: If the API call fails
            AIProviderTimeoutError: If the request times out
            AIProviderQuotaError: If quota is exceeded
        """
        try:
            logger.info(
                f"Requesting refactoring suggestions from OpenAI for {len(code_snippet.content)} characters"
            )

            # Prepare the prompts
            system_prompt = self._refactor_prompts.get_system_prompt()
            user_prompt = self._refactor_prompts.get_user_prompt(
                code_snippet.content, goal
            )

            # Make API request
            response_data = await self._make_completion_request(
                system_prompt, user_prompt
            )

            # Extract refactoring suggestion from response
            refactor_content = response_data["choices"][0]["message"]["content"]

            if not refactor_content:
                raise AIProviderError("Empty response from OpenAI")

            logger.info("Successfully received refactoring suggestions from OpenAI")

            # Parse the AI response to extract refactored code and improvements
            refactored_code, improvements = self._parse_refactor_response(
                refactor_content
            )

            # Create code refactor value object
            return CodeRefactor(
                original_snippet=code_snippet,
                refactored_code=refactored_code,
                explanation=refactor_content,
                improvements=improvements,
                provider=self.provider_name,
                is_placeholder=False,
            )

        except httpx.TimeoutException as e:
            logger.error(f"OpenAI refactor request timed out: {e}")
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
            logger.error(f"Unexpected error calling OpenAI for refactoring: {e}")
            raise AIProviderError(
                f"Failed to get refactoring suggestions from OpenAI: {str(e)}"
            )

    def _parse_refactor_response(self, response_content: str) -> tuple[str, list[str]]:
        """
        Parse the AI response to extract refactored code and improvements.

        Args:
            response_content: The full AI response content

        Returns:
            Tuple of (refactored_code, improvements_list)
        """
        import re

        # Try to extract refactored code from code blocks
        code_block_pattern = r"```(?:python|py|code)?\n?(.*?)\n?```"
        code_matches = re.findall(
            code_block_pattern, response_content, re.DOTALL | re.IGNORECASE
        )

        refactored_code = ""
        if code_matches:
            # Use the first code block as the refactored code
            refactored_code = code_matches[0].strip()
        else:
            # If no code blocks found, try to extract from common patterns
            lines = response_content.split("\n")
            in_code_section = False
            code_lines = []

            for line in lines:
                if any(
                    keyword in line.lower()
                    for keyword in ["refactored code", "improved code", "new code"]
                ):
                    in_code_section = True
                    continue
                elif in_code_section and line.strip() and not line.startswith("#"):
                    if line.startswith("    ") or line.startswith("\t"):
                        code_lines.append(line)
                    elif len(code_lines) > 0:
                        # Stop if we hit a non-indented line after starting code
                        break

            if code_lines:
                refactored_code = "\n".join(code_lines).strip()

        # If still no code found, use a placeholder
        if not refactored_code:
            refactored_code = "# Refactored code would go here"

        # Extract improvements from the response
        improvements = []
        lines = response_content.split("\n")

        for line in lines:
            line = line.strip()
            if any(
                keyword in line.lower()
                for keyword in ["improvement", "benefit", "advantage", "better"]
            ):
                # Clean up the improvement text
                improvement = re.sub(r"^[-•*]\s*", "", line)
                improvement = re.sub(r"^.*?:\s*", "", improvement)
                if improvement and len(improvement) > 10:  # Avoid too short items
                    improvements.append(improvement)

        # If no improvements found, add some defaults
        if not improvements:
            improvements = [
                "Improved code structure",
                "Enhanced readability",
                "Better maintainability",
            ]

        return refactored_code, improvements

    async def generate_tests(
        self, code_snippet: CodeSnippet, test_framework: Optional[str] = None
    ) -> TestScaffold:
        """
        Generate unit test scaffold for the given code snippet using OpenAI.

        Args:
            code_snippet: The code snippet to generate tests for
            test_framework: Optional test framework preference

        Returns:
            A test scaffold with metadata

        Raises:
            AIProviderError: If the API call fails
            AIProviderTimeoutError: If the request times out
            AIProviderQuotaError: If quota is exceeded
        """
        try:
            logger.info(
                f"Requesting test generation from OpenAI for {len(code_snippet.content)} characters"
            )

            # Prepare the prompts
            system_prompt = self._test_prompts.get_system_prompt()
            user_prompt = self._test_prompts.get_user_prompt(
                code_snippet.content, code_snippet.language, test_framework
            )

            # Make API request
            response_data = await self._make_completion_request(
                system_prompt, user_prompt
            )

            # Extract test code from response
            test_content = response_data["choices"][0]["message"]["content"]

            if not test_content:
                raise AIProviderError("Empty response from OpenAI")

            logger.info("Successfully received test scaffold from OpenAI")

            # Create test scaffold value object
            return TestScaffold(
                original_snippet=code_snippet,
                test_code=test_content,
                test_framework=test_framework or "pytest",
                test_cases=[
                    "test_basic_functionality",
                    "test_edge_cases",
                ],  # TODO: Extract from AI response
                setup_instructions=None,  # TODO: Extract from AI response if needed
                provider=self.provider_name,
                is_placeholder=False,
            )

        except httpx.TimeoutException as e:
            logger.error(f"OpenAI test generation request timed out: {e}")
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
            logger.error(f"Unexpected error calling OpenAI for test generation: {e}")
            raise AIProviderError(f"Failed to generate tests from OpenAI: {str(e)}")

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

        client = await self._get_client()
        response = await client.post(
            f"{self._base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()
