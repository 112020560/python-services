from dataclasses import dataclass

DEFAULT_CONFIG_NAME = "credentials"


@dataclass
class OpenfinCredentials:
    base_url: str
    username: str
    password: str

    APPLICATION = "openfin"


@dataclass
class DatabaseCredentials:
    name: str
    host: str
    readonly_host: str
    port: int
    password: str
    username: str

    APPLICATION = "fondeadora_database"


@dataclass
class FirebaseCredentials:
    api_key: str

    APPLICATION = "firebase"


@dataclass
class MailgunCredentials:
    api_key: str
    domain: str

    APPLICATION = "mailgun"


@dataclass
class TwilioCredentials:
    account_sid: str
    api_key: str
    auth_token: str

    APPLICATION = "twilio"


@dataclass
class Au10tixCredentials:
    sub: str
    iss: str
    aud: str
    kid: str
    private_key: str
    callback_url: str
    verification_link_url_endpoint: str
    access_token_endpoint: str
    bos_image_verification_endpoint: str
    bos_get_readiness_verification_result_endpoint: str
    bos_get_verification_result_endpoint: str
    dashboard_url: str
    callback_poa_url: str
    poa_endpoint: str
    poa_endpoint_dc_result: str

    APPLICATION = "au10tix"


@dataclass
class RudderstackCredentials:
    write_key: str
    data_plane_url: str

    APPLICATION = "rudderstack"
