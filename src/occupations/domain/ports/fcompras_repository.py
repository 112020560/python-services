from abc import ABC, abstractmethod


class FComprasRepository(ABC):
    @abstractmethod
    def get(
        self,
        customer_id: int,
    ) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        key: int,
        data: dict,
    ) -> None:
        raise NotImplementedError
