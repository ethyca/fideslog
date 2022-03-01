from typing import Dict

from fastapi import APIRouter, Depends, Security, status
from fastapi.openapi.models import APIKey

from pydantic import ValidationError

from sqlalchemy.orm import Session

from fideslog.api.models.analytics_event import AnalyticsEvent
from fideslog.api.utils.auth import get_api_key
from fideslog.api.database.dal import create_event
from fideslog.api.database.database import get_db

router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    event: Dict,
    _: APIKey = Security(get_api_key),
    database: Session = Depends(get_db),
) -> AnalyticsEvent:
    """Create a new analytics event."""
    try:
        event_obj = AnalyticsEvent.parse_obj(event)
        create_event(database=database, event=event_obj)
    except ValidationError:
        print("Write a simple error to the db for traceability")

    return event_obj
