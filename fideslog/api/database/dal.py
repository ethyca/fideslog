from sqlalchemy.orm import Session
from sqlalchemy import select

from models.analytics_event import AnalyticsEvent
from database.models import APIKey, AnalyticsEvent as AnalyticsEventORM


# TODO: Finish this
def create_event(db: Session, event: AnalyticsEvent) -> AnalyticsEventORM:
    """Create a new analytics event."""

    db.add(AnalyticsEventORM())


def api_key_exists(db: Session, token: str) -> bool:
    """
    Return whether the provided token exists in the database.
    """

    result = db.execute(select(APIKey).where(APIKey.api_key == token))
    return len(result) > 0
