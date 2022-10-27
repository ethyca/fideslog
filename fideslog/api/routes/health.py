from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from ..errors import TooManyRequestsError

health_router = APIRouter(tags=["Health"])


@health_router.get(
    "/health",
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
    },
    status_code=status.HTTP_200_OK,
)
async def health(_: Request) -> JSONResponse:
    """Confirm that the API is running and healthy."""

    return JSONResponse({"status": "healthy"})
