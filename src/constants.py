import os

SERVICE = os.getenv("SERVICE")
STAGE = os.environ["STAGE"]

DB_ECHO = bool(int(os.getenv("DB_ECHO", "0")))
DB_PRE_PING = bool(int(os.getenv("DB_PRE_PING", "0")))
FCOMPRAS_TABLE = os.getenv("FCOMPRAS_TABLE")
