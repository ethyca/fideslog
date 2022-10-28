# pylint: disable= too-many-arguments, too-many-instance-attributes, too-many-locals

from datetime import datetime, timezone

from .exceptions import InvalidEventError


class Registration:
    """
    A discrete event, representing a user registering their information.
    """

    def __init__(
        self,
        email: str,
        organization: str,
        created_at: datetime,
    ) -> None:
        """
        Define a new user registration event to send to the fideslog server.

        :param email: User email
        :param organization: User organization
        :param created_at: The UTC timestamp when the event occurred, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. Must include the UTC timezone, and represent a datetime in the past.

        """

        try:
            assert (
                email is not None and email.find("@") != -1
            ), "A valid email must be provided"
            self.email = email

            assert organization is not None, "An organization must be provided"
            self.organization = organization

            assert (
                created_at.tzinfo is not None and created_at.tzinfo == timezone.utc
            ), "created_at must use the UTC timezone"
            assert created_at < datetime.now(
                timezone.utc
            ), "created_at must be in the past"
            self.created_at = created_at

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None
