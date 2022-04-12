from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from ..database.data_access import create_event
from ..database.database import get_db
from ..models.analytics_event import AnalyticsEvent

log = getLogger(__name__)
router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    event: AnalyticsEvent,
    database: Session = Depends(get_db),
) -> AnalyticsEvent:
    """Create a new analytics event."""
    try:
        create_event(database=database, event=event)
    except DBAPIError as err:
        log.error("Failed to create event: %s", err, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        ) from err
    else:
        return event
