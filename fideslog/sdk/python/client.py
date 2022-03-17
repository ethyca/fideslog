# pylint: disable=too-many-arguments

from typing import Dict, Optional
from urllib.error import HTTPError

from requests import post
from requests.exceptions import RequestException

from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsException


class AnalyticsClient:
    """
    An instance of a fides tool that wishes to send
    analytics events to the fideslog server.
    """

    server_url = "https://fideslog.ethyca.com"

    def __init__(
        self,
        client_id: str,
        os: str,
        product_name: str,
        production_version: str,
        developer_mode: bool = False,
        extra_data: Optional[Dict] = None,
    ) -> None:
        """
        Define a new client from which to send analytics events to the fideslog server.

        :param client_id: The fully anonymized, globally unique identifier for this client.
        :param os: The operating system on which this client is running, as returned by [platform.system()](https://docs.python.org/3/library/platform.html#platform.system).
        :param product_name: The name of the fides tool in which this client is integrated.
        :param production_version: The semantic version number of the fides tool in which this client is integrated.
        :param extra_data: Any additional information that should be included in all analytics events sent by this client. Any key/value pairs included here will be merged with key/value pairs included directly on specific `AnalyticsEvent`s, with the `AnalyticsEvent`'s `extra_data` taking priority.
        :param developer_mode: `True` if this client exists for the purposes of local development. Default: `False`.
        """

        for arg in [client_id, os, product_name, production_version]:
            assert arg is not None and arg != "", (
                f"{arg=}".split("=")[0] + " must be provided"
            )

        self.client_id = client_id
        self.os = os
        self.product_name = product_name
        self.production_version = production_version
        self.developer_mode = developer_mode
        self.extra_data = extra_data

    async def send(self, event: AnalyticsEvent) -> None:
        """
        Record a new event.
        """

        payload = {
            "client_id": self.client_id,
            "developer": self.developer_mode,
            "docker": event.docker,
            "event": event.event,
            "event_created_at": event.event_created_at.isoformat(),
            "local_host": event.local_host,
            "os": self.os,
            "product_name": self.product_name,
            "production_version": self.production_version,
        }

        payload_extras = [
            "command",
            "endpoint",
            "error",
            "flags",
            "resource_counts",
            "status_code",
        ]

        event_dict = vars(event)
        for extra in payload_extras:
            if event_dict[extra]:
                payload[extra] = event_dict[extra]

        extra_data: Dict = {}
        if self.extra_data is not None:
            extra_data = self.extra_data

        if event.extra_data is not None:
            for key, val in event.extra_data.items():
                extra_data[key] = val

        payload["extra_data"] = extra_data

        try:
            response = post(
                f"{self.server_url}/events",
                json=payload,
                timeout=(3.05, 120),
            )
            try:
                response.raise_for_status()
            except HTTPError as error:
                raise AnalyticsException(
                    error.reason, error.args, status_code=error.code
                ) from error

        except RequestException as exc:
            raise AnalyticsException(exc.strerror, exc.args) from exc
