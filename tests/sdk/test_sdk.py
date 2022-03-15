# pylint: disable=redefined-outer-name

from datetime import datetime, timezone
from typing import Generator

import pytest

from fideslog.api.models.analytics_event import AnalyticsEvent as APIAnalyticsEvent
from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent


@pytest.fixture()
def test_create_client() -> Generator:
    """
    Yield a test AnalyticsClient.
    """

    yield AnalyticsClient(
        client_id="fake_client_id",
        os="Darwin",
        product_name="fideslog",
        production_version="1.2.3",
    )


@pytest.fixture()
def test_basic_additional_payload() -> Generator:
    """
    Yield a simple test AnalyticsEvent.
    """

    yield AnalyticsEvent(
        event="test_event",
        event_created_at=datetime.now(timezone.utc),
    )


@pytest.fixture()
def test_rich_additional_payload() -> Generator:
    """
    Yield a complex test AnalyticsEvent.
    """

    yield AnalyticsEvent(
        event="test_event",
        event_created_at=datetime.now(timezone.utc),
        command="test_command",
        docker=True,
        status_code=0,
        extra_data={"extra": "data"},
        resource_counts={
            "datasets": 0,
            "policies": 0,
            "systems": 0,
        },
        endpoint="https://www.example.com/path/string",
        flags=["-f", "-y", "--test"],
        error=None,
        local_host=True,
    )


@pytest.yield_fixture()
def test_rich_additional_payload_with_error(
    test_rich_additional_payload: AnalyticsEvent,
) -> Generator:
    """
    Yield a complex test AnalyticsEvent.
    """

    event = test_rich_additional_payload
    event.status_code = 1
    event.error = "Internal Server Error"

    yield event


def test_create_client_attribute(test_create_client: AnalyticsClient) -> None:
    """
    Test that AnalyticsClients are created as expected.
    """

    assert test_create_client.client_id == "fake_client_id"
    assert test_create_client.extra_data is None


def test_basic_event_payload(test_basic_additional_payload: AnalyticsEvent) -> None:
    """
    Test that simple AnalyticsEvents are created as expected.
    """

    assert test_basic_additional_payload.event == "test_event"


def test_rich_event_payload(test_rich_additional_payload: AnalyticsEvent) -> None:
    """
    Test that complex AnalyticsEvents are created as expected.
    """

    assert test_rich_additional_payload.command == "test_command"
    assert test_rich_additional_payload.docker
    assert test_rich_additional_payload.status_code == 0
    assert isinstance(test_rich_additional_payload.extra_data, dict)


def test_sdk_to_api_types(
    test_create_client: AnalyticsClient,
    test_rich_additional_payload: AnalyticsEvent,
) -> None:
    """
    Validate that all sdk values align with their API equivalent
    """

    prepared_payload = test_create_client._prepare_payload(test_rich_additional_payload)
    api_analytics_event = APIAnalyticsEvent.parse_obj(prepared_payload)

    assert api_analytics_event


def test_sdk_to_api_types_with_error(
    test_create_client: AnalyticsClient,
    test_rich_additional_payload_with_error: AnalyticsEvent,
) -> None:
    """
    Validate that all sdk values align with their API equivalent
    """

    prepared_payload = test_create_client._prepare_payload(
        test_rich_additional_payload_with_error
    )

    assert APIAnalyticsEvent.parse_obj(prepared_payload)
