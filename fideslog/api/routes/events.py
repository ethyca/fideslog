from logging import getLogger

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from ..database.data_access import create_event
from ..database.database import get_db
from ..errors import InternalServerError, TooManyRequestsError
from ..schemas.analytics_event import AnalyticsEvent

log = getLogger(__name__)
event_router = APIRouter(tags=["Events"], prefix="/events")


@event_router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_201_CREATED,
)
async def create(
    _: Request,
    event: AnalyticsEvent,
    database: Session = Depends(get_db),
) -> AnalyticsEvent:
    """
    Create a new analytics event.
    """

    try:
        create_event(database=database, event=event)
    except DBAPIError as err:
        raise InternalServerError(err) from err

    return event
