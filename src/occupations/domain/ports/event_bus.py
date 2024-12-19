from abc import ABC, abstractmethod

from src.occupations.domain.events import DomainEvent


class AbstractEventBus(ABC):
    """Abstract base class for event bus implementations."""

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publish an event to the event bus.

        Args:
            event: The domain event to publish

        Raises:
            EventPublishError: If the event cannot be published
        """
        raise NotImplementedError
