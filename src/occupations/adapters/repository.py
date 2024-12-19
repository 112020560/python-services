from src.occupations.domain.model import Occupation
from src.occupations.domain.ports.repository import AbstractRepository


class OccupationRepository(AbstractRepository):
    def __init__(self, occupation):
        self.occupation = occupation

    def get(self, customer_id: int) -> Occupation | None:
        return self.occupation.get(Occupation, customer_id)
