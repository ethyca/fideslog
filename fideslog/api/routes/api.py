from typing import Dict

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from ..endpoints.events import router as event_router

api_router = APIRouter()
api_router.include_router(event_router)


@api_router.get(
    "/health",
    response_model=Dict[str, str],
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {"example": {"status": "healthy"}}},
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "content": {
                "application/json": {
                    "example": {"error": "Rate limit exceeded: 6 per minute"}
                }
            },
            "description": "Rate limit exceeded",
        },
    },
    tags=["Health"],
)
async def health(request: Request) -> JSONResponse:  # pylint: disable=unused-argument
    """Confirm that the API is running and healthy."""

    return JSONResponse({"status": "healthy"})
