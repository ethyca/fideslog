from sqlalchemy import select
from sqlalchemy.orm import Session

from fideslog.api.models.analytics_event import AnalyticsEvent

from fideslog.api.database.models import AnalyticsEvent as AnalyticsEventORM
from fideslog.api.database.models import APIKey


# TODO: Finish this
def create_event(database: Session, event: AnalyticsEvent) -> AnalyticsEventORM:
    """Create a new analytics event."""

    database.add(AnalyticsEventORM())

    return AnalyticsEventORM()


def api_key_exists(database: Session, token: str) -> bool:
    """
    Return whether the provided token exists in the database.
    """

    return (
        database.execute(
            select(APIKey).where(APIKey.api_key == token).limit(1),
        ).first()
        is not None
    )
