from logging import getLogger

from boto3 import Session
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, Request, status

from ..config import config
from ..database import get_storage
from ..database.events import create
from ..errors import InternalServerError, TooManyRequestsError
from ..schemas.analytics_event import AnalyticsEvent

LOG_BUCKET = config.storage.bucket_name

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
    config_dict = (
        {
            "region_name": config.storage.region_name,
            "aws_access_key_id": config.storage.aws_access_key_id,
            "aws_secret_access_key": config.storage.aws_secret_access_key,
        }
        if config.storage.region_name
        else {}
    )

    client = session.client("s3", **config_dict)  # type: ignore
    try:
        create(client=client, bucket=LOG_BUCKET, event=event)
        client.close()
    except ClientError as err:
        raise InternalServerError(err) from err

    return event
