from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    """Confirm that the API is running and healthy."""

    return {"status": "healthy"}
