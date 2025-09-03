from app.domain.value_objects.code_snippet import CodeSnippet

PROMPT_VERSION = "1.0.0"


class ExplainPrompts:
    """Centralized prompt templates for code explanation."""

    def get_system_prompt(self) -> str:
        """Get the system prompt for code explanation."""
        return """You are an expert code analysis assistant. Your job is to provide clear, comprehensive explanations of code snippets.

Guidelines:
1. Explain what the code does in plain language
2. Break down complex logic into understandable parts
3. Identify key programming concepts and patterns
4. Mention any potential issues or improvements
5. Use markdown formatting for better readability
6. Be concise but thorough
7. Assume the reader has basic programming knowledge

Format your response with clear sections using markdown headers."""

    def get_user_prompt(self, code_snippet: CodeSnippet) -> str:
        """Get the user prompt with the code to explain."""
        language_hint = (
            f" (Language: {code_snippet.language})" if code_snippet.language else ""
        )

        return f"""Please explain this code snippet{language_hint}:

```{code_snippet.language or 'text'}
{code_snippet.content}
```

Provide a clear explanation of what this code does, how it works, and any notable patterns or concepts it demonstrates."""

    def get_version(self) -> str:
        """Get the current prompt version."""
        return PROMPT_VERSION
