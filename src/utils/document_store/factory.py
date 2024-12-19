import boto3

from src.utils.document_store.adapters.dynamo_db import DynamoDBAdapter
from src.utils.document_store.document_store import DocumentStoreInterface


def get_document_store(
    table_name: str,
    klass: str = "DynamoDB",
) -> DocumentStoreInterface:
    if klass == "DynamoDB":
        return DynamoDBAdapter(boto3.resource("dynamodb").Table(table_name))

    raise ValueError(f"Invalid document store class: {klass}")
