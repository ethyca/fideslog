class AnalyticsError(Exception):
    """
    To be raised wherever an exception is required.
    """


class AnalyticsSendError(AnalyticsError):
    """
    To be raised when the fideslog API server responds with
    a non-2XX status code.
    """

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"The fideslog API responded with an error: {self.status_code} {self.message}"


class InvalidClientError(AnalyticsError):
    """
    To be raised when an `AnalyticsClient` cannot be created.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"Failed to initialize AnalyticsClient: {self.message}"


class InvalidEventError(AnalyticsError):
    """
    To be raised when an `AnalyticsEvent` cannot be created.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"Failed to initialize AnalyticsEvent: {self.message}"


class UnknownError(AnalyticsError):
    """
    To be raised when an unforeseen error occurs.
    """

    def __init__(self, error: Exception) -> None:
        self.message = error.__str__()
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"An unknown error occurred: {self.message}"


class UnreachableServerError(AnalyticsError):
    """
    To be raised when a connection to the fideslog API server
    cannot be made.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"Failed to connect to the fideslog API server: {self.message}"
