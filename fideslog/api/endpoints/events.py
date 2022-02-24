from fastapi import APIRouter, status
from models.analytics_event import AnalyticsEvent

router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(event: AnalyticsEvent) -> AnalyticsEvent:
    """Create a new analytics event."""

    return event
