from datetime import datetime, timezone
from json import dumps
from logging import getLogger
from typing import Optional
from urllib.parse import urlparse
from uuid import uuid1

from mypy_boto3_s3.client import S3Client

from ..schemas.analytics_event import AnalyticsEvent

EXCLUDED_ATTRIBUTES = set(("client_id", "endpoint", "extra_data", "os"))


log = getLogger(__name__)


def file_name_random() -> str:
    """
    Generates a random uuid to be passed as the filename
    """
    return uuid1().hex + ".json"


def create(client: S3Client, bucket: str, event: AnalyticsEvent) -> None:
    """Create a new analytics event."""

    logged_event = event.dict(exclude=EXCLUDED_ATTRIBUTES)
    log.debug("Creating event from: %s", logged_event)
    log.debug(
        "The following attributes have been excluded as PII: %s", EXCLUDED_ATTRIBUTES
    )

    event.endpoint = truncate_endpoint_url(event.endpoint)

    date_dir = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_file = file_name_random()

    client.put_object(
        Bucket=bucket,
        Key=f"{date_dir}/{new_file}",
        Body=dumps(event.dict(), indent=4, sort_keys=True, default=str),
    )

    log.debug("Event created: %s", logged_event)


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
