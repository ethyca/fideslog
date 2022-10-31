from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from ..database import get_db
from ..database.registrations import create, delete, get, update
from ..errors import InternalServerError, NotFoundError, TooManyRequestsError
from ..models.models import Registration as RegistrationORM
from ..schemas.registration import Registration

log = getLogger(__name__)
registration_router = APIRouter(tags=["Registrations"], prefix="/registrations")


@registration_router.get(
    "",
    response_description="A list of registrations",
    response_model=List[Registration],
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_200_OK,
)
async def list_registrations(
    _: Request,
    params: Params = Depends(),
    database: Session = Depends(get_db),
) -> AbstractPage[RegistrationORM]:
    """
    List existing registrations.
    """

    try:
        registrations = get(database, params)
    except DBAPIError as err:
        raise InternalServerError(err) from err

    return registrations.items  # type: ignore[attr-defined]


@registration_router.post(
    "",
    response_description="The created registration",
    response_model=Registration,
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_registration(
    _: Request,
    registration: Registration,
    database: Session = Depends(get_db),
) -> Registration:
    """
    Create a new registration.
    """

    try:
        create(database, registration)
    except DBAPIError as err:
        raise InternalServerError(err) from err

    return registration


@registration_router.patch(
    "",
    response_description="The updated registration",
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundError.doc(),
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    response_model=Registration,
    status_code=status.HTTP_200_OK,
)
async def modify_registration(
    _: Request,
    registration: Registration,
    database: Session = Depends(get_db),
) -> RegistrationORM:
    """
    Update an existing registration.
    """

    try:
        updated = update(database, registration)
    except NoResultFound as err:
        raise NotFoundError(err) from err
    except Exception as err:
        raise InternalServerError(err) from err

    return updated


@registration_router.delete(
    "/{client_id}",
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundError.doc(),
        status.HTTP_429_TOO_MANY_REQUESTS: TooManyRequestsError.doc(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerError.doc(),
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_registration(
    _: Request,
    client_id: str,
    database: Session = Depends(get_db),
) -> Response:
    """
    Delete a registration.
    """

    try:
        delete(database, client_id)
    except UnmappedInstanceError as err:
        raise NotFoundError(err) from err
    except Exception as err:
        raise InternalServerError(err) from err

    return Response(status_code=status.HTTP_204_NO_CONTENT)
