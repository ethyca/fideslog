from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import APIKey

from models.analytics_event import AnalyticsEvent
from utils.auth import get_api_key

router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    event: AnalyticsEvent,
    _: APIKey = Depends(get_api_key),
) -> AnalyticsEvent:
    """Create a new analytics event."""

    return event
