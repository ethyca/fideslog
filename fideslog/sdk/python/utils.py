from hashlib import md5
from uuid import uuid1

from bcrypt import gensalt

FIDESCTL_API = b"fidesctl-api"
FIDESCTL_CLI = b"fidesctl-cli"
FIDESOPS = b"fidesops"


def generate_client_id(application: bytes) -> str:
    """
    Generates a cryptographically secure, fully anonymized string
    that is globally unique to the machine on which it is generated.
    The hash digest's component values are never stored in memory.

    :param application: A bytestring corresponding to the fides tool currently in use. Consider `import`ing and using the constants available in this function's package.
    :returns: The hash digest, as a hexadecimal string, to be used as the analytics identifier for the machine on which this function is executed.
    """

    return md5(uuid1().bytes + gensalt() + application).hexdigest()
