# pylint: disable= line-too-long, no-self-argument, no-self-use

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, validator


class APIKey(BaseModel):
    """The model for API keys."""

    api_key: str = Field(..., description="The access key, provided by Ethyca")
    client_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for the client",
    )
    created_at: Optional[datetime] = Field(
        None,
        description="The UTC timestamp when the API key was created, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="The UTC timestamp when the API key was last updated, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )

    @validator("client_id")
    def check_not_an_email_address(cls, value: str) -> str:
        """
        Validate that client_id does not contain an email address literal.
        """

        assert value.find("@") == -1, "client_id must not be identifiable"
        return value

    @validator("created_at", "updated_at")
    def check_in_the_past(cls, value: datetime) -> datetime:
        """
        Validate that a timestamp is in the past.
        """

        assert value.tzinfo == timezone.utc, "date must be an explicit UTC timestamp"
        assert value < datetime.now(timezone.utc), "date must be in the past"
        return value

    class Config:
        """Modifies pydantic behavior."""

        orm_mode = True
