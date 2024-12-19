from enum import Enum
from pydantic import BaseModel

class OccupationType(str, Enum):
    EMPLOYEE = "employee"
    STUDENT = "student"
    FREELANCER = "freelancer"
    OTHER = "other"
    
class Occupation(BaseModel):
    occupation: OccupationType
    is_real_property: bool = True
    
class OccupationDTO(BaseModel):
    customer_id: int
    occupation: str
    
def select_occupation(occupation: str) -> dict:
    occupation_instance = Occupation(
        occupation=OccupationType(occupation),
        is_real_property=True,
    )
    return occupation_instance.model_dump()  # Convert the Occupation instance to a dictionary
