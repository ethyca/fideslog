import logging
from sys import stdout

LOG_ENTRY_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"


def get_fideslog_logger(
    level: str,
    destination: str,
    destination_type: str,
) -> logging.Logger:
    """
    Configure and return the top-level fideslog logger. All loggers retrieved
    via the standard library's `logging.getLogger()` method will use this same
    configuration, assuming that `__name__` is passed, and that `__name__`
    resolves to a descendent of the `fideslog` module.

    Ex:
    ```python
    # fideslog/api/config.py
    config_logger = logging.getLogger(__name__)
    ```
    Here, `__name__` resolves to `fideslog.api.config`, and all configuration
    applied by this function will also apply to the returned logger.
    """

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    logger = logging.getLogger("fideslog")
    logger.setLevel(logging.getLevelName(level))
    logger.propagate = False

    formatter = logging.Formatter(LOG_ENTRY_FORMAT)

    if destination_type == "stdout":
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    elif destination_type == "file":
        handler = logging.FileHandler(destination)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    elif destination_type == "directory":
        logfile_path = f"{destination}/fideslog.log"
        open(logfile_path, "x").close()

        handler = logging.FileHandler(logfile_path)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    else:
        raise ValueError('destination must be "", a valid file, or a valid directory')

    return logger
