from typing import Any

import botocore
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from src.occupations.adapters.document_store import (
    ConditionalPutFailedError,
    DocumentStoreInterface,
)

RETURN_VALUE = "UPDATED_NEW"


class DynamoDBAdapter(DocumentStoreInterface):
    def __init__(self, table: Table):
        self._table = table

    def get(self, key: dict):
        return self._table.get_item(Key=key).get("Item")

    def get_all(self):
        return self._table.scan().get("Items")

    def filter_by(self, attribute: str, target_value):
        return self._table.scan(
            FilterExpression=Key(attribute).eq(target_value),
        ).get("Items")

    def filter_all_pages_by(self, attribute: str, target_value):
        scan_result = self._table.scan(
            FilterExpression=Key(attribute).eq(target_value),
        )
        matches = scan_result["Items"]

        while "LastEvaluatedKey" in scan_result:
            scan_result = self._table.scan(
                FilterExpression=Key(attribute).eq(target_value),
                ExclusiveStartKey=scan_result["LastEvaluatedKey"],
            )
            matches.extend(scan_result["Items"])

        return matches

    def query(
        self,
        conditions: dict[str, str],
        limit: int | None = None,
        index_name: str | None = None,
        asc_order: bool | None = None,
        filters: dict[str, Any] | None = None,
    ):
        extra_args: dict[str, Any] = {}
        if limit:
            extra_args["Limit"] = limit

        if index_name:
            extra_args["IndexName"] = index_name

        if asc_order is not None:
            extra_args["ScanIndexForward"] = asc_order

        if filters:
            extra_args["FilterExpression"] = self._build_expression(filters)

        query_result = self._table.query(
            KeyConditionExpression=self._build_expression(conditions),
            **extra_args,
        )

        return query_result.get("Items")

    def put(self, attributes: dict, condition=None):
        extra_args = {}
        if condition:
            extra_args["ConditionExpression"] = condition
        try:
            return self._table.put_item(Item=attributes, **extra_args)
        except botocore.exceptions.ClientError as exception:
            if exception.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ConditionalPutFailedError

            raise exception("Error while putting item in DynamoDB")

    def bulk_insert(self, rows: list[dict]):
        with self._table.batch_writer() as batch:
            for row in rows:
                batch.put_item(row)

    def update(self, key: dict, attributes: dict):
        return self._table.update_item(
            Key=key,
            UpdateExpression=self._update_expression(attributes),
            ExpressionAttributeNames=self._expression_attribute_names(attributes),
            ExpressionAttributeValues=self._expression_attribute_values(attributes),
            ReturnValues=RETURN_VALUE,  # type: ignore
        )

    def list_append(self, key: dict, attributes: dict):
        return self._table.update_item(
            Key=key,
            UpdateExpression=self._list_append_expression(attributes),
            ExpressionAttributeNames=self._expression_attribute_names(attributes),
            ExpressionAttributeValues={
                ":empty_list": [],
                **self._expression_attribute_values(attributes),
            },
            ReturnValues=RETURN_VALUE,  # type: ignore
        )

    def delete(self, key: dict):
        return self._table.delete_item(Key=key)

    def count(self) -> int:
        return self._table.item_count

    def upsert(self, key: dict, attributes: dict):
        return self.put({**key, **attributes})

    def list_count(self, item_key_name: str, item_key_value: str, property_name: str):
        found_item = self.get(
            {item_key_name: item_key_value},
        )

        if not found_item:
            return 0

        return len(found_item.get(property_name, []))

    def batch_writer(self):
        return self._table.batch_writer()

    def get_all_pages(self):
        scan_result = self._table.scan()
        items = scan_result["Items"]

        while "LastEvaluatedKey" in scan_result:
            scan_result = self._table.scan(
                ExclusiveStartKey=scan_result["LastEvaluatedKey"],
            )
            items.extend(scan_result["Items"])

        return items

    def _list_append_expression(self, attributes: dict):
        expression = (
            "{key} = list_append(if_not_exists({attribute}, :empty_list), {value})"
        )

        return "SET {param}".format(
            param=",".join(
                expression.format(
                    key=f"#{key}",
                    attribute=key,
                    value=f":{key}",
                )
                for key in attributes
            ),
        )

    def _update_expression(self, attributes: dict):
        return "SET {param}".format(
            param=",".join(f"#{key}=:{key}" for key in attributes),
        )

    def _expression_attribute_names(self, attributes: dict):
        return {f"#{key}": key for key in attributes}

    def _expression_attribute_values(self, attributes: dict):
        return {f":{key}": attr for key, attr in attributes.items()}

    def _build_expression(self, attr_values: dict[str, str]):
        key_condition = None

        for key, value in attr_values.items():
            condition = Key(key).eq(value)
            key_condition = (
                condition if key_condition is None else key_condition & condition  # type: ignore
            )

        return key_condition
