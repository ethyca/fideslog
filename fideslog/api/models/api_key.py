# pylint: disable=line-too-long

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from fideslog.api.models.validation import check_in_the_past, check_not_an_email_address


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
