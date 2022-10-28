from datetime import datetime, timezone

from .exceptions import InvalidEventError


class Registration:
    """
    Represents a user registering their information.
    """

    def __init__(self, email: str, organization: str, created_at: datetime) -> None:
        """
        Define a new user registration.

        :param email: The user's email address.
        :param organization: The user's organization.
        :param created_at: The UTC timestamp when the user registered, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. Must include the UTC timezone, and represent a datetime in the past.

        """

        try:
            assert "@" in email, "a valid email address must be provided"
            self.email = email

            assert len(organization) > 0, "organization must be provided"
            self.organization = organization

            self.created_at = self.validate_created_at(created_at)

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None

    @staticmethod
    def validate_created_at(date: datetime) -> datetime:
        """
        Asserts that `date` is an explicit UTC timestamp in the past.
        """

        assert date.tzinfo is not None, "created_at must include a UTC timezone"
        assert date.tzinfo == timezone.utc, "created_at must use the UTC timezone"
        assert date < datetime.now(timezone.utc), "created_at must be in the past"
        return date
