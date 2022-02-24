import logging
from datetime import datetime
from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, Request, Response
from uvicorn import run

from config import ServerSettings, get_config
from routes.api import api_router

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

app = FastAPI(title="fideslog")
app.include_router(api_router)


@app.middleware("http")
async def log_request(request: Request, call_next: Callable) -> Response:
    "Log basic information about every request handled by the server."
    start = datetime.now()
    response = await call_next(request)
    handler_time = (datetime.now() - start).microseconds * 0.001
    log.info(
        'Request received (handled in %sms):\t"%s %s" %s',
        handler_time,
        request.method,
        request.url.path,
        f"{response.status_code} {HTTPStatus(response.status_code).phrase}",
    )
    return response


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
