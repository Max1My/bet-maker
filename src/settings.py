from functools import lru_cache
from typing import TypeVar
import dotenv
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)
dotenv.load_dotenv()


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_prefix="app_",
    )

    debug: bool = True


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_prefix="postgres_",
        extra="allow",
    )

    scheme: str
    user: str
    password: str
    host: str
    port: str
    db: str
    url: PostgresDsn | None = None

    @field_validator("url")
    def get_postgres_dsn(
            cls,
            value: PostgresDsn | None,
            values: FieldValidationInfo,
    ) -> PostgresDsn:
        if value:
            return value
        return PostgresDsn(
            f"{values.data.get('scheme')}://"
            f"{values.data.get('user')}:"
            f"{values.data.get('password')}@"
            f"{values.data.get('host')}:"
            f"{values.data.get('port')}/"
            f"{values.data.get('db') if values.data.get('db') else 'postgres'}",
        )


@lru_cache
def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()
