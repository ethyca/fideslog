from hashlib import md5
from uuid import uuid1

from bcrypt import gensalt

FIDES = b"fides"
FIDESCTL_API = b"fidesctl-api"
FIDESCTL_CLI = b"fidesctl-cli"
FIDESOPS = b"fidesops"

OPT_OUT_COPY = """
Ethyca exists to make privacy a default feature of any tech stack, and we need your consent to use some of your data to achieve this mission:

    - Usage statistics, including a unique identifier, for product improvement
    - Your email address and organization name, for our sales team (we will never share this data)

You can learn more, and manage your privacy settings any time by visiting:
    https://fid.es/privacy
"""
OPT_OUT_PROMPT = (
    "To opt out of all, press 'n'. To opt-in and continue, press any other key."
)
EMAIL_PROMPT = "Email address: "
ORGANIZATION_PROMPT = "Organization name: "
CONFIRMATION_COPY = """
Thank you! To disable analytics at any time, set 'analytics_opt_out = false' in your configuration. For more information, our analytics collection code is fully open source:
    https://github.com/ethyca/fideslog
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
