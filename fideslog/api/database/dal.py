from sqlalchemy.orm import Session
from sqlalchemy import select

from fideslog.api.models.analytics_event import AnalyticsEvent
from fideslog.api.database.models import APIKey, AnalyticsEvent as AnalyticsEventORM


# TODO: Finish this
def create_event(db: Session, event: AnalyticsEvent) -> AnalyticsEventORM:
    """Create a new analytics event."""

    db.add(AnalyticsEventORM())


def api_key_exists(db: Session, token: str) -> bool:
    """
    Return whether the provided token exists in the database.
    """

    return (
        db.execute(
            select(APIKey).where(APIKey.api_key == token).limit(1),
        ).first()
        is not None
    )
