from fastapi import APIRouter, Security, status
from fastapi.openapi.models import APIKey

from fideslog.api.models.analytics_event import AnalyticsEvent
from fideslog.api.utils.auth import get_api_key

router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    event: AnalyticsEvent,
    _: APIKey = Security(get_api_key),
) -> AnalyticsEvent:
    """Create a new analytics event."""

    return event
