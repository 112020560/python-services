from dataclasses import dataclass

from src.credentials import entities
from src.utils.app_config import AppConfig

BASE_URL = "base_url"
API_KEY = "api_key"


@dataclass
class CredentialsProvider:
    stage: str

    def get_db_credentials(
        self,
        configuration_name: str | None = None,
    ) -> entities.DatabaseCredentials:
        config = AppConfig(
            application=entities.DatabaseCredentials.APPLICATION,
            environment=self.stage,
            configuration=configuration_name or entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.DatabaseCredentials(
            name=config["db_name"],
            host=config["host"],
            readonly_host=config["readonly_host"],
            port=config["port"],
            password=config["password"],
            username=config["username"],
        )

    def get_firebase_credentials(
        self,
    ) -> entities.FirebaseCredentials:
        config = AppConfig(
            application=entities.FirebaseCredentials.APPLICATION,
            environment=self.stage,
            configuration=entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.FirebaseCredentials(
            api_key=config[API_KEY],
        )

    def get_mailgun_credentials(
        self,
    ) -> entities.MailgunCredentials:
        config = AppConfig(
            application=entities.MailgunCredentials.APPLICATION,
            environment=self.stage,
            configuration=entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.MailgunCredentials(
            api_key=config[API_KEY],
            domain=config["domain"],
        )

    def get_twilio_credentials(
        self,
    ) -> entities.TwilioCredentials:
        config = AppConfig(
            application=entities.TwilioCredentials.APPLICATION,
            environment=self.stage,
            configuration=entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.TwilioCredentials(
            account_sid=config["account_sid"],
            api_key=config["api_key"],
            auth_token=config["auth_token"],
        )

    def get_au10tix_credentials(
        self,
    ) -> entities.Au10tixCredentials:
        config = AppConfig(
            application=entities.Au10tixCredentials.APPLICATION,
            environment=self.stage,
            configuration=entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.Au10tixCredentials(
            sub=config["sub"],
            iss=config["iss"],
            aud=config["aud"],
            kid=config["kid"],
            private_key=config["private_key"],
            callback_url=config["callback_url"],
            verification_link_url_endpoint=config["verification_link_url_endpoint"],
            access_token_endpoint=config["access_token_endpoint"],
            bos_image_verification_endpoint=config["bos_image_verification_endpoint"],
            bos_get_readiness_verification_result_endpoint=config[
                "bos_get_readiness_verification_result_endpoint"
            ],
            bos_get_verification_result_endpoint=config[
                "bos_get_verification_result_endpoint"
            ],
            dashboard_url=config["dashboard_url"],
            poa_endpoint=config["poa_endpoint"],
            poa_endpoint_dc_result=config["poa_endpoint_dc_result"],
            callback_poa_url=config["callback_poa_url"],
        )

    def get_rudderstack_credentials(
        self,
    ) -> entities.RudderstackCredentials:
        config = AppConfig(
            application=entities.RudderstackCredentials.APPLICATION,
            environment=self.stage,
            configuration=entities.DEFAULT_CONFIG_NAME,
        ).load()

        return entities.RudderstackCredentials(
            write_key=config["write_key"],
            data_plane_url=config["data_plane_url"],
        )
