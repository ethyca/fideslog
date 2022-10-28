from datetime import datetime, timezone

from .exceptions import InvalidEventError


class Registration:
    """
    Represents a user registering their information.
    """

    def __init__(self, email: str, organization: str) -> None:
        """
        Define a new user registration.

        :param email: The user's email address.
        :param organization: The user's organization.
        """

        try:
            assert "@" in email, "a valid email address must be provided"
            self.email = email

            assert len(organization) > 0, "organization must be provided"
            self.organization = organization

            self.created_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None
