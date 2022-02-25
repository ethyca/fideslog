from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import AnalyticsEvent as AnalyticsEventORM
from database.models import APIKey
from models.analytics_event import AnalyticsEvent


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
