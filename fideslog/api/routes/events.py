from logging import getLogger

from boto3 import Session
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, Request, status

from ..database import get_storage
from ..database.events import create
from ..errors import InternalServerError, TooManyRequestsError
from ..schemas.analytics_event import AnalyticsEvent

LOG_BUCKET = "fideslog-test"
# TODO - replace with an env var and load via config

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
async def add_event(
    _: Request,
    event: AnalyticsEvent,
    session: Session = Depends(get_storage),
) -> AnalyticsEvent:
    """
    Create a new analytics event.
    """

    try:
        create(session=session, bucket=LOG_BUCKET, event=event)
    except ClientError as err:
        raise InternalServerError(err) from err

    return event
