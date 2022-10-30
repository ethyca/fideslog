# pylint: disable= too-many-arguments, too-many-instance-attributes, too-many-locals

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from validators import url as is_valid_url

from .exceptions import InvalidEventError

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


class AnalyticsEvent:
    """
    A discrete event, representing a user action within a fides tool.
    """

    def __init__(
        self,
        event: str,
        event_created_at: datetime,
        command: Optional[str] = None,
        docker: bool = False,
        endpoint: Optional[str] = None,
        error: Optional[str] = None,
        extra_data: Optional[Dict] = None,
        flags: Optional[List[str]] = None,
        local_host: Optional[bool] = None,
        resource_counts: Optional[Dict[str, int]] = None,
        status_code: Optional[int] = None,
    ) -> None:
        """
        Define a new analytics event to send to the fideslog server.

        :param event: The name/type of this event.
        :param event_created_at: The UTC timestamp when the event occurred, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. Must include the UTC timezone, and represent a datetime in the past.
        :param command: For events submitted as a result of running CLI commands, the name of the command that was submitted. May include the subcommand name(s).
        :param docker: `True` if the command was submitted within a Docker container. Default: `False`.
        :param endpoint: For events submitted as a result of making API server requests, the HTTP method and full API endpoint URL included on the request, delimited by a colon. Ex: `GET: https://www.example.com/api/path`. The URL will be truncated, and only the URL path will be stored.
        :param error: For events submitted as a result of running CLI commands that exit with a non-0 status code, or events submitted as a result of API server requests that respond with a non-2xx status code, the error type, without specific error details.
        :param extra_data: Any additional key/value pairs that should be associated with this event.
        :param flags: For events submitted as a result of running CLI commands, the flags in use when the command was submitted. Omits flag values (when they exist) by persisting only the portion of each string in this list that come before `=` or `space` characters.
        :param local_host: For events submitted as a result of making API server requests, `True` if the API server is running on the user's local host, otherwise `False`. Default: `None` (acceptable only when `endpoint` is also `None`).
        :param resource_counts: Should contain the counts of dataset, policy, and system manifests in use when this event was submitted. Include all three keys, even if one or more of their values are `0`. Ex: `{ "datasets": 7, "policies": 26, "systems": 9 }`.
        :param status_code: For events submitted as a result of making API server requests, the HTTP status code included in the response.
        """

        try:
            assert len(event) > 0, "event (name or type) is required"
            self.event = event

            self.event_created_at = self.validate_created_at(event_created_at)
            self.resource_counts = self.validate_resource_counts(resource_counts)
            self.endpoint, self.local_host = self.validate_endpoint_and_local_host(
                endpoint,
                local_host,
            )
            self.command = command
            self.docker = docker
            self.error = error
            self.extra_data = extra_data or {}
            self.flags = flags
            self.status_code = status_code

            if self.command is not None or self.endpoint is not None:
                assert self.status_code is not None, "status_code must be provided"

            if self.error is not None:
                assert (
                    self.status_code is not None
                ), "An error was provided, but status_code is empty"
                assert self.status_code > 0 and (
                    self.status_code < 200 or self.status_code > 299
                ), "An error was provided, but the provided status_code indicates success"

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None

    @staticmethod
    def validate_created_at(date: datetime) -> datetime:
        """
        Asserts that `date` is an explicit UTC timestamp in the past.
        """

        assert date.tzinfo is not None, "event_created_at must include a UTC timezone"
        assert date.tzname() == str(
            timezone.utc
        ), "event_created_at must use the UTC timezone"
        assert date < datetime.now(timezone.utc), "event_created_at must be in the past"
        return date

    @staticmethod
    def validate_resource_counts(
        resource_counts: Optional[Dict[str, int]]
    ) -> Optional[Dict[str, int]]:
        """
        Asserts that `resource_counts` conforms to the expected type.
        """

        if resource_counts is None:
            return None

        for key in ["datasets", "policies", "systems"]:
            val = resource_counts.get(key)
            assert val is not None, f'resource_counts must include a "{key}" key'
            assert isinstance(
                val,
                int,
            ), f'The value of resource_counts["{key}"] must be an integer'

        return resource_counts

    @staticmethod
    def validate_endpoint_and_local_host(
        endpoint: Optional[str],
        local_host: Optional[bool],
    ) -> Tuple[Optional[str], Optional[bool]]:
        """
        Asserts that if `endpoint` is provided, then `local_host` is also provided,
        and that `endpoint` conforms to the expected format.
        """

        if endpoint is None:
            return (None, local_host)

        assert local_host is not None, "local_host must be provided"

        endpoint_components = endpoint.split(":", maxsplit=1)
        assert (
            len(endpoint_components) == 2
        ), "endpoint must contain only the HTTP method and URL, delimited by a colon"

        http_method = endpoint_components[0].strip().upper()
        assert (
            http_method in ALLOWED_HTTP_METHODS
        ), f"HTTP method must be one of: {', '.join(ALLOWED_HTTP_METHODS)}"

        url = endpoint_components[1].strip()
        assert is_valid_url(
            url.replace("://0.0.0.0", "://localhost", 1)
        ), "endpoint URL must be a valid URL"

        return (f"{http_method}: {url}", local_host)
