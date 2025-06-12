from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    DOCKER_RUN: bool = False

    TESTS_MONGODB_HOST: str
    TESTS_MONGODB_PORT: int
    TESTS_MONGODB_USER: str
    TESTS_MONGODB_PASSWORD: str
    TESTS_MONGODB_DB: str

    TESTS_RABBITMQ_HOST: str
    TESTS_RABBITMQ_USER: str
    TESTS_RABBITMQ_PASSWORD: str
    TESTS_RABBITMQ_VHOST: str
    TESTS_RABBITMQ_PORT: int

    TESTS_NOTIFICATION_SERVICE_QUEUE_NAME: str = 'tests_notification_service_queue'
    TESTS_NANOSERVICES_EXCH_NAME: str
    TESTS_NOTIFICATION_SERVICE_CONSUMING_TOPICS: list[str] = ['fake.notification.topic',]

    TESTS_SMTP_HOST: str
    TESTS_SMTP_USER: str
    TESTS_SMTP_PORT: int
    TESTS_SMTP_PASSWORD: str
    TESTS_SMTP_USE_TLS: bool = False
    TESTS_SMTP_USE_SSL: bool = False

    TESTS_TWILIO_ACCOUNT_SID: str
    TESTS_TWILIO_AUTH_TOKEN: str

    TESTS_FROM_EMAIL: str
    TESTS_FROM_PHONE_NUMBER: str

    @property
    def TESTS_MONGODB_URL(self):
        return (
            f'mongodb://'
            f'{self.TESTS_MONGODB_USER}:'
            f'{self.TESTS_MONGODB_PASSWORD}@'
            f'{self.TESTS_MONGODB_HOST}:'
            f'{27017 if self.DOCKER_RUN else self.TESTS_MONGODB_PORT}/'
            f'{self.TESTS_MONGODB_DB}'
            f'?authSource=admin'
        )

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env.tests',
        case_sensitive=True,
    )


test_settings = TestSettings() # type: ignore
