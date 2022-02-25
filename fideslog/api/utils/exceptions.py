from fastapi import HTTPException, status


class AuthenticationException(HTTPException):
    """
    To be raised when attempting to fetch an access token using
    invalid credentials.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid credentials",
        )


class InvalidAuthorizationSchemeException(HTTPException):
    """
    To be raised when attempting to authenticate with an unexpected
    Authorization header value.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate",
            headers={"WWW-Authenticate": "Token "},
        )
