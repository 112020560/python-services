from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict

from src.occupations.domain.model import OccupationType


class DomainEvent(BaseModel):
    """Base class for all domain events."""

    model_config = ConfigDict(frozen=True)

    event_id: UUID | None = None
    timestamp: datetime | None = None

    def __init__(self, **data: Any) -> None:
        if "event_id" not in data:
            data["event_id"] = uuid4()
        if "timestamp" not in data:
            data["timestamp"] = datetime.now(UTC)
        super().__init__(**data)


class OccupationSelected(DomainEvent):
    """Event triggered when a customer selects an occupation."""

    customer_id: str
    occupation: OccupationType
    is_real_property: bool = True


class OccupationSelectionRejected(DomainEvent):
    """Event triggered when an occupation selection is rejected."""

    customer_id: str
    occupation: OccupationType | None = None
    reason: str | None = None
