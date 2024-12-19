import json
import warnings
from collections.abc import Sequence

import boto3
from mypy_boto3_sqs.client import SQSClient
from mypy_boto3_sqs.type_defs import SendMessageBatchRequestEntryTypeDef

from src.constants import SERVICE, STAGE
from src.utils.document_store.adapters.dynamo_db import DynamoDBAdapter
from src.utils.message_broker.adapters.sns import SNSAdapter


def remove_none_values(data: dict) -> dict:
    return {key: value for key, value in data.items() if value is not None}


def invoke(service: str, function: str, payload: dict):
    """Call lambda function."""
    client = boto3.client("lambda")

    response = client.invoke(
        FunctionName=f"{service}-{STAGE}-{function}",
        InvocationType="RequestResponse",
        Payload=json.dumps({"source": SERVICE, **payload}),
    )

    return response["Payload"].read().decode("utf-8")


def queue(
    queue_url: str,
    payload: dict,
    message_attributes=None,
    delay_seconds=None,
    message_group_id=None,
    message_deduplication_id=None,
):
    """Queue message to SQS."""
    client: SQSClient = boto3.client("sqs")

    message_params = {
        "QueueUrl": queue_url,
        "MessageBody": json.dumps(payload),
        "MessageAttributes": message_attributes,
        "DelaySeconds": delay_seconds,
        "MessageGroupId": message_group_id,
        "MessageDeduplicationId": message_deduplication_id,
    }

    clean_params = {key: value for key, value in message_params.items() if value}

    return client.send_message(**clean_params)


def queue_batch(queue_url: str, entries: Sequence[SendMessageBatchRequestEntryTypeDef]):
    """Queue batch messages to SQS."""
    client: SQSClient = boto3.client("sqs")

    return client.send_message_batch(
        QueueUrl=queue_url,
        Entries=entries,
    )


def scan(**kwargs):
    """Retrieve data from dynamoDB."""
    client = boto3.client("dynamodb")

    return client.scan(**kwargs)


class S3:
    def __init__(self, bucket_url):
        self._bucket_url = bucket_url
        self._resource = boto3.resource("s3")

    def get(self, file_name):
        return self._resource.Object(self._bucket_url, file_name).get()

    def upload(self, file_name, file_content, content_type: str | None = None):
        optional_params = {"ContentType": content_type}
        return self._resource.Object(self._bucket_url, file_name).put(
            Body=file_content,
            **remove_none_values(optional_params),
        )

    def delete(self, file_name):
        return self._resource.Object(self._bucket_url, file_name).delete()

    def get_url(self, file_name):
        return f"https://{self._bucket_url}.s3.amazonaws.com/{file_name}"

    def get_bucket(self):
        return self._resource.Bucket(self._bucket_url)

    def get_bucket_list_objects(self, dir_name):
        bucket_dir = self.get_bucket()
        return [bucket.key for bucket in bucket_dir.objects.filter(Prefix=dir_name)]

    def read(self, file_name):
        return self.get(file_name)["Body"].read()


class SNS(SNSAdapter):
    # Keep backwards compatibility, delete when issues fondeadora/fondeadora#1127 is closed
    def __init__(self, target_arn):
        self.channel = target_arn
        super().__init__(
            client=boto3.client("sns"),
        )


class DynamoTable(DynamoDBAdapter):
    def __init__(self, table_name):
        warnings.warn(
            "Deprecated: use DynamoDBAdapter through get_document_store factory",
            DeprecationWarning,
        )
        super().__init__(boto3.resource("dynamodb").Table(table_name))
