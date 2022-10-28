from logging import getLogger
from typing import Dict, Union

from fastapi import HTTPException, status

from .config import config

log = getLogger(__name__)


class NotFoundError(HTTPException):
    """
    To be raised when a request is made for an object that does not exist.
    """

    MESSAGE = "Not found"

    def __init__(self, error: Exception):
        log.error("%s: %s", self.MESSAGE, error, exc_info=error)
        super().__init__(status.HTTP_404_NOT_FOUND, self.MESSAGE)

    @classmethod
    def doc(cls) -> Dict[str, Dict]:
        """
        Returns the documentation for a 404 Not Found response,
        in the OpenAPI spec format.
        """

        return {
            "content": {
                "application/json": {
                    "example": {"detail": cls.MESSAGE},
                    "schema": {
                        "properties": {"detail": {"type": "string"}},
                        "type": "object",
                    },
                }
            }
        }


class InternalServerError(HTTPException):
    """
    To be raised when a request results in an error that cannot
    be resolved by a change to the request itself.
    """

    MESSAGE = "Internal server error"

    def __init__(self, error: Exception) -> None:
        log.error("%s: %s", self.MESSAGE, error, exc_info=error)
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.MESSAGE)

    @classmethod
    def doc(cls) -> Dict[str, Dict]:
        """
        Returns the documentation for a 500 Internal Server Error response,
        in the OpenAPI spec format.
        """

        return {
            "content": {
                "application/json": {
                    "example": {"detail": cls.MESSAGE},
                    "schema": {
                        "properties": {"detail": {"type": "string"}},
                        "type": "object",
                    },
                }
            }
        }


class TooManyRequestsError(HTTPException):
    """
    To be raised when a request exceeds the configured rate limit.
    """

    MESSAGE = "Rate limit exceeded"

    def __init__(self, error: Exception) -> None:
        log.error("%s: %s", self.MESSAGE, error, exc_info=error)
        super().__init__(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"message": self.MESSAGE, "limit": config.server.request_rate_limit},
        )

    @classmethod
    def doc(cls) -> Dict[str, Union[Dict, str]]:
        """
        Returns the documentation for a 429 Too Many Requests response,
        in the OpenAPI spec format.
        """

        return {
            "content": {
                "application/json": {
                    "example": {
                        "error": f"Rate limit exceeded: {config.server.request_rate_limit}"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}},
                    },
                }
            },
            "description": "Rate limit exceeded",
            "headers": {
                "Retry-After": {
                    "description": "The datetime after which to retry the request.",
                    "schema": {"type": "http-date"},
                },
                "X-RateLimit-Limit": {
                    "description": "The number of allowed requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Remaining": {
                    "description": "The number of remaining requests in the current period.",
                    "schema": {"type": "integer"},
                },
                "X-RateLimit-Reset": {
                    "description": "The number of seconds left in the current period.",
                    "schema": {"type": "integer"},
                },
            },
        }
