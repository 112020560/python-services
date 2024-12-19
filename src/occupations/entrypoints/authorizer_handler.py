from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.parser import (
    envelopes,
    event_parser,  # type: ignore[reportUnknownVariableType]
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.occupations.adapters.fcompras_repository import DynamoFComprasRepository
from src.occupations.adapters.repository import OccupationRepository
from src.occupations.domain.model import CustomerDTO
from src.occupations.service.authorizer import authorize
from src.constants import FCOMPRAS_TABLE
from src.utils.boto import DynamoTable
from src.utils.database import READONLY_DB_CREDENTIALS
from src.utils.decorators import setup_db
from src.utils.session import Session

logger = Logger()
tracer = Tracer()

FCOMPRAS_REPO_TABLE = DynamoFComprasRepository(DynamoTable(FCOMPRAS_TABLE))


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@event_parser(model=CustomerDTO, envelope=envelopes.ApiGatewayV2Envelope)
@setup_db(READONLY_DB_CREDENTIALS)
def handler(event: CustomerDTO, _: LambdaContext) -> str:
    customer_repository = CustomerRepository(Session)
    return authorize(event, customer_repository, FCOMPRAS_REPO_TABLE)
