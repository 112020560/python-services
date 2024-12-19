import json

from src.utils.exceptions import InvalidSnsPayloadError
from src.utils.message_broker.message_broker import MessageBrokerInterface


class SNSAdapter(MessageBrokerInterface):
    def __init__(self, client):
        self._client = client
        self.provider = "SNS"

    def publish(self, event, message, attributes=None):
        messages_attributes = self._dict_to_attributes(attributes) if attributes else {}
        default_message_attributes = {
            "event_type": {
                "DataType": "String",
                "StringValue": event.event_type,
            },
        }

        return self._client.publish(
            TargetArn=event.channel,
            Subject=event.subject,
            Message=message.to_json(),
            MessageAttributes={
                **default_message_attributes,
                **messages_attributes,
            },
        )

    # Keep backwards compatibility, delete when issues fondeadora/fondeadora#1127 is closed

    def publish_json(self, payload):
        self.publish_message(json.dumps(payload))

    def publish_message(self, message, subject=None, group_id=None, attributes=None):
        if not isinstance(message, str):
            error_message = "SNS message must be a string"
            raise InvalidSnsPayloadError(error_message, message)

        args = {
            "TargetArn": self.channel,
            "Message": message,
        }
        if subject:
            args["Subject"] = subject
        if group_id:
            args["MessageGroupId"] = group_id
        if attributes:
            args["MessageAttributes"] = self._dict_to_attributes(attributes)

        return self._client.publish(**args)

    def _dict_to_attributes(self, attributes: dict) -> dict:
        client_attributes = {}

        for attribute_key, attribute_value in attributes.items():
            client_attributes.update(
                {
                    attribute_key: {
                        "DataType": "String",
                        "StringValue": attribute_value,
                    },
                }
            )

        return client_attributes
