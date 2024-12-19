from typing import TYPE_CHECKING

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

if TYPE_CHECKING:
    from mypy_boto3_sqs import SQSClient
    from mypy_boto3_sqs.type_defs import MessageAttributeValueTypeDef

from src.occupations.domain.events import DomainEvent
from src.occupations.domain.exceptions import EventPublishError
from src.occupations.domain.ports.event_bus import AbstractEventBus

logger = Logger()


class SQSEventBus(AbstractEventBus):
    """AWS SQS implementation of the event bus."""

    def __init__(self, queue_url: str, region: str = "us-east-1") -> None:
        """Initialize the SQS event bus.

        Args:
            queue_url: The URL of the SQS queue
            region: AWS region where the queue is located
        """
        self.queue_url = queue_url
        self.sqs: SQSClient = boto3.client("sqs", region_name=region)  # type: ignore[reportUnknownMemberType]

    def publish(self, event: DomainEvent) -> None:
        try:
            message_body = event.model_dump_json()
            message_attributes: dict[str, MessageAttributeValueTypeDef] = {
                "event_type": {
                    "DataType": "String",
                    "StringValue": event.__class__.__name__,
                }
            }

            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                MessageAttributes=message_attributes,
            )

            logger.info(
                "Event published successfully",
                extra={
                    "event_type": event.__class__.__name__,
                    "message_id": response["MessageId"],
                },
            )

        except ClientError as e:
            logger.exception(
                "Failed to publish event to SQS",
                extra={"event_type": event.__class__.__name__, "error": str(e)},
            )
            raise EventPublishError(event) from e


class LocalEventBus(AbstractEventBus):
    """Local implementation of event bus for testing."""

    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        """Store the event locally.

        Args:
            event: The domain event to store
        """
        self.events.append(event)
