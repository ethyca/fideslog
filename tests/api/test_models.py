import pytest

from fideslog.api.models.analytics_event import AnalyticsEvent


@pytest.fixture()
def test_full_payload():
    yield {
        "client_id": "test_client_id",
        "event": "test_event_type",
        "event_created_at": "2022-02-21 19:56:11Z",
        "os": "darwin",
        "product_name": "test_product",
        "production_version": "1.2.3",
        "status_code": 200,
        "endpoint": "https://www.example.com/path/string",
        "flags": ["-f", "-y", "--test"],
        "command": "apply",
        "error": "Internal Server Error",
        "local_host": True,
        "extra_data": {"extra_value": "extra_value"},
        "docker": True,
        "resource_counts": {"datasets": 1, "policies": 1, "systems": 27},
    }


def test_analytic_event_model(test_full_payload):
    analytic_event = AnalyticsEvent.parse_obj(test_full_payload)

    assert analytic_event is not None
