from logging import getLogger
from json import dumps

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from fideslog.api.database.models import AnalyticsEvent as AnalyticsEventORM

# from fidesapi.database.session import async_session ## future to do after working sync
from fideslog.api.models.analytics_event import AnalyticsEvent

log = getLogger(__name__)


def create_event(database: Session, event: AnalyticsEvent) -> None:
    """Create a new analytics event."""

    try:
        log.debug("Creating resource")
        extra_data = dumps(event.extra_data) if event.extra_data else None
        flags = ", ".join(event.flags) if event.flags else None
        resource_counts = (
            dumps(event.resource_counts.dict()) if event.resource_counts else None
        )
        database.add(
            AnalyticsEventORM(
                client_id=event.client_id,
                command=event.command,
                docker=event.docker,
                endpoint=event.endpoint,
                error=event.error,
                event=event.event,
                event_created_at=event.event_created_at,
                extra_data=extra_data,
                flags=flags,
                local_host=event.local_host,
                os=event.os,
                product_name=event.product_name,
                production_version=event.production_version,
                resource_counts=resource_counts,
                status_code=event.status_code,
            )
        )
        database.commit()
    except DBAPIError:
        log.error("Insert Failed")


def api_key_exists(
    database: Session, token: str  # pylint: disable=unused-argument
) -> bool:
    """
    Return whether the provided token exists in the database.

    Temporarily returns True to negate the need for an API key.
    """

    return True
