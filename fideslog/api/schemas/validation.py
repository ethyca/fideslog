from datetime import datetime, timezone


def check_not_an_email_address(value: str) -> str:
    """
    Validate that client_id does not contain an email address literal.
    """

    assert value.find("@") == -1, "client_id must not be identifiable"
    return value


def check_in_the_past(value: datetime) -> datetime:
    """
    Validate that a timestamp is in the past.
    """

    assert value.tzname() == str(timezone.utc), "date must be an explicit UTC timestamp"
    assert value < datetime.now(timezone.utc), "date must be in the past"
    return value
