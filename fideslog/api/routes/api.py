from typing import Dict

from fastapi import APIRouter, status
from fideslog.api.endpoints import events

api_router = APIRouter()
api_router.include_router(events.router)


@api_router.get(
    "/health",
    response_model=Dict[str, str],
    responses={
        status.HTTP_200_OK: {
            "content": {"application/json": {"example": {"status": "healthy"}}},
        }
    },
    tags=["Health"],
)
async def health() -> Dict[str, str]:
    """Confirm that the API is running and healthy."""

    return {"status": "healthy"}
