from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from ..config import config
from ..database.data_access import create_event
from ..database.database import get_db
from ..schemas.analytics_event import AnalyticsEvent

log = getLogger(__name__)
router = APIRouter(tags=["Events"], prefix="/events")


@router.post(
    "",
    response_description="The created event",
    response_model=AnalyticsEvent,
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "content": {
                "application/json": {
                    "example": {
                        "error": f"Rate limit exceeded: {config.server.request_rate_limit}"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}},
                    },
                }
            },
            "description": "Rate limit exceeded",
            "headers": {
                "Retry-After": {
                    "description": "The datetime after which to retry the request.",
                    "schema": {"type": "http-date"},
                },
                "X-RateLimit-Limit": {
                    "description": "The number of allowed requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Remaining": {
                    "description": "The number of remaining requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Reset": {
                    "description": "The number of seconds left in the current period.",
                    "schema": {"type": "integer"},
                },
            },
        }
    },
    status_code=status.HTTP_201_CREATED,
)
async def create(
    request: Request,  # pylint: disable=unused-argument
    event: AnalyticsEvent,
    database: Session = Depends(get_db),
) -> AnalyticsEvent:
    """
    Create a new analytics event.
    """

    try:
        create_event(database=database, event=event)
    except DBAPIError as err:
        log.error("Failed to create event: %s", err, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        ) from None

    return event
