from logging import getLogger
from typing import Dict

from fastapi import APIRouter, Depends, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fideslog.api.database.data_access import create_event
from fideslog.api.database.database import get_db
from fideslog.api.models.analytics_event import AnalyticsEvent

log = getLogger(__name__)
router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(event: Dict, database: Session = Depends(get_db)) -> AnalyticsEvent:
    """Create a new analytics event."""
    try:
        event_obj = AnalyticsEvent.parse_obj(event)
        create_event(database=database, event=event_obj)
    except ValidationError as e:
        log.error(e.__str__())

    return event_obj
