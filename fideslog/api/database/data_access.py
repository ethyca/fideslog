import logging
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

# from fidesapi.database.session import async_session ## future to do after working sync

from fideslog.api.models.analytics_event import AnalyticsEvent

from fideslog.api.database.models import AnalyticsEvent as AnalyticsEventORM
from fideslog.api.database.models import APIKey

log = logging.getLogger(__name__)

# TODO: Finish this
def create_event(database: Session, event: AnalyticsEvent) -> None:
    """Create a new analytics event."""

    try:
        log.debug("Creating resource")
        event_record = AnalyticsEventORM(
            client_id=event.client_id,
            product_name=event.product_name,
            production_version=event.production_version,
            os=event.os,
            docker=event.docker,
            resource_counts=json.dumps(event.resource_counts.dict())
            if event.resource_counts
            else None,
            event=event.event,
            command=event.command,
            flags=", ".join(event.flags) if event.flags else None,
            endpoint=event.endpoint,
            status_code=event.status_code,
            error=event.error,
            local_host=event.local_host,
            extra_data=json.dumps(event.extra_data) if event.extra_data else None,
            event_created_at=event.event_created_at,
        )
        database.add(event_record)
        database.commit()
    except DBAPIError:
        log.error("Insert Failed")


def api_key_exists(database: Session, token: str) -> bool:
    """
    Return whether the provided token exists in the database.

    Temporarily returns True to negate the need for an API key.
    """

    return True
