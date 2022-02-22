import os
from logging import getLogger
from typing import Any, Tuple

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from toml import load

ENV_PREFIX = "FIDESLOG__"
CONFIG_FILE_NAME = "fideslog.toml"
CONFIG_PATH_VAR = f"{ENV_PREFIX}CONFIG_PATH"

log = getLogger(__name__)


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


class ServerSettings(Settings):
    """Configuration options for the API server."""

    host: str = "0.0.0.0"
    hot_reload: bool = False
    port: int = 8080

    class Config:
        """Modifies pydantic behavior."""

        env_prefix = f"{ENV_PREFIX}SERVER_"


class FideslogSettings(Settings):
    """Configuration options for fideslog."""

    server: ServerSettings = ServerSettings()


def load_file(filename: str) -> dict[str, Any]:
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
        log.info("Loading configuration from environment variables...")
        settings = FideslogSettings()

    log.info("Configuration in use: %s", settings.json())
    return settings
