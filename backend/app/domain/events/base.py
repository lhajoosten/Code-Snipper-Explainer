from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Base class for domain events."""

    event_id: UUID = uuid4()
    occurred_at: datetime = datetime.utcnow()


@dataclass(frozen=True)
class CodeExplainedEvent(DomainEvent):
    """Event raised when code has been explained."""

    code_length: int
    language: str | None
    provider: str
    success: bool
