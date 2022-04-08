import logging
from datetime import datetime
from http import HTTPStatus
from typing import Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from uvicorn import run

from fideslog.api.config import ServerSettings, config
from fideslog.api.routes.api import api_router

log = logging.getLogger(__name__)

app = FastAPI(title="fideslog")
app.include_router(api_router)


# Defined before `log_request` to ensure that both are always executed.
@app.middleware("http")
async def require_version_header(request: Request, call_next: Callable) -> Response:
    """
    Enforce that the `X-Fideslog-Version` header was included on the request.
    Does not apply to the `/docs` and `/openapi.json` endpoints, to ensure
    that they remain publicly available.

    This header is intentionally undocumented, for mildly increased security.
    """

    excluded_endpoints = ["/docs", "/openapi.json"]
    version = request.headers.get("x-fideslog-version", None)

    if version is None and request.url.path not in excluded_endpoints:
        return JSONResponse(
            {"error": "Missing required header(s)"},
            status.HTTP_400_BAD_REQUEST,
        )

    return await call_next(request)


@app.middleware("http")
async def log_request(request: Request, call_next: Callable) -> Response:
    """
    Log basic information about every request handled by the server.
    """

    start = datetime.now()
    response = await call_next(request)
    handler_time = round((datetime.now() - start).microseconds * 0.001, 3)
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
    run_webserver(config.server)
