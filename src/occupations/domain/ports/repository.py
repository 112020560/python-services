import abc

from src.occupations.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, customer_id: str) -> model.Occupation:
        raise NotImplementedError
