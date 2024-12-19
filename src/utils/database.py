from types import MappingProxyType

from src.constants import SERVICE, STAGE
from src.credentials.provider import CredentialsProvider

DB_CREDENTIALS = CredentialsProvider(stage=STAGE).get_db_credentials(
    configuration_name=SERVICE,
)

COMMON_DB_CREDENTIALS = MappingProxyType(
    {
        "drivername": "postgresql+psycopg2",
        "database": DB_CREDENTIALS.name,
        "username": DB_CREDENTIALS.username,
        "password": DB_CREDENTIALS.password,
        "port": DB_CREDENTIALS.port,
    }
)

WRITE_DB_CREDENTIALS = MappingProxyType(
    {
        **COMMON_DB_CREDENTIALS,
        "host": DB_CREDENTIALS.host,
    }
)

READONLY_DB_CREDENTIALS = MappingProxyType(
    {
        **COMMON_DB_CREDENTIALS,
        "host": DB_CREDENTIALS.readonly_host,
    }
)
