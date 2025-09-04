"""Prompts for code refactoring using OpenAI."""


class RefactorPrompts:
    """Centralized prompts for code refactoring."""

    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for code refactoring."""
        return """You are an expert software engineer specializing in code refactoring and improvement.

Your task is to analyze the provided code snippet and suggest meaningful refactoring improvements.
Focus on:
- Code readability and maintainability
- Following best practices and design patterns
- Reducing complexity and improving structure
- Eliminating code smells
- Making the code more testable

Provide:
1. A clear explanation of the refactoring suggestions
2. The refactored code with improvements
3. Specific benefits of the changes
4. Any trade-offs or considerations

Format your response as a structured analysis with clear sections."""

    @staticmethod
    def get_user_prompt(code_snippet: str, goal: str = None) -> str:
        """
        Get the user prompt for code refactoring.

        Args:
            code_snippet: The code to refactor
            goal: Optional specific refactoring goal

        Returns:
            Formatted user prompt
        """
        base_prompt = f"""Please analyze and refactor the following code snippet:

```code
{code_snippet}
```

"""

        if goal:
            base_prompt += f"""
Specific refactoring goal: {goal}

"""

        base_prompt += """
Please provide:
1. **Analysis**: What issues or improvements do you see?
2. **Refactored Code**: The improved version
3. **Benefits**: What advantages does this refactoring provide?
4. **Considerations**: Any potential trade-offs or additional improvements?

Focus on practical, actionable improvements that enhance code quality."""

        return base_prompt
