# pylint: disable=import-outside-toplevel, too-many-arguments

from asyncio import run
from sys import platform, version_info
from typing import Dict, Optional

from aiohttp import (
    ClientConnectionError,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
)

from . import __version__
from .event import AnalyticsEvent
from .exceptions import (
    AnalyticsSendError,
    InvalidClientError,
    UnknownError,
    UnreachableServerError,
)

REQUIRED_HEADERS = {"X-Fideslog-Version": __version__}


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

        try:
            assert client_id != "", "client_id must be provided"
            assert os != "", "os must be provided"
            assert product_name != "", "product_name must be provided"
            assert production_version != "", "production_version must be provided"
        except AssertionError as err:
            raise InvalidClientError(str(err)) from None

        self.client_id = client_id
        self.os = os
        self.product_name = product_name
        self.production_version = production_version
        self.developer_mode = developer_mode
        self.extra_data = extra_data or {}

    def send(self, event: AnalyticsEvent) -> None:
        """
        Record a new event.
        """

        # Works around a bug in the default Windows event loop for Python 3.8+
        # by changing the default event loop in Windows processes.
        if (
            version_info[0] == 3
            and version_info[1] >= 8
            and platform.lower().startswith("win")
        ):
            from asyncio import (  # type: ignore
                WindowsSelectorEventLoopPolicy,
                set_event_loop_policy,
            )

            set_event_loop_policy(WindowsSelectorEventLoopPolicy())

        run(self.__send(event))

    def __get_request_payload(self, event: AnalyticsEvent) -> Dict:
        """
        Construct the `POST` body required for a new `AnalyticsEvent` to
        be recorded via the API server.
        """

        payload = {
            "client_id": self.client_id,
            "developer": self.developer_mode,
            "docker": event.docker,
            "event": event.event,
            "event_created_at": event.event_created_at.isoformat(),
            "extra_data": {**self.extra_data, **event.extra_data},
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

        return payload

    async def __send(self, event: AnalyticsEvent) -> None:
        """
        Asynchronously record a new `AnalyticsEvent`.
        """

        async with ClientSession(
            self.server_url,
            headers=REQUIRED_HEADERS,
            timeout=ClientTimeout(connect=3.05, total=120),
        ) as session:
            try:
                async with session.post(
                    "/events",
                    json=self.__get_request_payload(event),
                ) as resp:
                    resp.raise_for_status()

            except ClientConnectionError as err:
                raise UnreachableServerError(err.__str__()) from err
            except ClientResponseError as err:
                raise AnalyticsSendError(err.message, err.status) from err
            except Exception as err:
                raise UnknownError(err) from err
