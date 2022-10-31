from datetime import datetime, timezone

from .exceptions import InvalidEventError


class Registration:
    """
    Represents a user registering their information.
    """

    def __init__(
        self,
        email: str,
        organization: str,
        created_at: datetime = datetime.now(tz=timezone.utc),
        updated_at: datetime = datetime.now(tz=timezone.utc),
    ) -> None:
        """
        Define a new user registration.

        :param email: The user's email address.
        :param organization: The user's organization.
        :param created_at: The UTC timestamp when the registration occurred, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.
        :param updated_at: The UTC timestamp when the registration was last updated, in ISO 8601 format. Must include the UTC timezone, and represent a datetime in the past.
        """

        try:
            assert "@" in email, "a valid email address must be provided"
            self.email = email

            assert len(organization) > 0, "organization must be provided"
            self.organization = organization

            self.created_at = created_at
            self.updated_at = updated_at

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None
