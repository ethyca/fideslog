from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import sys
sys.path.append(".")
from api.config import config
from api.endpoints.events import router as event_router

api_router = APIRouter()
api_router.include_router(event_router)


@api_router.get(
    "/health",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {"status": "healthy"},
                    "schema": {
                        "type": "object",
                        "properties": {"status": {"type": "string"}},
                    },
                }
            }
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "content": {
                "application/json": {
                    "example": {
                        "error": f"Rate limit exceeded: {config.server.request_rate_limit}"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}},
                    },
                }
            },
            "description": "Rate limit exceeded",
            "headers": {
                "Retry-After": {
                    "description": "The datetime after which to retry the request.",
                    "schema": {"type": "http-date"},
                },
                "X-RateLimit-Limit": {
                    "description": "The number of allowed requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Remaining": {
                    "description": "The number of remaining requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Reset": {
                    "description": "The number of seconds left in the current period.",
                    "schema": {"type": "integer"},
                },
            },
        },
    },
    tags=["Health"],
)
async def health(request: Request) -> JSONResponse:  # pylint: disable=unused-argument
    """Confirm that the API is running and healthy."""

    return JSONResponse({"status": "healthy"})
