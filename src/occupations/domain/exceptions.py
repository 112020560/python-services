from src.occupations.domain.events import DomainEvent


class CustomerNotFoundError(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(f"User with id {user_id} not found")


class EventPublishError(Exception):
    """Raised when an event cannot be published to the event bus."""

    def __init__(self, event: DomainEvent) -> None:
        super().__init__(f"Failed to publish event: {event.__class__.__name__}")
