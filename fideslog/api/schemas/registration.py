# pylint: disable= no-self-argument, no-self-use

from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field, validator

from .validation import check_in_the_past, check_not_an_email_address


class Registration(BaseModel):
    """The schema for registrations."""

    client_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for the event sender.",
    )
    email: EmailStr = Field(
        ...,
        description="The user's email address.",
    )
    organization: str = Field(
        ...,
        description="The organization in which the user is registered.",
    )
    created_at: datetime = Field(
        datetime.now(tz=timezone.utc),
        description="The UTC timestamp when the registration occurred, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )
    updated_at: datetime = Field(
        datetime.now(tz=timezone.utc),
        description="The UTC timestamp when the registration was last updated, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )

    _check_not_an_email_address: classmethod = validator(
        "client_id",
        allow_reuse=True,
    )(check_not_an_email_address)

    _check_in_the_past: classmethod = validator(
        "created_at",
        "updated_at",
        allow_reuse=True,
    )(check_in_the_past)

    class Config:
        """Modifies pydantic behavior."""

        orm_mode = True
