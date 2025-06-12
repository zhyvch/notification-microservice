import logging
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    DOCKER_RUN: bool = False

    NOTIFICATION_SERVICE_API_HOST: str = '127.0.0.1'
    NOTIFICATION_SERVICE_API_PORT: int
    NOTIFICATION_SERVICE_API_PREFIX: str = '/api/v1'
    NOTIFICATION_SERVICE_API_DOCS_URL: str = '/api/docs'
    NOTIFICATION_SERVICE_DEBUG: bool = True

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_DB: str

    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str
    RABBITMQ_PORT: int

    NANOSERVICES_EXCH_NAME: str
    NOTIFICATION_SERVICE_QUEUE_NAME: str = 'notification_service_queue'
    NOTIFICATION_SERVICE_CONSUMING_TOPICS: list[str] = ['user.#']

    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PORT: int
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = False
    SMTP_USE_SSL: bool = False

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str

    FROM_EMAIL: str
    FROM_PHONE_NUMBER: str


    LOG_LEVEL: int = logging.WARNING  # one of logging.getLevelNamesMapping().values()
    LOG_FORMAT: str = '[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)s - %(message)s'

    @property
    def MONGODB_URL(self):
        return (
            f'mongodb://'
            f'{self.MONGODB_USER}:'
            f'{self.MONGODB_PASSWORD}@'
            f'{self.MONGODB_HOST}:'
            f'{27017 if self.DOCKER_RUN else self.MONGODB_PORT}/'
            f'{self.MONGODB_DB}'
            f'?authSource=admin'
        )

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True
    )


settings = Settings() # type: ignore
