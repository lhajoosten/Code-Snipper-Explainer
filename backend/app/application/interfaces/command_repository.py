from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from uuid import UUID

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Base repository interface following DDD patterns."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update existing entity."""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete entity by ID."""
        pass
