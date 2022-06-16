# pylint: disable= no-self-argument, no-self-use

from datetime import datetime, timezone
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator
from validators import url as is_valid_url

from .manifest_file_counts import ManifestFileCounts

ALLOWED_HTTP_METHODS = [
    "CONNECT",
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "TRACE",
]


class AnalyticsEvent(BaseModel):
    """The model for analytics events."""

    client_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for the event sender.",
    )
    command: Optional[str] = Field(
        None,
        description="For events submitted as a result of running CLI commands, the name of the command that was submitted.",
    )
    developer: bool = Field(
        False,
        description="`true` if the command was submitted during local development of a fides tool, otherwise `false`.",
    )
    docker: bool = Field(
        False,
        description="`true` if the command was submitted within a Docker container, otherwise `false`.",
    )
    endpoint: Optional[str] = Field(
        None,
        description="For events submitted as a result of making API server requests, the HTTP method and full API endpoint URL included on the request, delimited by a colon. Ex: `GET: https://www.example.com/api/path`. The URL will be truncated, and only the URL path will be stored.",
    )
    error: Optional[str] = Field(
        None,
        description="For events submitted as a result of running CLI commands that exit with a non-0 status code, or events submitted as a result of API server requests that respond with a non-2xx status code, the error **type**, without specific error details.",
    )
    event: str = Field(..., description="The name/type of event submitted.")
    event_created_at: datetime = Field(
        ...,
        description="The UTC timestamp when the event occurred, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )
    extra_data: Optional[Dict] = Field(
        None,
        description="A JSON object containing any additional data desired.",
    )
    flags: Optional[List[str]] = Field(
        None,
        description="For events submitted as a result of running CLI commands, the flags in use when the command was submitted. Omits flag values when they exist.",
    )
    local_host: bool = Field(
        False,
        description="For events submitted as a result of making API server requests, `true` if the API server is running on the user's local host, otherwise `false`.",
    )
    os: str = Field(
        ...,
        description="The operating system in use when the event was submitted.",
    )
    product_name: str = Field(
        ...,
        description="The fides product from which the analytics event was sent.",
    )
    production_version: str = Field(
        ...,
        description="The fides product's version number.",
    )
    resource_counts: Optional[ManifestFileCounts]
    status_code: Optional[int] = Field(
        None,
        description="For events submitted as a result of making API server requests, the HTTP status code included in the response.",
    )

    @validator("client_id")
    def check_not_an_email_address(cls, value: str) -> str:
        """
        Validate that client_id does not contain an email address literal.
        """

        assert value.find("@") == -1, "client_id must not be identifiable"
        return value

    @validator("endpoint")
    def validate_endpoint_format(cls, value: Optional[str]) -> Optional[str]:
        """
        Ensure that `endpoint` contains the request's HTTP method and URL.
        """

        if value is None:
            return None

        endpoint_components = value.split(":", maxsplit=1)
        assert (
            len(endpoint_components) == 2
        ), "endpoint must contain only the HTTP method and URL, delimited by a colon"

        http_method = endpoint_components[0].strip().upper()
        assert (
            http_method in ALLOWED_HTTP_METHODS
        ), f"HTTP method must be one of {', '.join(ALLOWED_HTTP_METHODS)}"

        url = endpoint_components[1].strip()
        assert is_valid_url(url), "endpoint URL must be a valid URL"

        return f"{http_method}: {url}"

    @validator("event_created_at")
    def check_in_the_past(cls, value: datetime) -> datetime:
        """
        Validate that the event creation timestamp is in the past.
        """

        assert (
            value.tzinfo == timezone.utc
        ), "event_created_at must be an explicit UTC timestamp"
        assert value < datetime.now(
            timezone.utc
        ), "event_created_at must be in the past"
        return value

    @validator("flags", each_item=True)
    def check_no_values(cls, value: str) -> str:
        """
        Ensure that flags do not include the value provided by the user, if one existed.
        """

        includes_value_chars = ["=", " "]
        for char in includes_value_chars:
            value = value.split(char)[0]

        return value

    class Config:
        """Modifies pydantic behavior."""

        orm_mode = True
