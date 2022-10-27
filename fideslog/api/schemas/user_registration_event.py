# pylint: disable= no-self-argument, no-self-use

from datetime import datetime, timezone

from pydantic import BaseModel, Field, validator


class UserRegistrationEvent(BaseModel):
    """The model for user registration events."""

    analytics_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for the event sender.",
    )
    email: str = Field(
        ...,
        description="User registration event email",
    )
    organization: str = Field(
        ...,
        description="TUser registration event organization",
    )
    registered_at: datetime = Field(
        ...,
        description="The UTC timestamp when the user registration event occurred, in ISO 8601 format. Must include "
        "the UTC timezone, and represent a datetime in the past.",
    )

    @validator("analytics_id")
    def check_not_an_email_address(cls, value: str) -> str:
        """
        Validate that analytics_id does not contain an email address literal.
        """

        assert value.find("@") == -1, "analytics_id must not be identifiable"
        return value

    @validator("email")
    def check_email(cls, value: str) -> str:
        """
        Validate that email is an email.
        """

        assert value.find("@") != -1, "email must contain a valid email address"
        return value

    @validator("registered_at")
    def check_in_the_past(cls, value: datetime) -> datetime:
        """
        Validate that the event creation timestamp is in the past.
        """

        assert (
            value.tzinfo == timezone.utc
        ), "event_created_at must be an explicit UTC timestamp"
        assert value < datetime.now(
            timezone.utc
        ), "event_created_at must be in the past"
        return value

    class Config:
        """Modifies pydantic behavior."""

        orm_mode = True
