# pylint: disable=too-many-arguments

from typing import Any, Optional
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
        extra_data: Optional[dict[str, Any]] = None,
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
