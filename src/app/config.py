from pydantic import AnyUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    SECRET: str

    # DATABASE
    SQLALCHEMY_DATABASE_URI: AnyUrl

    # Mail credentials
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_TO: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
