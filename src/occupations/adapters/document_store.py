from abc import ABCMeta, abstractmethod
from typing import Any


class ConditionalPutFailedError(Exception):
    pass


class DocumentStoreInterface(metaclass=ABCMeta):
    """DocumentStoreInterface is an abstract base class that defines the
    interface for a document store.

    Methods:
        get(key: Dict):
            Retrieve a document based on the provided key.

        get_all():
            Retrieve all documents from the store.

        filter_by(attribute: str, target_value):
            Filter documents by a specific attribute and target value.

        filter_all_pages_by(attribute: str, target_value):
            Filter documents across all pages by a specific attribute and target value.

        query(
            Query documents based on specified conditions, with optional limit, index name, order, and filters.

        put(attributes: Dict, condition: Optional[Any] = None):
            Insert a document with the specified attributes, optionally conditioned on some criteria.

        bulk_insert(rows: List[Dict]):
            Insert multiple documents in bulk.

        update(key: Dict, attributes: Dict):
            Update a document identified by the provided key with the specified attributes.

        list_append(key: Dict, attributes: Dict):
            Append items to a list attribute of a document identified by the provided key.

        delete(key: Dict):
            Delete a document identified by the provided key.

        count() -> int:
            Count the number of documents in the store.

        upsert(key: Dict, attributes: Dict):
            Insert or update a document identified by the provided key with the specified attributes.

        list_count(item_key_name: str, item_key_value: str, property_name: str):
            Count the number of items in a list attribute of documents that match the specified criteria.

        batch_writer():
            Create a batch writer for performing bulk write operations.

        get_all_pages():
            Retrieve all documents across all pages from the store.
    """

    @abstractmethod
    def get(self, key: dict):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def filter_by(self, attribute: str, target_value):
        raise NotImplementedError

    @abstractmethod
    def filter_all_pages_by(self, attribute: str, target_value):
        raise NotImplementedError

    @abstractmethod
    def query(
        self,
        conditions: dict[str, str],
        limit: int | None = None,
        index_name: str | None = None,
        asc_order: bool | None = None,
        filters: dict[str, Any] | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def put(self, attributes: dict, condition: Any | None = None):
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(self, rows: list[dict]):
        raise NotImplementedError

    @abstractmethod
    def update(self, key: dict, attributes: dict):
        raise NotImplementedError

    @abstractmethod
    def list_append(self, key: dict, attributes: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: dict):
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def upsert(self, key: dict, attributes: dict):
        raise NotImplementedError

    @abstractmethod
    def list_count(self, item_key_name: str, item_key_value: str, property_name: str):
        raise NotImplementedError

    @abstractmethod
    def batch_writer(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_pages(self):
        raise NotImplementedError
