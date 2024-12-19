from src.occupations.domain import model
from src.occupations.domain.ports.fcompras_repository import FComprasRepository

def validate_and_process_occupation(occupation: str) -> model.Occupation:
    if occupation not in model.OccupationType._value2member_map_:
        raise ValueError(f"Invalid occupation type: {occupation}")
    
    result = model.select_occupation(occupation)
    
    return result

    # After Save the value update the dynamo table
    # fcompras-services-fcompras-data-dev with key customer_id,
    # update status with confirm_address
    
    