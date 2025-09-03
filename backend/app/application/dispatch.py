from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Callable, Awaitable, Dict, Type
import logging
import time
import logging

logger = logging.getLogger(__name__)

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class Handler(ABC, Generic[TCommand, TResult]):
    """Base handler interface."""

    @abstractmethod
    async def handle(self, command: TCommand) -> TResult:
        pass


class Middleware(ABC):
    """Base middleware for cross-cutting concerns."""

    @abstractmethod
    async def execute(
        self, command: Any, next_handler: Callable[[Any], Awaitable[Any]]
    ) -> Any:
        pass


class LoggingMiddleware(Middleware):
    """Middleware for request/response logging."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def execute(
        self, command: Any, next_handler: Callable[[Any], Awaitable[Any]]
    ) -> Any:
        start_time = time.time()
        command_name = command.__class__.__name__

        self.logger.info(f"Executing command: {command_name}")

        try:
            result = await next_handler(command)
            duration = (time.time() - start_time) * 1000
            self.logger.info(f"Command {command_name} completed in {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.error(
                f"Command {command_name} failed after {duration:.2f}ms: {str(e)}"
            )
            raise


# class CommandDispatcher:
#     """Enhanced dispatcher with middleware support."""

#     def __init__(self):
#         self._handlers: dict[type, Handler] = {}
#         self._middlewares: list[Middleware] = []

#     def register_handler(self, command_type: type, handler: Handler) -> None:
#         self._handlers[command_type] = handler

#     def add_middleware(self, middleware: Middleware) -> None:
#         self._middlewares.append(middleware)

#     async def dispatch(self, command: Any) -> Any:
#         command_type = type(command)
#         if command_type not in self._handlers:
#             raise ValueError(f"No handler registered for {command_type.__name__}")

#         handler = self._handlers[command_type]

#         # Build middleware chain
#         async def execute_handler(cmd: Any) -> Any:
#             return await handler.handle(cmd)

#         # Apply middlewares in reverse order
#         next_handler = execute_handler
#         for middleware in reversed(self._middlewares):
#             current_middleware = middleware
#             current_next = next_handler

#             async def middleware_wrapper(
#                 cmd: Any, mw=current_middleware, next_fn=current_next
#             ) -> Any:
#                 return await mw.execute(cmd, next_fn)

#             next_handler = middleware_wrapper

#         return await next_handler(command)


class CommandDispatcher:
    """
    Command dispatcher for CQRS pattern.
    Maps command types to their handlers and executes them.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[Any], Handler] = {}

    def register_handler(
        self, command_type: Type[TCommand], handler: Handler[TCommand, TResult]
    ) -> None:
        """
        Register a handler for a specific command type.

        Args:
            command_type: The command class type
            handler: The handler instance for this command type
        """
        if command_type in self._handlers:
            logger.warning(f"Handler for {command_type.__name__} is being overridden")

        self._handlers[command_type] = handler
        logger.debug(f"Registered handler for {command_type.__name__}")

    # Add alias for backward compatibility
    def register(
        self, command_type: Type[TCommand], handler: Handler[TCommand, TResult]
    ) -> None:
        """Alias for register_handler to maintain compatibility."""
        self.register_handler(command_type, handler)

    async def dispatch(self, command: TCommand) -> TResult:
        """
        Dispatch a command to its registered handler.

        Args:
            command: The command instance to execute

        Returns:
            The result from the handler

        Raises:
            ValueError: If no handler is registered for the command type
        """
        command_type = type(command)

        if command_type not in self._handlers:
            raise ValueError(
                f"No handler registered for command type: {command_type.__name__}"
            )

        handler = self._handlers[command_type]

        logger.debug(f"Dispatching command: {command_type.__name__}")

        try:
            result = await handler.handle(command)
            logger.debug(f"Successfully handled command: {command_type.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error handling command {command_type.__name__}: {str(e)}")
            raise

    def is_registered(self, command_type: Type[Any]) -> bool:
        """Check if a handler is registered for the given command type."""
        return command_type in self._handlers

    def get_registered_commands(self) -> list[Type[Any]]:
        """Get list of all registered command types."""
        return list(self._handlers.keys())


def create_dispatcher() -> CommandDispatcher:
    """Factory function to create configured dispatcher."""
    dispatcher = CommandDispatcher()

    # Add default middlewares
    dispatcher.add_middleware(LoggingMiddleware())

    return dispatcher
