from datetime import datetime, timezone
from logging import getLogger
from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..models.models import Registration as RegistrationORM
from ..schemas.registration import Registration

log = getLogger(__name__)


def get(
    database: Session,
    count: Optional[int],
    offset: Optional[int],
) -> List[RegistrationORM]:
    """
    Return existing registrations.
    """

    log.debug("Fetching registrations")
    if count is not None:
        return database.query(RegistrationORM).limit(count).offset(offset or 0).all()

    return database.query(RegistrationORM).all()


def create(database: Session, registration: Registration) -> None:
    """
    Create a new registration.
    """

    log.debug("Creating registration for client with ID: %s", registration.client_id)
    database.add(
        RegistrationORM(
            client_id=registration.client_id,
            email=registration.email,
            organization=registration.organization,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    )

    database.commit()
    log.debug(
        "Successfully created registration for client with ID: %s",
        registration.client_id,
    )


def update(
    database: Session,
    registration: Registration,
) -> RegistrationORM:
    """
    Modify an existing registration.
    """

    log.debug("Updating registration for client with ID: %s", registration.client_id)
    record = (
        database.query(RegistrationORM)
        .filter_by(client_id=registration.client_id)
        .first()
    )
    if record is None:
        raise NoResultFound

    record.email = registration.email
    record.organization = registration.organization
    record.updated_at = datetime.now(timezone.utc)

    database.commit()
    log.debug("Updated registration for client with ID: %s", registration.client_id)

    return record


def delete(database: Session, client_id: str) -> None:
    """
    Delete an existing registration.
    """

    log.debug("Deleting registration for client with ID: %s", client_id)

    record = database.query(RegistrationORM).filter_by(client_id=client_id).first()
    database.delete(record)
    database.commit()

    log.debug("Deleted registration for client with ID: %s", client_id)
