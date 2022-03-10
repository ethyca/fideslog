from hashlib import md5
from uuid import uuid1

from bcrypt import gensalt

FIDESCTL_API = b"fidesctl-api"
FIDESCTL_CLI = b"fidesctl-cli"
FIDESOPS = b"fidesops"
OPT_OUT_COPY = """
Fides needs your permission to send Ethyca a limited set of anonymous usage statistics.
Ethyca will only use this anonymous usage data to improve the product experience, and will never collect sensitive or personal data.

***
Don't believe us? Check out the open-source code here:
    https://github.com/ethyca/fideslog
***

To opt-out of all telemetry, press "n". To continue with telemetry, press any other key.
"""


def generate_client_id(application: bytes) -> str:
    """
    Generates a cryptographically secure, fully anonymized string
    that is globally unique to the machine on which it is generated.
    The hash digest's component values are never stored in memory.

    :param application: A bytestring corresponding to the fides tool currently in use. Consider `import`ing and using the constants available in this function's package.
    :returns: The hash digest, as a hexadecimal string, to be used as the analytics identifier for the machine on which this function is executed.
    """

    return md5(uuid1().bytes + gensalt() + application).hexdigest()
