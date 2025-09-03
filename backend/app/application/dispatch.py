from typing import Any, Dict, Type, TypeVar, Generic
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class Handler(ABC, Generic[T, R]):
    """Base handler interface."""

    @abstractmethod
    async def handle(self, command: T) -> R:
        """Handle the command and return result."""
        pass


class CommandDispatcher:
    """Central dispatcher for commands following CQRS pattern."""

    def __init__(self) -> None:
        self._handlers: Dict[Type, Handler] = {}

    def register(self, command_type: Type[T], handler: Handler[T, R]) -> None:
        """Register a handler for a specific command type."""
        self._handlers[command_type] = handler
        logger.debug(f"Registered handler for {command_type.__name__}")

    async def dispatch(self, command: T) -> Any:
        """Dispatch command to appropriate handler."""
        command_type = type(command)

        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for {command_type.__name__}")

        handler = self._handlers[command_type]
        logger.info(f"Dispatching {command_type.__name__}")

        try:
            result = await handler.handle(command)
            logger.info(f"Successfully handled {command_type.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error handling {command_type.__name__}: {str(e)}")
            raise
