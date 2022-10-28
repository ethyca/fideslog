# pylint: disable= too-many-arguments, too-many-instance-attributes, too-many-locals

from datetime import datetime, timezone

from ..exceptions import InvalidEventError


class UserRegistrationEvent:
    """
    A discrete event, representing a user action within a fides tool.
    """

    def __init__(
        self,
        email: str,
        organization: str,
        registered_at: datetime,
    ) -> None:
        """
        Define a new user registration event to send to the fideslog server.

        :param email: User email
        :param organization: User organization
        :param registered_at: The UTC timestamp when the event occurred, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. Must include the UTC timezone, and represent a datetime in the past.

        """

        try:
            assert email is not None and email.find("@") != -1
            self.email = email

            assert organization is not None
            self.organization = organization

            assert (
                registered_at.tzinfo is not None
                and registered_at.tzinfo == timezone.utc
            ), "event_created_at must use the UTC timezone"
            assert registered_at < datetime.now(
                timezone.utc
            ), "event_created_at must be in the past"
            self.registered_at = registered_at

        except AssertionError as err:
            raise InvalidEventError(str(err)) from None
