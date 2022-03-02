# pylint: disable=too-many-arguments

from typing import Dict, Optional
from urllib.error import HTTPError

from requests import PreparedRequest, post
from requests.auth import AuthBase
from requests.exceptions import RequestException

from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsException


class AnalyticsAuth(AuthBase):
    """
    Attaches fideslog authentication to a given Request object.
    """

    def __init__(self, api_key: str):
        self.token = api_key

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers["Authorization"] = f"Token {self.token}"
        return request


class AnalyticsClient:
    """
    An instance of a fides tool that wishes to send
    analytics events to the fideslog server.
    """

    def __init__(
        self,
        api_key: str,
        client_id: str,
        os: str,
        product_name: str,
        production_version: str,
        extra_data: Optional[Dict] = None,
    ) -> None:
        # pylint: disable=line-too-long
        """
        Define a new client from which to send analytics events to the fideslog server.

        :param api_key: The authorization token, administered by Ethyca, that enables query access to the fideslog server.
        :param client_id: The fully anonymized, globally unique identifier for this client.
        :param os: The operating system on which this client is running, as returned by [platform.system()](https://docs.python.org/3/library/platform.html#platform.system).
        :param product_name: The name of the fides tool in which this client is integrated.
        :param production_version: The semantic version number of the fides tool in which this client is integrated.
        :param extra_data: Any additional information that should be included in all analytics events sent by this client. Any key/value pairs included here will be merged with key/value pairs included directly on specific `AnalyticsEvent`s, with the `AnalyticsEvent`'s `extra_data` taking priority.
        """
        # pylint: enable=line-too-long

        for arg in [api_key, client_id, os, product_name, production_version]:
            assert arg is not None and arg != "", (
                f"{arg=}".split("=")[0] + " must be provided"
            )

        self.api_key = api_key
        self.client_id = client_id
        self.os = os
        self.product_name = product_name
        self.production_version = production_version
        self.extra_data = extra_data

    async def send(self, event: AnalyticsEvent) -> None:
        """
        Record a new event.
        """

        payload = {
            "client_id": self.client_id,
            "docker": event.docker,
            "event": event.event,
            "event_created_at": event.event_created_at,
            "local_host": event.local_host,
            "os": self.os,
            "product_name": self.product_name,
            "production_version": self.production_version,
        }

        payload_extras = [
            "command",
            "endpoint",
            "error",
            # "extra_data",
            "flags",
            "resource_counts",
            "status_code",
        ]

        event_dict = event.dict()
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
                "http://localhost:8080",
                auth=AnalyticsAuth(self.api_key),
                json=payload,
                timeout=(3.05, 120),
            )

            try:
                response.raise_for_status()
            except HTTPError as e:
                raise AnalyticsException(e.reason, e.args, status_code=e.code) from e

        except RequestException as e:
            raise AnalyticsException(e.strerror, e.args) from e
