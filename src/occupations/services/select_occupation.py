from src.occupations.domain import model
from src.occupations.domain.ports.fcompras_repository import FComprasRepository

def validate_and_process_occupation(
    event: model.OccupationDTO,
    fcompras_repository: FComprasRepository,
    ) -> dict:
    if event.occupation not in model.OccupationType._value2member_map_:
        raise ValueError(f"Invalid occupation type: {model.OccupationDTO.occupation}")
    
    result = model.select_occupation(event.occupation)
    fcompras_repository.persist({"customer_id": event.customer_id}, result) # type: ignore
    
    return result
    
    