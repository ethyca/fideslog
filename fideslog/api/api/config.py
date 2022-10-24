# pylint: disable= no-self-argument, no-self-use

import logging
import os
from typing import Optional, Tuple, Union

from pydantic import BaseSettings, Field, validator
from pydantic.env_settings import SettingsSourceCallable
from snowflake.sqlalchemy import URL
from toml import load

from logger import LOG_ENTRY_FORMAT, get_fideslog_logger

ENV_PREFIX = "FIDESLOG__"
CONFIG_FILE_NAME = "fideslog.toml"
CONFIG_PATH_VAR = f"{ENV_PREFIX}CONFIG_PATH"

logging.basicConfig(format=LOG_ENTRY_FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)


class Settings(BaseSettings):
    """The base model for configuration sub-sections."""

    class Config:
        """Modifies pydantic behavior."""

        extra = "ignore"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            """
            Sets ENV variable values to be treated as higher priority than __init__ values.
            """

            return env_settings, init_settings, file_secret_settings


class DatabaseSettings(Settings):
    """Configuration options for Snowflake."""

    account: str = Field(..., exclude=True)
    database: str = "raw"
    db_schema: str = "fides"
    password: str = Field(..., exclude=True)
    role: str = "event_writer"
    user: str = Field(..., exclude=True)
    warehouse: str = "fides_log"

    db_connection_uri: Optional[str] = Field(None, exclude=True)

    @validator("db_connection_uri", pre=True, always=True)
    def assemble_db_connection_uri(
        cls,
        value: Optional[str],
        values: dict[str, str],
    ) -> str:
        """
        Ensures a valid connection string is built from the provided details.
        """

        return (
            value
            if isinstance(value, str)
            else URL(
                account=values["account"],
                database=values["database"],
                password=values["password"],
                role=values["role"],
                schema=values["db_schema"],
                warehouse=values["warehouse"],
                user=values["user"],
            )
        )

    class Config:
        """Modifies pydantic behavior."""

        env_prefix = f"{ENV_PREFIX}DATABASE_"


class LoggingSettings(Settings):
    """Configuration options for API server logging."""

    destination: str = Field("stdout", min_length=1)
    level: str = Field(logging.getLevelName(logging.INFO), min_length=4, max_length=8)

    destination_type: Optional[str] = Field(None, exclude=True)
    logger: Optional[logging.Logger] = Field(None, exclude=True)

    @validator("level")
    def upcase_level_name(cls, value: str) -> str:
        """
        Ensure that the logging level one of the available logging levels,
        as defined by the [Python logging documentation](https://docs.python.org/3.9/howto/logging.html#logging-levels).
        If not, sets the logging level to "INFO".

        This also enables the value in an ENV variable or config file to be
        case-insensitive.
        """

        uppercase_value = value.upper()
        return (
            uppercase_value
            if isinstance(logging.getLevelName(uppercase_value), int)
            else "INFO"
        )

    @validator("destination_type", always=True)
    def get_destination_type(cls, _: Optional[str], values: dict[str, str]) -> str:
        """
        Determine if the `destination` is a valid file path, a valid directory, or `stdout`.
        """

        if os.path.isdir(values["destination"]):
            return "directory"

        if os.path.isfile(values["destination"]):
            return "file"

        return "stdout"

    @validator("logger", always=True)
    def configure_logger(
        cls,
        value: Optional[logging.Logger],
        values: dict[str, str],
    ) -> logging.Logger:
        """
        Use the desired `logging.Logger`, or the default fideslog logger.
        """

        return (
            value
            if isinstance(value, logging.Logger)
            else get_fideslog_logger(
                values["level"],
                values["destination"],
                values["destination_type"],
            )
        )

    class Config:
        """Modifies pydantic behavior."""

        env_prefix = f"{ENV_PREFIX}LOGGING_"


class ServerSettings(Settings):
    """Configuration options for the API server."""

    host: str = "localhost"
    hot_reload: bool = False
    port: int = 8080
    request_rate_limit: str = "100/minute"

    class Config:
        """Modifies pydantic behavior."""

        env_prefix = f"{ENV_PREFIX}SERVER_"


class FideslogSettings(Settings):
    """Configuration options for fideslog."""

    database: DatabaseSettings
    logging: LoggingSettings
    server: ServerSettings


def load_file(filename: str) -> dict[str, Union[str, int, bool]]:
    """
    Load a toml file from the first matching location. Raises a
    `FileNotFoundError` if none is found.

    Checks the following locations (in order of priority):
    1. A path defined by the `FIDESLOG__CONFIG_PATH` environment variable
    2. The current directory
    3. The parent directory
    4. The user's home directory (`~`)
    """

    possible_locations = [
        os.getenv(CONFIG_PATH_VAR),
        os.curdir,
        os.pardir,
        os.path.expanduser("~"),
    ]

    directories: list[str] = [dir for dir in possible_locations if dir]

    for directory in directories:
        log.debug(
            "Searching for configuration file in %s...",
            os.path.realpath(directory),
        )

        possible_location = os.path.join(directory, filename)
        if possible_location and os.path.isfile(possible_location):
            log.info(
                "Configuration file found: %s",
                os.path.realpath(possible_location),
            )

            return load(possible_location)

    raise FileNotFoundError


def get_config() -> FideslogSettings:
    """
    Attempt to parse and return configuration options by calling `load_file`.
    Fails on the first invalid configuration file found.
    """

    settings: FideslogSettings

    try:
        settings = FideslogSettings.parse_obj(load_file(CONFIG_FILE_NAME))
        log.debug("Successfully loaded configuration options from %s", CONFIG_FILE_NAME)
    except FileNotFoundError:
        log.warning("No %s file found", CONFIG_FILE_NAME)
        log.info(
            "Loading configuration from environment variables and default values..."
        )
        settings = FideslogSettings(
            database=DatabaseSettings(),
            logging=LoggingSettings(),
            server=ServerSettings(),
        )

    log.info("Configuration in use: %s", settings.json())
    return settings


config = get_config()
