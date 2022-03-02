from typing import Optional


class AnalyticsException(Exception):
    """
    To be raised wherever an exception is required in this package.
    """

    def __init__(
        self,
        message: str,
        *args: object,
        status_code: Optional[int] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, *args)

    def __str__(self) -> str:
        if self.status_code is not None:
            return f"{self.status_code} response from fideslog: {self.message}"

        return f"Failed to send analytics event: {self.message}"
