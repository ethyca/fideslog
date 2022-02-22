import logging

from fastapi import FastAPI
from uvicorn import run

from config import get_config, ServerSettings

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

app = FastAPI(title="fideslog")


def run_webserver(server_config: ServerSettings) -> None:
    """
    Manages the API server lifecycle.
    """

    log.info("Starting the server...")
    run(
        "main:app",
        host=server_config.host,
        log_level=logging.WARNING,
        log_config=None,
        port=server_config.port,
        reload=server_config.hot_reload,
    )
    log.info("Server stopped. Goodbye!")


if __name__ == "__main__":
    config = get_config()
    run_webserver(config.server)
