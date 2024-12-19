from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.parser import (
    event_parser,  # type: ignore[reportUnknownVariableType]
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.auth.adapters.fcompras_repository import DynamoFComprasRepository
from src.auth.domain.model import TokenValidate
from src.auth.service.validate import validate_token
from src.constants import FCOMPRAS_TABLE
from src.utils.boto import DynamoTable

logger = Logger()
tracer = Tracer()

FCOMPRAS_REPO_TABLE = DynamoFComprasRepository(DynamoTable(FCOMPRAS_TABLE))


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@event_parser(model=TokenValidate)
def handler(event: TokenValidate, _: LambdaContext) -> str:
    return validate_token(event, FCOMPRAS_REPO_TABLE)
