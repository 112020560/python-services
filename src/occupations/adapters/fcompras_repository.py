from dataclasses import dataclass

from src.occupations.domain.ports.fcompras_repository import FComprasRepository
from src.utils.document_store.adapters.dynamo_db import DynamoDBAdapter


@dataclass
class DynamoFComprasRepository(FComprasRepository):
    fcompras_table: DynamoDBAdapter

    def get(self, customer_id):
        return self.fcompras_table.get(
            key={"customer_id": customer_id},
        )

    def persist(self, key, fcompras_result: dict):
        return self.fcompras_table.put({**key, **fcompras_result})
