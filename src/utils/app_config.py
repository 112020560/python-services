import json
from dataclasses import dataclass
from urllib import request

from aws_lambda_powertools.utilities import parameters

APP_CONFIG_PROXY_URL = "http://localhost:2772"


@dataclass
class AppConfig:
    application: str
    environment: str
    configuration: str

    def __post_init__(self):
        self.url = f"{APP_CONFIG_PROXY_URL}/applications/{self.application}/environments/{self.environment}/configurations/{self.configuration}"

    def load(self) -> dict:
        try:
            return json.loads(request.urlopen(self.url).read())  # noqa: S310
        except Exception:
            return json.loads(
                parameters.get_app_config(  # type: ignore
                    name=self.configuration,
                    environment=self.environment,
                    application=self.application,
                ),
            )
