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
    
def select_occupation(occupation: str) -> Occupation:
    return Occupation(
        occupation=OccupationType(occupation),
        is_real_property=True,
    )