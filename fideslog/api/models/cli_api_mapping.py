from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from fideslog.api.models.validation import check_in_the_past, check_not_an_email_address


class CLIAPIMapping(BaseModel):
    """The model for CLI/API mappings."""

    id: Optional[str] = Field(
        None,
        description="The unique identifier for the mapping.",
    )
    api_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for an API server instance.",
    )
    cli_id: str = Field(
        ...,
        description="The fully anonymized, globally unique identifier for a CLI instance.",
    )
    created_at: Optional[datetime] = Field(
        None,
        description="The UTC timestamp when the mapping was created, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="The UTC timestamp when the mapping was last updated, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.",
    )

    _check_not_an_email_address: classmethod = validator(
        "api_id",
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
