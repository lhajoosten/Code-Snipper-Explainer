"""Prompts for test generation using OpenAI."""


class TestGenerationPrompts:
    """Centralized prompts for test generation."""

    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for test generation."""
        return """You are an expert software engineer specializing in writing comprehensive unit tests.

Your task is to analyze the provided code snippet and generate a complete test scaffold that covers:
- Happy path scenarios
- Edge cases and error conditions
- Input validation
- Integration points
- Mocking external dependencies

Focus on:
- High test coverage (aim for >80%)
- Meaningful test names that describe behavior
- Proper test structure with Arrange-Act-Assert pattern
- Realistic test data and scenarios
- Both positive and negative test cases

Use modern testing best practices and provide tests that are maintainable and reliable."""

    @staticmethod
    def get_user_prompt(
        code_snippet: str, language: str = None, test_framework: str = None
    ) -> str:
        """
        Get the user prompt for test generation.

        Args:
            code_snippet: The code to generate tests for
            language: Programming language hint
            test_framework: Preferred test framework

        Returns:
            Formatted user prompt
        """
        language_hint = f" ({language})" if language else ""
        framework_hint = f" using {test_framework}" if test_framework else ""

        prompt = f"""Please analyze the following code snippet{language_hint} and generate a comprehensive unit test scaffold{framework_hint}:

```code
{code_snippet}
```

Please provide:
1. **Test Analysis**: What functionality needs to be tested?
2. **Test Structure**: How should the tests be organized?
3. **Complete Test Code**: Full test implementation with all necessary imports
4. **Coverage Notes**: What scenarios are covered and any gaps?

Ensure the tests are:
- Comprehensive but focused
- Easy to understand and maintain
- Following testing best practices
- Including both positive and negative cases

If the code has external dependencies, include examples of how to mock them."""

        return prompt
