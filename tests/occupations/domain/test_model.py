from src.occupations.domain.model import Occupation, OccupationType, select_occupation

CUSTOMER_ID = 1234

def test_occupation():
    occupation = Occupation(
      occupation=OccupationType.EMPLOYEE,
    )
    assert occupation.occupation == OccupationType.EMPLOYEE


def test_select_occupation():
    selected_occupation = select_occupation("employee")
    assert selected_occupation.occupation == OccupationType.EMPLOYEE