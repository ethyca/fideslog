import csv
from datetime import datetime, timezone
from uuid import uuid1

from fideslog.api.schemas.analytics_event import AnalyticsEvent


class Pipe:
    """
    Class that imitates a file object in write mode
    Used to write out a csv for use with S3
    """

    value = ""

    def write(self, text: str) -> None:
        """
        Sets the value to be returned as a csv
        """
        self.value = self.value + text


def file_name_random() -> str:
    """
    Generates a random uuid to be passed as the filename
    """
    utc_datetime = datetime.now(timezone.utc)
    return utc_datetime.strftime("%H-%M-") + uuid1().hex + ".csv"


def write_csv_object(event: AnalyticsEvent) -> str:
    """
    Writes out a csv object to be loaded
    """
    pipe = Pipe()
    writer = csv.DictWriter(pipe, list(event.__fields__))
    writer.writerow(event.dict())

    return pipe.value
