import pytest
from datetime import datetime, timezone

from fideslog.sdk.python import client, event


API_KEY = "Token 12345"


@pytest.fixture()
def test_create_client():
    yield client.AnalyticsClient(
        api_key=API_KEY,
        client_id="fake_client_id",
        os="Darwin",
        product_name="fideslog",
        production_version="1.2.3",
    )


@pytest.fixture()
def test_basic_additional_payload():
    yield event.AnalyticsEvent(
        event="test_event",
        event_created_at=datetime.now(timezone.utc),
    )


@pytest.fixture()
def test_rich_additional_payload():
    yield event.AnalyticsEvent(
        event="test_event",
        event_created_at=datetime.now(timezone.utc),
        command="test_command",
        docker=True,
        status_code=200,
        extra_data={"extra": "data"},
    )


def test_create_client_attribute(test_create_client):
    assert test_create_client.client_id == "fake_client_id"
    assert test_create_client.extra_data == None


def test_basic_event_payload(test_basic_additional_payload):
    assert test_basic_additional_payload.event == "test_event"


def test_rich_event_payload(test_rich_additional_payload):
    assert test_rich_additional_payload.command == "test_command"
    assert test_rich_additional_payload.docker
    assert test_rich_additional_payload.status_code == 200
    assert isinstance(test_rich_additional_payload.extra_data, dict)
