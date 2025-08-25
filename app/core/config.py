from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Basic App Settings
    APP_NAME: str = "ondc-bap"
    VERSION: str = "0.1.0"
    ENV: str = "local"
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ONDC Configuration
    ONDC_SUBSCRIBER_ID: str = "neo-server.rozana.in"
    ONDC_SUBSCRIBER_URL: str = "https://neo-server.rozana.in"
    ONDC_DOMAIN: str = "nic2004:52110"
    ONDC_TYPE: str = "BAP"
    ONDC_CALLBACK_URL: str = "https://neo-server.rozana.in/on_subscribe"

    # ONDC Registry Settings (for production)
    ONDC_REGISTRY_URL: str = "https://registry.ondc.org"
    ONDC_GATEWAY_URL: str = "https://gateway.ondc.org"

    # Security Settings
    ONDC_PRIVATE_KEY_PATH: str = "keys/private_key.pem"
    ONDC_PUBLIC_KEY_PATH: str = "keys/public_key.pem"


settings = Settings()

