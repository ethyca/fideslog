from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from api.database.dal import api_key_exists
from api.database.database import get_db
from utils.exceptions import (
    AuthenticationException,
    InvalidAuthorizationSchemeException,
)

API_KEY_HEADER = "Authorization"
API_KEY_PREFIX = "Token "

api_key_header = APIKeyHeader(name=API_KEY_HEADER)


def get_api_key(
    db: Session = Depends(get_db),
    header_value: str = Depends(api_key_header),
) -> str:
    """
    Fetch the value of the API key provided in an Authorization
    header. The header's value must be formatted as "Token <API key>".
    """

    if not header_value.startswith(API_KEY_PREFIX):
        raise InvalidAuthorizationSchemeException()

    token = header_value.removeprefix(API_KEY_PREFIX)
    if not api_key_exists(db, token):
        raise AuthenticationException()

    return token
