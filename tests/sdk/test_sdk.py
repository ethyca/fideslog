# pylint: disable=redefined-outer-name

from datetime import datetime, timezone
from typing import Generator

import pytest

from fideslog.sdk.python.analytics_event import AnalyticsEvent
from fideslog.sdk.python.client import AnalyticsClient


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
        status_code=200,
        extra_data={"extra": "data"},
    )


def test_create_client_attribute(test_create_client: AnalyticsClient) -> None:
    """
    Test that AnalyticsClients are created as expected.
    """

    assert test_create_client.client_id == "fake_client_id"
    assert test_create_client.extra_data == {}


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
    assert test_rich_additional_payload.status_code == 200
    assert isinstance(test_rich_additional_payload.extra_data, dict)
