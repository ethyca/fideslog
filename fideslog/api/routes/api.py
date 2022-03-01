from fastapi import APIRouter
from fideslog.api.endpoints import events

api_router = APIRouter()
api_router.include_router(events.router)


@api_router.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    """Confirm that the API is running and healthy."""

    return {"status": "healthy"}
