from json import dumps
from logging import getLogger
from typing import Optional
from urllib.parse import urlparse

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..models.models import AnalyticsEvent as AnalyticsEventORM
from ..models.models import Registration as RegistrationORM
from ..schemas.analytics_event import AnalyticsEvent
from ..schemas.registration import Registration

EXCLUDED_ATTRIBUTES = set(("client_id", "endpoint", "extra_data", "os"))


log = getLogger(__name__)


def create_event(database: Session, event: AnalyticsEvent) -> None:
    """Create a new analytics event."""

    logged_event = event.dict(exclude=EXCLUDED_ATTRIBUTES)
    log.debug("Creating event from: %s", logged_event)
    log.debug(
        "The following attributes have been excluded as PII: %s", EXCLUDED_ATTRIBUTES
    )

    extra_data = dumps(event.extra_data) if event.extra_data else None
    flags = ", ".join(event.flags) if event.flags else None
    resource_counts = (
        dumps(event.resource_counts.dict()) if event.resource_counts else None
    )
    endpoint = truncate_endpoint_url(event.endpoint)

    database.add(
        AnalyticsEventORM(
            client_id=event.client_id,
            command=event.command,
            developer=event.developer,
            docker=event.docker,
            endpoint=endpoint,
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
    log.debug("Event created: %s", logged_event)


def create_registration(
    database: Session,
    event: Registration,
) -> None:
    """Create a new registration."""
    log.debug("Creating registration")
    database.add(
        RegistrationORM(
            client_id=event.client_id,
            email=event.email,
            organization=event.organization,
            registered_at=event.created_at,
        )
    )

    database.commit()
    log.debug("Registration created")


def update_registration(
    database: Session,
    registration: Registration,
) -> RegistrationORM:
    """Modify an existing registration"""
    log.debug("Updating registration: %s", registration.client_id)
    record = (
        database.query(RegistrationORM)
        .filter_by(client_id=registration.client_id)
        .first()
    )
    if record is None:
        raise NoResultFound

    record.email = registration.email
    record.organization = registration.organization

    database.commit()
    log.debug("Updated registration: %s", registration.client_id)

    return record


def delete_registration(database: Session, client_id: str) -> None:
    """Delete an existing registration"""
    log.debug("Deleting registration: %s", client_id)

    record = database.query(RegistrationORM).filter_by(client_id=client_id).first()
    database.delete(record)
    database.commit()

    log.debug("Deleted registration: %s", client_id)


def truncate_endpoint_url(endpoint: Optional[str]) -> Optional[str]:
    """
    Guarantee that only the endpoint path is stored in the database.
    """

    if endpoint is None:
        return None

    endpoint_components = endpoint.split(":", maxsplit=1)
    http_method = endpoint_components[0].strip().upper()
    url = endpoint_components[1].strip()
    return f"{http_method}: {urlparse(url).path}"
