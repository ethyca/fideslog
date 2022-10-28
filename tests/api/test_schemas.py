# pylint: disable=redefined-outer-name

from datetime import datetime, timedelta, timezone
from typing import Generator

import pytest
from pydantic import ValidationError

from fideslog.api.schemas.analytics_event import AnalyticsEvent
from fideslog.api.schemas.registration import Registration


class TestAnalyticsEventSchema:
    @pytest.fixture()
    def analytics_event_payload(self) -> Generator:
        """
        Yield an analytics event payload.
        """

        yield {
            "client_id": "test_client_id",
            "event": "test_event_type",
            "event_created_at": "2022-02-21 19:56:11Z",
            "os": "darwin",
            "product_name": "test_product",
            "production_version": "1.2.3",
            "status_code": 200,
            "endpoint": "GET: https://www.example.com/path/string",
            "flags": ["-f", "-y", "--test"],
            "command": "apply",
            "error": "Internal Server Error",
            "local_host": True,
            "extra_data": {"extra_value": "extra_value"},
            "docker": True,
            "resource_counts": {"datasets": 1, "policies": 1, "systems": 27},
            "developer": True,
        }

    def test_analytic_event_model(self, analytics_event_payload: dict) -> None:
        """
        Test that pydantic validations succeed for a valid payload.
        """

        assert AnalyticsEvent.parse_obj(analytics_event_payload) is not None


class TestUserRegistrationEventSchema:
    @pytest.fixture()
    def user_registration_event_payload(self) -> Generator:
        """
        Yield a test user registration payload.
        """

        yield {
            "email": "johndoe@example.com",
            "organization": "ACME",
            "client_id": "totally_unique_id",
            "created_at": "2022-10-26T19:07:41Z",
        }

    def test_user_registration_event_schema(
        self, user_registration_event_payload: dict
    ) -> None:
        """
        Test that pydantic validations succeed for a valid payload.
        """

        assert Registration.parse_obj(user_registration_event_payload) is not None

    def test_catch_invalid_email(self, user_registration_event_payload: dict):
        user_registration_event_payload["email"] = "invalid_email"
        with pytest.raises(ValidationError) as exe:
            Registration.parse_obj(user_registration_event_payload)

        print(exe.value.errors())
        assert len(exe.value.errors()) == 1
        assert exe.value.errors()[0]["msg"] == "value is not a valid email address"

    def test_catch_invalid_client_id(self, user_registration_event_payload: dict):
        user_registration_event_payload["client_id"] = "@_invalid_client_id"
        with pytest.raises(ValidationError) as exe:
            Registration.parse_obj(user_registration_event_payload)

        assert len(exe.value.errors()) == 1
        assert exe.value.errors()[0]["msg"] == "client_id must not be identifiable"

    def test_catch_invalid_created_at(self, user_registration_event_payload: dict):
        user_registration_event_payload["created_at"] = datetime.now() + timedelta(
            days=7
        )
        with pytest.raises(ValidationError) as exe:
            Registration.parse_obj(user_registration_event_payload)

        assert len(exe.value.errors()) == 1
        assert exe.value.errors()[0]["msg"] == "date must be an explicit UTC timestamp"

        user_registration_event_payload["created_at"] = datetime.now(
            timezone.utc
        ) + timedelta(days=7)
        with pytest.raises(ValidationError) as exe:
            Registration.parse_obj(user_registration_event_payload)

        assert len(exe.value.errors()) == 1
        assert exe.value.errors()[0]["msg"] == "date must be in the past"
